import glob
import os

from scipy.stats import spearmanr

from app.matcher import analyze
from app.parser import extract_text_from_pdf

# Fill this in BEFORE you run the script: your own 1 to 5 fit rating per JD.
GUT_RATINGS = {"jd1.txt": 4,  "jd2.txt": 2,"jd3.txt": 3, "jd_unrelated.txt": 1,}

if not os.path.exists("sample_resume.pdf"):
    raise SystemExit("Put sample_resume.pdf in the project root first.")

resume_text = extract_text_from_pdf("sample_resume.pdf")
out = []

# Sanity check: a resume compared with itself should score close to 100.
self_result = analyze(resume_text, resume_text)
out.append(f"SELF-CHECK (resume vs itself): {self_result['score']}  (expect near 100)\n")

results = []
for path in sorted(glob.glob("data/jd*.txt")):
    with open(path, encoding="utf-8") as f:
        results.append((os.path.basename(path), analyze(resume_text, f.read())))

# Ranked table
out.append(f"{'JD file':<22}{'score':>7}{'meaning':>9}{'skills':>8}{'gut':>5}   missing")
for name, r in sorted(results, key=lambda item: item[1]["score"], reverse=True):
    coverage = "n/a" if r["coverage"] is None else f"{r['coverage']:.0f}%"
    gut = GUT_RATINGS.get(name, "-")
    out.append(
        f"{name:<22}{r['score']:>7.1f}{r['semantic']:>9.1f}{coverage:>8}{gut:>5}   "
        f"{len(r['missing_skills'])} skills"
    )

# Agreement with your own ratings
rated = [(GUT_RATINGS[name], r["score"]) for name, r in results if name in GUT_RATINGS]
if len(rated) >= 3:
    rho, _ = spearmanr([g for g, _ in rated], [s for _, s in rated])
    out.append(f"\nAGREEMENT with your gut ratings (Spearman): {rho:.2f}  (1.0 = same order)")
else:
    out.append("\n(Fill in GUT_RATINGS for at least 3 JDs to see how well the order agrees.)")

# Details per JD
for name, r in results:
    out.append(f"\n=== {name} (score {r['score']}) ===")
    out.append("MATCHED : " + ", ".join(r["matched_skills"]))
    out.append("MISSING : " + ", ".join(r["missing_skills"]))
    out.append("WEAKEST REQUIREMENTS:")
    for m in r["weak_requirements"][:5]:
        out.append(f"  fit {m['fit']:>3} | {m['requirement']}")
        out.append(f"           closest: {m['best_match']}")

with open("experiments/batch_report.txt", "w", encoding="utf-8") as f:
    f.write("\n".join(out))
print("\n".join(out))
print("\nSaved to experiments/batch_report.txt")