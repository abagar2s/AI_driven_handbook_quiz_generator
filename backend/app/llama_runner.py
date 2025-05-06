from llama_cpp import Llama
import time

MODEL_PATH = "./app/models/llama-2-7b-chat.Q4_K_M.gguf"

llm = Llama(
    model_path=MODEL_PATH,
    n_ctx=4096,
    n_threads=8,
    n_batch=128,
    verbose=False
)

def run_llama_chat(user_prompt: str, chunk: str, max_tokens: int = 512) -> str:
    base_prompt = (
        "You are a helpful assistant that generates handbook content and quiz questions "
        "based strictly on the provided input."
    )
    full_prompt = f"{base_prompt}\n\n{user_prompt}" if user_prompt.strip() else base_prompt
    full_prompt += f"\n\nINPUT:\n{chunk}"

    start_time = time.time()
    output = llm.create_chat_completion(
        messages=[
            {"role": "system", "content": base_prompt},
            {"role": "user", "content": full_prompt}
        ],
        temperature=0.4,
        max_tokens=max_tokens,
        stop=["</s>"]
    )
    print(f"✅ Chunk processed in {time.time() - start_time:.2f} seconds")

    return output["choices"][0]["message"]["content"]