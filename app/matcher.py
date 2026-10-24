from functools import lru_cache

from sentence_transformers import SentenceTransformer, util

MODEL_NAME = "all-MiniLM-L6-v2"


@lru_cache(maxsize=1)
def get_model() -> SentenceTransformer:
    """Load the model once, on first use, and reuse it afterwards."""
    return SentenceTransformer(MODEL_NAME)


def embed(chunks: list[str]):
    return get_model().encode(
        chunks,
        convert_to_tensor=True,
        normalize_embeddings=True,
        batch_size=32,
        show_progress_bar=False,
    )


def semantic_match(resume_chunks: list[str], jd_chunks: list[str]) -> list[dict]:
    """For each JD chunk, find the most similar resume chunk."""
    if not resume_chunks or not jd_chunks:
        return []

    sim = util.cos_sim(embed(jd_chunks), embed(resume_chunks))  # (n_jd, n_resume)
    best_scores, best_idx = sim.max(dim=1)                      # best per JD row

    return [
        {
            "requirement": jd_chunks[i],
            "best_match": resume_chunks[int(best_idx[i])],
            "score": float(best_scores[i]),
        }
        for i in range(len(jd_chunks))
    ]