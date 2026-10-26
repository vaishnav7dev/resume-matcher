import json
import re
from pathlib import Path

SKILLS_PATH = Path(__file__).resolve().parent.parent / "data" / "skills.json"

# A negation word shortly before a skill means the person does NOT have it:
# "have not worked with TensorFlow", "no experience with Spark".
NEGATION = re.compile(r"\b(?:not|no|never|without|lack|lacking|unfamiliar)\b|n['’]t\b")
SENTENCE_END = re.compile(r"[.!?;\n]")
NEGATION_WINDOW = 60  # how many characters before a skill to look back


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


def _is_negated(text: str, start: int) -> bool:
    """True if a negation word sits shortly before `start`, in the same sentence."""
    before = text[max(0, start - NEGATION_WINDOW):start]
    ends = list(SENTENCE_END.finditer(before))
    if ends:
        before = before[ends[-1].end():]  # keep only the current sentence
    return bool(NEGATION.search(before))


def extract_skills(text: str) -> set[str]:
    """Return the canonical names of all skills mentioned (and not negated) in the text."""
    t = text.lower()
    found = set()
    for canon, pattern in _PATTERNS.items():
        for match in pattern.finditer(t):
            if not _is_negated(t, match.start()):
                found.add(canon)
                break  # one un-negated mention is enough
    return found