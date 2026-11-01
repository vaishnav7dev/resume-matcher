import glob
import os
import time

from app.matcher import semantic_match
from app.parser import clean_text, extract_text_from_pdf, split_chunks

if not os.path.exists("sample_resume.pdf"):
    raise SystemExit("Put sample_resume.pdf in the project root first.")

resume_chunks = split_chunks(extract_text_from_pdf("sample_resume.pdf"))
semantic_match(["warm up"], ["warm up"])  # loads the model, so timing below is fair

out = [f"Resume chunks: {len(resume_chunks)}\n"]

for path in sorted(glob.glob("data/jd*.txt")):
    with open(path, encoding="utf-8") as f:
        jd_chunks = split_chunks(clean_text(f.read()))

    start = time.perf_counter()
    matches = semantic_match(resume_chunks, jd_chunks)
    elapsed = time.perf_counter() - start

    scores = [m["score"] for m in matches]
    out.append(f"=== {path} ({len(jd_chunks)} JD chunks, {elapsed:.2f}s) ===")
    out.append(
        f"mean best-match: {sum(scores) / len(scores):.2f} | "
        f"max: {max(scores):.2f} | min: {min(scores):.2f}\n"
    )
    for m in sorted(matches, key=lambda m: m["score"], reverse=True):
        out.append(f"{m['score']:.2f} | REQ : {m['requirement']}")
        out.append(f"       BEST: {m['best_match']}\n")

with open("experiments/day5_output.txt", "w", encoding="utf-8") as f:
    f.write("\n".join(out))
print("\n".join(out))
print("Saved to experiments/day5_output.txt")