from functools import lru_cache

import numpy as np
from sentence_transformers import SentenceTransformer, util

from app.parser import clean_text, split_chunks
from app.skills import extract_skills

MODEL_NAME = "all-MiniLM-L6-v2"

# Scoring settings: first guesses, to be tuned with real data in Week 3.
W_SEMANTIC = 0.6    # share of the final score that comes from meaning similarity
W_COVERAGE = 0.4    # share that comes from skill coverage
CAL_LO = 0.25       # raw best-match cosine that counts as "no real support" (becomes 0)
CAL_HI = 0.65       # raw best-match cosine that counts as "clear support" (becomes 1)
WEAK_BELOW = 0.30   # a requirement whose calibrated fit (0 to 1) is below this is a gap


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


def calibrate(x: float, lo: float = CAL_LO, hi: float = CAL_HI) -> float:
    """Map a raw cosine value onto 0..1: lo or less becomes 0, hi or more becomes 1."""
    return float(np.clip((x - lo) / (hi - lo), 0.0, 1.0))


def _tidy(match: dict) -> dict:
    """Copy of a match with a rounded raw score and a 0 to 100 fit value."""
    return {
        **match,
        "score": round(match["score"], 2),
        "fit": round(100 * calibrate(match["score"])),
    }


def analyze(resume_text: str, jd_text: str) -> dict:
    """Score how well a resume fits a job description and report the gaps."""
    resume_text, jd_text = clean_text(resume_text), clean_text(jd_text)
    resume_chunks = split_chunks(resume_text)
    jd_chunks = split_chunks(jd_text)
    if not resume_chunks:
        raise ValueError("Could not find any usable text in the resume.")
    if not jd_chunks:
        raise ValueError("Could not find any usable text in the job description.")

    # 1. Meaning: the best resume line for every JD requirement.
    matches = semantic_match(resume_chunks, jd_chunks)
    mean_best = sum(m["score"] for m in matches) / len(matches)
    semantic = calibrate(mean_best)

    # 2. Skills: which of the JD's skills does the resume cover?
    resume_skills = extract_skills(resume_text)
    jd_skills = extract_skills(jd_text)
    matched = resume_skills & jd_skills
    missing = jd_skills - resume_skills

    # 3. Combine the two parts.
    if jd_skills:
        coverage = len(matched) / len(jd_skills)
        final = W_SEMANTIC * semantic + W_COVERAGE * coverage
    else:
        coverage = None  # no known skills in the JD, so meaning alone decides
        final = semantic

    weak = sorted(
        (m for m in matches if calibrate(m["score"]) < WEAK_BELOW),
        key=lambda m: m["score"],
    )
    return {
        "score": round(100 * final, 1),
        "semantic": round(100 * semantic, 1),
        "coverage": None if coverage is None else round(100 * coverage, 1),
        "matched_skills": sorted(matched),
        "missing_skills": sorted(missing),
        "weak_requirements": [_tidy(m) for m in weak],
        "matches": [_tidy(m) for m in matches],
    }