from sentence_transformers import SentenceTransformer

model = SentenceTransformer("all-mpnet-base-v2")

def embed_text_segments(segments: list[str], batch_size=64) -> list[list[float]]:
    return model.encode(segments, batch_size=batch_size, convert_to_numpy=True).tolist()
