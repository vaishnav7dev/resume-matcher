import re
import pdfplumber

BULLETS = "•●▪◦‣-–*"


def extract_text_from_pdf(file) -> str:
    """Read all pages of a PDF (path or file object) and return cleaned text."""
    with pdfplumber.open(file) as pdf:
        pages = [page.extract_text() or "" for page in pdf.pages]
    return clean_text("\n".join(pages))


def clean_text(text: str) -> str:
    """Fix common PDF glitches and collapse extra whitespace."""
    text = text.replace("\u00a0", " ")       # non-breaking space
    text = text.replace("ﬁ", "fi").replace("ﬂ", "fl")   # ligatures
    text = re.sub(r"[ \t]+", " ", text)       # many spaces -> one
    text = re.sub(r"\n{3,}", "\n\n", text)    # many blank lines -> one
    return text.strip()


def split_chunks(text: str, min_len: int = 25) -> list[str]:
    """Split text into bullet/sentence-sized chunks."""
    # Step 1: rebuild lines. PDFs wrap long bullets onto a second line,
    # so a line starting with a lowercase letter is joined to the previous one.
    merged = []
    for line in text.split("\n"):
        line = line.strip()
        if not line:
            continue
        starts_bullet = line[0] in BULLETS
        if merged and not starts_bullet and line[0].islower():
            merged[-1] += " " + line
        else:
            merged.append(line.lstrip(BULLETS + " \t"))

    # Step 2: split each line into sentences, then drop tiny fragments.
    chunks = []
    for line in merged:
        for sentence in re.split(r"(?<=[.!?])\s+(?=[A-Z])", line):
            sentence = sentence.strip()
            if len(sentence) >= min_len and not sentence.isupper():
                chunks.append(sentence)
    return chunks