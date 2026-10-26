import json
import os

from app.matcher import analyze
from app.parser import extract_text_from_pdf

if not os.path.exists("sample_resume.pdf"):
    raise SystemExit("Put sample_resume.pdf in the project root first.")

resume_text = extract_text_from_pdf("sample_resume.pdf")
with open("data/jd1.txt", encoding="utf-8") as f:
    jd_text = f.read()

result = analyze(resume_text, jd_text)
report = json.dumps(result, indent=2, ensure_ascii=False)

with open("experiments/day6_output.json", "w", encoding="utf-8") as f:
    f.write(report)
print(report)