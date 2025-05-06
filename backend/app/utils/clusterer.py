from sklearn.cluster import AgglomerativeClustering
from typing import List

def cluster_embeddings(embeddings: List[List[float]], threshold: float = 1.5) -> List[int]:
    clustering = AgglomerativeClustering(
        n_clusters=None,
        distance_threshold=threshold,
        metric="cosine",
        linkage="average"
    )
    return clustering.fit_predict(embeddings)
