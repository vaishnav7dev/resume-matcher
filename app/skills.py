import json
import re
from pathlib import Path

SKILLS_PATH = Path(__file__).resolve().parent.parent / "data" / "skills.json"


def load_skills(path: Path = SKILLS_PATH) -> dict[str, list[str]]:
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def _compile(skills: dict[str, list[str]]) -> dict[str, re.Pattern]:
    patterns = {}
    for canon, aliases in skills.items():
        names = {a.lower() for a in aliases} | {canon.lower()}
        # longest first, so "scikit-learn" is tried before shorter alternatives
        body = "|".join(re.escape(n) for n in sorted(names, key=len, reverse=True))
        # the lookarounds stop partial-word matches: "ml" inside "html",
        # "java" inside "javascript", "sql" inside "postgresql", "c++" vs "c"
        patterns[canon] = re.compile(rf"(?<![\w+#])(?:{body})(?![\w+#])")
    return patterns


SKILLS = load_skills()
_PATTERNS = _compile(SKILLS)


def extract_skills(text: str) -> set[str]:
    """Return the canonical names of all skills mentioned in the text."""
    t = text.lower()
    return {canon for canon, pattern in _PATTERNS.items() if pattern.search(t)}