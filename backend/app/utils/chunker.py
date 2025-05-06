from app.utils.embedder import embed_text_segments
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.cluster import AgglomerativeClustering
from sklearn.preprocessing import normalize
from nltk.tokenize import sent_tokenize
import nltk
import numpy as np

nltk.download("punkt")

MAX_CHUNK_LENGTH = 2000  # characters
AGGLOMERATIVE_DISTANCE_THRESHOLD = 0.60  # lower = fewer, larger clusters

def average_similarity(embeddings, labels):
    scores = []
    for cid in set(labels):
        indices = [i for i, lbl in enumerate(labels) if lbl == cid]
        if len(indices) < 2:
            continue
        cluster_vectors = [embeddings[i] for i in indices]
        sims = cosine_similarity(cluster_vectors)
        triu_indices = np.triu_indices(len(cluster_vectors), k=1)
        if sims[triu_indices].size > 0:
            scores.append(np.mean(sims[triu_indices]))
    return np.mean(scores) if scores else 0.0

def chunk_text_semantically(text: str) -> list[str]:
    segments = sent_tokenize(text)
    
    # Step 1: Embed the sentences
    embeddings = embed_text_segments(segments)
    
    # ✅ Step 2: Normalize for cosine distance (important for clustering quality)
    embeddings = normalize(embeddings)

    # Step 3: Agglomerative clustering
    model = AgglomerativeClustering(
        distance_threshold=AGGLOMERATIVE_DISTANCE_THRESHOLD,
        n_clusters=None,
        metric="cosine",
        linkage="average"
    )
    labels = model.fit_predict(embeddings)

    # Step 4: Print evaluation score
    sim_score = average_similarity(embeddings, labels)
    print(f"✅ Agglomerative Clustering Score: {sim_score:.4f}")
    print(f"📊 Agglomerative produced {len(set(labels))} clusters")

    # Optional preview
    for i, sentence in enumerate(segments[:5]):
        print(f"🔹 Preview Segment {i}: {sentence[:60]}... → Cluster {labels[i]}")

    # Step 5: Group and chunk by cluster
    clusters = {}
    for idx, cid in enumerate(labels):
        clusters.setdefault(cid, []).append(segments[idx])

    final_chunks = []
    for group in clusters.values():
        current_chunk = ""
        for sentence in group:
            if len(current_chunk) + len(sentence) > MAX_CHUNK_LENGTH:
                final_chunks.append(current_chunk.strip())
                current_chunk = ""
            current_chunk += " " + sentence
        if current_chunk:
            final_chunks.append(current_chunk.strip())

    return final_chunks
