# Day 2: Embedding experiment notes

Model: all-MiniLM-L6-v2, cosine similarity on normalized embeddings.

## Scores (Part 1), sorted by band

| Case | A | B | Score |
|---|---|---|---|
| Near-identical | Built REST APIs using FastAPI | Developed REST APIs with FastAPI | 0.97 |
| Negation (trap) | Must have experience with Python | No experience with Python | 0.88 |
| Same meaning, different words | Experience building REST APIs in Python | Developed backend web services using Flask | 0.57 |
| Skill list vs sentence | Proficient in Python, SQL and Docker | Wrote Python scripts and deployed them in Docker containers | 0.56 |
| Tool in JD vs tool-specific bullet | Hands-on experience with Git and version control | Managed project code on GitHub with branches and pull requests | 0.49 |
| Abbreviation vs full form | Familiarity with NLP and transformer models | Used Hugging Face to fine-tune a BERT model for text classification | 0.41 |
| Same word, different meaning (Java) | Experience with Java programming | Visited Java island and enjoyed the coffee | 0.41 |
| JD requirement vs matching project bullet | Experience training and evaluating machine learning models | Trained a classifier on sensor data and evaluated it using accuracy and F1-score | 0.31 |
| Soft skill vs teamwork bullet | Ability to work in a team and communicate technical ideas clearly | Coordinated a 5-member team to split tasks and present the project demo | 0.29 |
| Unrelated | Experience deploying ML models to production | Passionate about cooking and travelling | 0.18 |
| Same field, different skill | Experience with machine learning models | Built a data dashboard using Power BI | 0.11 |
| Vague resume line | Strong knowledge of deep learning frameworks | Hardworking team player with good communication skills | 0.11 |
| Adjacent skill (embedded, not ML) | Experience training and evaluating machine learning models | Programmed an ESP32 microcontroller to read temperature sensors over I2C | 0.03 |

## Bands

| Band | Range |
|---|---|
| Good match | 0.49 to 0.57 |
| Weak or partial | 0.29 to 0.41 |
| Noise | 0.03 to 0.18 |

## Part 2: ranking resume lines for one requirement

Requirement: Experience building and deploying machine learning models

| Rank | Score | Resume line | Fair? |
|---|---|---|---|
| 1 | 0.23 | Fine-tuned a pretrained model for image classification using PyTorch | Yes, correct best match |
| 2 | 0.11 | Led a 5-member team for a college hackathon project | No, not relevant |
| 3 | 0.09 | Created a Python script to automate data cleaning with pandas | Partly relevant |
| 4 | 0.08 | Built an ESP32-based sensor system for motor monitoring | Not relevant |
| 5 | 0.04 | Deployed a FastAPI service in Docker | Should rank higher (deployment) |
| 6 | 0.02 | Won first prize in an inter-college quiz | Yes, correctly last |

Observations: the best and worst lines are found correctly, but the middle order is unreliable at these low scores. All scores are low because the requirement is short and generic while resume lines are long and specific. The requirement also has two parts (building and deploying), so splitting compound requirements into separate chunks should help.

## Takeaways

1. Good matches in different wording land around 0.5 to 0.6, and noise is below about 0.2.
2. Embeddings capture topic, not logic: negation scored 0.88. Note this as a limitation in the README.
3. Shared words can inflate scores: the Java island line (0.41) scored higher than a real ML classifier bullet (0.31).
4. Soft skills score low (0.29) even when they are a clear match, so give them little weight.
5. Use the best match per requirement, not an average over all resume lines, because most lines are irrelevant to any one requirement.
6. Embeddings alone are not enough, which is why the skill-dictionary check (Day 4) is part of the design.

## Calibration idea for Day 6

The planned bounds were lo=0.20 and hi=0.60. The best Part 2 match was only 0.23, which would scale to almost 0 out of 100 with lo=0.20. Start with lo about 0.05 to 0.10 and hi about 0.55, then tune with the Week 3 evaluation set.
