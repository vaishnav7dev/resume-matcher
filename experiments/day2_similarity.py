from sentence_transformers import SentenceTransformer, util

model = SentenceTransformer("all-MiniLM-L6-v2")

def sim(a: str, b: str) -> float:
    ea, eb = model.encode([a, b], convert_to_tensor=True, normalize_embeddings=True)
    return util.cos_sim(ea, eb).item()

pairs = [
    ("near-identical",
     "Built REST APIs using FastAPI",
     "Developed REST APIs with FastAPI"),
    ("same meaning, different words",
     "Experience building REST APIs in Python",
     "Developed backend web services using Flask"),
    ("same field, different skill",
     "Experience with machine learning models",
     "Built a data dashboard using Power BI"),
    ("skill list vs sentence",
     "Proficient in Python, SQL and Docker",
     "Wrote Python scripts and deployed them in Docker containers"),
    ("vague resume line",
     "Strong knowledge of deep learning frameworks",
     "Hardworking team player with good communication skills"),
    ("same word, different meaning",
     "Experience with Java programming",
     "Visited Java island and enjoyed the coffee"),
    ("negation",
     "Must have experience with Python",
     "No experience with Python"),
    ("unrelated",
     "Experience deploying ML models to production",
     "Passionate about cooking and travelling"),
    ("JD requirement vs matching project bullet",
     "Experience training and evaluating machine learning models",
     "Trained a classifier on sensor data and evaluated it using accuracy and F1-score"),

    ("JD requirement vs adjacent skill (embedded, not ML)",
     "Experience training and evaluating machine learning models",
     "Programmed an ESP32 microcontroller to read temperature sensors over I2C"),

    ("Abbreviation vs full form",
     "Familiarity with NLP and transformer models",
     "Used Hugging Face to fine-tune a BERT model for text classification"),

    ("Tool in JD vs tool-specific bullet",
     "Hands-on experience with Git and version control",
     "Managed project code on GitHub with branches and pull requests"),

    ("Soft skill in JD vs project bullet",
     "Ability to work in a team and communicate technical ideas clearly",
     "Coordinated a 5-member team to split tasks and present the project demo"),
]

for label, a, b in pairs:
    print(f"{sim(a, b):.2f} | {label}")
    print(f"     A: {a}")
    print(f"     B: {b}\n")
    print("=" * 60)
print("PART 2: best match for one JD requirement\n")

requirement = "Experience building and deploying machine learning models"

resume_lines = [
    "Fine-tuned a pretrained model for image classification using PyTorch",
    "Built an ESP32-based sensor system for motor monitoring",
    "Created a Python script to automate data cleaning with pandas",
    "Led a 5-member team for a college hackathon project",
    "Deployed a FastAPI service in Docker",
    "Won first prize in an inter-college quiz",
]

req_emb = model.encode(requirement, convert_to_tensor=True, normalize_embeddings=True)
res_emb = model.encode(resume_lines, convert_to_tensor=True, normalize_embeddings=True)
scores = util.cos_sim(req_emb, res_emb)[0]

for score, line in sorted(zip(scores.tolist(), resume_lines), reverse=True):
    print(f"{score:.2f} | {line}")