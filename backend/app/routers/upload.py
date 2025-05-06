from fastapi import APIRouter, UploadFile, File, Form
from fastapi.responses import JSONResponse
from typing import List
from app.utils.extract import extract_text_from_files
from app.utils.clean import clean_text
from app.utils.chunker import chunk_text_semantically
from app.llama_runner import run_llama_chat
import logging
import json
import re
import tiktoken
import random

router = APIRouter()
MAX_TOKEN_LENGTH = 2048
import re
import json

def extract_json_block(text: str) -> dict:
    """
    Extracts and parses a JSON-like object containing keys: question, answers, right_answers.
    """
    try:
        # Find candidate block
        pattern = r"{\s*\"question\".*?\"right_answers\"\s*:\s*(\[.*?\]|\d+).*?}"
        match = re.search(pattern, text, re.DOTALL)
        if not match:
            return {}
        
        block = match.group(0)

        # Fix common formatting errors
        block = block.replace("‘", '"').replace("’", '"')  # smart quotes
        block = block.replace("“", '"').replace("”", '"')
        block = re.sub(r"//.*", "", block)  # remove inline comments
        block = re.sub(r"right_answers\"\s*:\s*(\d+)", r'right_answers": [\1]', block)

        # Load and validate
        parsed = json.loads(block)
        if (
            isinstance(parsed, dict)
            and "question" in parsed
            and "answers" in parsed
            and isinstance(parsed["answers"], list)
            and "right_answers" in parsed
        ):
            return parsed
    except Exception as e:
        print(f"⚠️ Failed to extract/parse JSON: {e}")
    return {}

# ✅ Token-safe text splitting
def split_by_tokens(text: str, max_tokens: int) -> list[str]:
    enc = tiktoken.get_encoding("cl100k_base")
    tokens = enc.encode(text)
    chunks = []
    for i in range(0, len(tokens), max_tokens):
        chunk_tokens = tokens[i:i + max_tokens]
        chunk_text = enc.decode(chunk_tokens)
        chunks.append(chunk_text)
    return chunks

@router.post("/upload")
async def upload_files(
    files: List[UploadFile] = File(...),
    prompt: str = Form("Create a training handbook and 5 quiz questions.")
):
    try:
        # 1️⃣ Extract, clean and chunk
        raw_text = await extract_text_from_files(files)
        cleaned_text = clean_text(raw_text)
        chunks = chunk_text_semantically(cleaned_text)

        # 2️⃣ Summarize each chunk
        all_summaries = [
            run_llama_chat("Summarize this section clearly and concisely.", chunk[:MAX_TOKEN_LENGTH])
            for chunk in chunks
        ]
        full_summary = "\n".join(all_summaries)

        # 3️⃣ Format final handbook
        handbook_prompt = (
            "Refine and format the following training content into a clear handbook format "
            "with sections and bullet points. Do not include quiz questions."
        )
        summary_chunks = split_by_tokens(full_summary, MAX_TOKEN_LENGTH)
        refined_parts = [
            run_llama_chat(handbook_prompt, chunk=c, max_tokens=1024)
            for c in summary_chunks
        ]
        final_handbook = "\n\n".join(refined_parts)

        # 4️⃣ Quiz generation from selected original chunks
        print(f"📊 Total chunks available: {len(chunks)}")
        quiz_questions = []
        attempts = 0

        while len(quiz_questions) < 5 and attempts < 15:
            selected_chunk = random.choice(chunks)
            print(f"\n🔍 Generating Question {len(quiz_questions) + 1}")
            print(f"📝 Selected chunk (first 300 chars):\n{selected_chunk[:300]}")

            q_prompt = (
                "Generate one multiple choice question in pure JSON format based on the following content.\n"
                "Strictly follow this format:\n\n"
                '{\n'
                '  "question": "Your question?",\n'
                '  "answers": ["Option A", "Option B", "Option C", "Option D"],\n'
                '  "right_answers": [0]  // one or more indices allowed.\n'
                '}\n\n'
                "❗Rules:\n"
                "- answers must be a list of 4 plain strings (no objects)\n"
                "- At least one of the questions should have more than one correct answer in 'right_answers'\n"
                "- No explanations. No keys other than question, answers, right_answers\n\n"
                f"CONTENT:\n{selected_chunk[:MAX_TOKEN_LENGTH]}"
            )


            raw_q = run_llama_chat(q_prompt, chunk=selected_chunk[:MAX_TOKEN_LENGTH])
            print(f"🧾 Raw model output:\n{raw_q[:500]}")
            
            try:
                parsed = extract_json_block(raw_q)
                if (
                    isinstance(parsed, dict) and
                    "question" in parsed and
                    "answers" in parsed and
                    "right_answers" in parsed and
                    isinstance(parsed["answers"], list) and
                    len(parsed["answers"]) == 4 and
                    all(isinstance(a, str) for a in parsed["answers"]) and
                    isinstance(parsed["right_answers"], list) and
                    all(isinstance(i, int) and 0 <= i < 4 for i in parsed["right_answers"])
                ):
                    quiz_questions.append(parsed)

                else:
                    print("❌ Skipped: wrong format or not enough answers.")

            except Exception as ex:
                print(f"⚠️ JSON parse failed: {ex}")

            attempts += 1


        # Final output
        print("\n📤 Sending response:")
        print("📘 Final Handbook preview:\n", final_handbook[:1000])
        print("🧪 Final Quiz JSON preview:", json.dumps(quiz_questions[:5], indent=2)[:5000])


        return JSONResponse(content={
            "handbuch": final_handbook,
            "quiz": quiz_questions[:5]  # Return top 5
        })

    except Exception as e:
        logging.exception("❌ Upload processing failed.")
        return JSONResponse(status_code=500, content={"error": str(e)})
