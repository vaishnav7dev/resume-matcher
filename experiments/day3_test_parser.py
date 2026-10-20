import glob
from app.parser import extract_text_from_pdf, split_chunks

text = extract_text_from_pdf("sample_resume.pdf")
print("=== RAW TEXT (first 1500 characters) ===")
print(text[:1500])

chunks = split_chunks(text)
print(f"\n=== {len(chunks)} RESUME CHUNKS ===")
for i, c in enumerate(chunks, 1):
    print(f"{i:02d} [{len(c)}] {c}")

for path in sorted(glob.glob("data/jd*.txt")):
    with open(path, encoding="utf-8") as f:
        jd_chunks = split_chunks(f.read())
    print(f"\n=== {path}: {len(jd_chunks)} JD CHUNKS ===")
    for i, c in enumerate(jd_chunks, 1):
        print(f"{i:02d} [{len(c)}] {c}")