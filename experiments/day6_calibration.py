import glob
import os

import numpy as np

from app.matcher import calibrate, semantic_match
from app.parser import clean_text, extract_text_from_pdf, split_chunks

if not os.path.exists("sample_resume.pdf"):
    raise SystemExit("Put sample_resume.pdf in the project root first.")

resume_chunks = split_chunks(extract_text_from_pdf("sample_resume.pdf"))

# file name -> raw best-match values, one per JD chunk
raw = {}
for path in sorted(glob.glob("data/jd*.txt")):
    with open(path, encoding="utf-8") as f:
        jd_chunks = split_chunks(clean_text(f.read()))
    scores = [m["score"] for m in semantic_match(resume_chunks, jd_chunks)]
    raw[os.path.basename(path)] = np.array(scores)

everything = np.concatenate(list(raw.values()))
out = [f"Resume chunks: {len(resume_chunks)} | JD chunks in total: {len(everything)}\n"]

out.append("RAW best-match values across all JDs:")
for p in (5, 10, 25, 50, 75, 90, 95):
    out.append(f"  {p:>2}th percentile: {np.percentile(everything, p):.2f}")

out.append("\nPER JD (raw)        mean   min   max")
for name, s in raw.items():
    out.append(f"  {name:<20}{s.mean():>5.2f} {s.min():>5.2f} {s.max():>5.2f}")

# Suggested bounds: the unrelated JD shows what "no fit" looks like.
if "jd_unrelated.txt" in raw:
    lo_hint = float(raw["jd_unrelated.txt"].mean())
    out.append(f"\nlo hint {lo_hint:.2f} = mean raw value of jd_unrelated.txt")
else:
    lo_hint = float(np.percentile(everything, 10))
    out.append(f"\nlo hint {lo_hint:.2f} = 10th percentile (no jd_unrelated.txt found)")
hi_hint = float(np.percentile(everything, 90))
out.append(f"hi hint {hi_hint:.2f} = 90th percentile")

settings = [(0.10, 0.55), (0.25, 0.65), (round(lo_hint, 2), round(hi_hint, 2))]
out.append("\nSEMANTIC SCORE (0 to 100) of each JD under different (lo, hi):")
labels = [f"{lo:.2f}-{hi:.2f}" for lo, hi in settings]
out.append("  " + f"{'JD file':<20}" + "".join(f"{label:>12}" for label in labels))
for name, s in raw.items():
    cells = ""
    for lo, hi in settings:
        cells += f"{100 * calibrate(float(s.mean()), lo, hi):>12.0f}"
    out.append("  " + f"{name:<20}" + cells)

with open("experiments/day6_calibration.txt", "w", encoding="utf-8") as f:
    f.write("\n".join(out))
print("\n".join(out))
print("\nSaved to experiments/day6_calibration.txt")