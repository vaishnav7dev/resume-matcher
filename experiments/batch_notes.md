# Batch report notes

Settings used: weights 0.6 meaning / 0.4 skills, calibration lo 0.25 and hi 0.65
(confirm these match matcher.py).

## 1. Results

| JD | My gut rating (1 to 5) | Score | Meaning | Skills coverage | Missing skills |
| --- | --- | --- | --- | --- | --- |
| jd1 | 4 | 71.9 | 61.5 | 88% | 1 (tensorflow) |
| jd2 | 2 | 63.4 | 47.3 | 88% | 1 (tensorflow) |
| jd3 | 3 | 45.1 | 47.4 | 42% | 7 |
| jd_unrelated | 1 | 11.7 | 11.7 | n/a | 0 |

Self-check (resume vs itself): 100.0
Spearman agreement with my gut ratings: 0.80 (only 4 JDs, so a rough hint)

## 2. Answers

1. **Tool ranking vs my ranking.** Tool: jd1 > jd2 > jd3 > unrelated.
   Mine: jd1 > jd3 > jd2 > unrelated. Only jd2 and jd3 are swapped.
2. **Highest and lowest.** Highest 71.9 (jd1), lowest 11.7 (unrelated), a spread of 60 points.
3. **Skills I added to skills.json.** a/b testing,data preprocessing,llm evaluation
4. **Lines that hurt the score. Data mining and preprocessing
5. **Scores that felt wrong.** jd2 (63.4) scored above jd3 (45.1), but I rated jd3 higher.
   The meaning scores are almost equal (47.3 vs 47.4), so the gap comes entirely from skills
   coverage (88% vs 42%). When I rated, I was evaluating the responsibilities , they were more promising and apt for the resume 

## 3. What worked

- Self-check scores 100, and the unrelated JD scores lowest.
- Negated skills are ignored: tensorflow is correctly missing for jd1 and jd2.
- Calibration gives a wide spread (11.7 to 71.9).

## 4. Problems found and ideas to test in Week 3

| Finding | Evidence | Idea to test |
| --- | --- | --- |
| Generic soft-skill lines are flagged as gaps | "Willingness to learn..." fit 16, "Ability to learn and experiment quickly" fit 3 | Do not flag them, or give them lower weight |
| Related skills count as separate gaps | claude, gpt and openai are 3 missing skills on jd3 | Group them as one "llm apis" skill |
| Role heading wins on keywords | One "Machine Learning Intern" line is the best match for many requirements | Down-weight heading-like lines |
| JD title and intro count as requirements | Title line scored fit 100 | Use only requirement or responsibility sections |
| Resume contact line used as a match | "Location" matched the contact line | Skip contact lines |
| Section labels glued to bullets | "What you will do• ..." stayed in one chunk | Fixed by the inline-bullet step; rerun to confirm |

## 5. Limitations for the README

- The match is against the JD as written, not against how much the candidate wants the role.
- Negation handling is a simple rule and can misfire inside long sentences.
- Skills not in the dictionary are invisible to the coverage score.
- Raw similarity grows with resume length, so calibration depends on the resume.
- Scores come from 4 JDs, so they are a sanity check and not an accuracy claim.