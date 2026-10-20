import glob
import os
import re

from app.parser import clean_text, extract_text_from_pdf
from app.skills import SKILLS, extract_skills

known = {a.lower() for aliases in SKILLS.values() for a in aliases} | set(SKILLS)


def candidate_terms(text: str) -> list[str]:
    """Capitalized or tool-like words the dictionary doesn't know (review by eye)."""
    words = set(re.findall(r"\b[A-Z][A-Za-z0-9+#.\-]{2,}\b", text))
    return sorted(w for w in words if w.lower() not in known)


resume_text = ""
if os.path.exists("sample_resume.pdf"):
    resume_text = extract_text_from_pdf("sample_resume.pdf")
resume_skills = extract_skills(resume_text)
print(f"RESUME skills ({len(resume_skills)}): {sorted(resume_skills)}\n")

for path in sorted(glob.glob("data/jd*.txt")):
    with open(path, encoding="utf-8") as f:
        jd_text = clean_text(f.read())
    jd_skills = extract_skills(jd_text)
    matched = jd_skills & resume_skills
    missing = jd_skills - resume_skills
    coverage = len(matched) / len(jd_skills) * 100 if jd_skills else 0
    print(f"=== {path} ===")
    print(f"JD skills ({len(jd_skills)}): {sorted(jd_skills)}")
    print(f"MATCHED : {sorted(matched)}")
    print(f"MISSING : {sorted(missing)}")
    print(f"COVERAGE: {coverage:.0f}%")
    print(f"Unknown words to review: {candidate_terms(jd_text)}\n")