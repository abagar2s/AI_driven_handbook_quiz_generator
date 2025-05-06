import pdfplumber
import io
from fastapi import UploadFile
from typing import List

async def extract_text_from_files(files: List[UploadFile]) -> str:
    content = []

    for file in files:
        filename = file.filename.lower()

        try:
            if filename.endswith(".pdf"):
                data = await file.read()
                with pdfplumber.open(io.BytesIO(data)) as pdf:
                    for page in pdf.pages:
                        text = page.extract_text()
                        if text:
                            content.append(text)

            elif filename.endswith(".txt"):
                text_bytes = await file.read()
                text = text_bytes.decode("utf-8", errors="ignore")
                content.append(text)

            else:
                print(f"⚠️ Unsupported file type: {file.filename}")

        except Exception as e:
            print(f"❌ Failed to extract from {file.filename}: {e}")

    return "\n".join(t.strip() for t in content if t.strip())
