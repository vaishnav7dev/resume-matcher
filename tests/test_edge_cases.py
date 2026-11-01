import pytest

from app.matcher import analyze
from app.parser import split_chunks

RESUME = """\
Built REST APIs in Python and deployed them with Docker
Trained a classifier on sensor data and evaluated it with F1-score
Fine-tuned a pretrained model for image classification using PyTorch
"""


def test_one_sentence_jd_still_works():
    result = analyze(RESUME, "Experience with Python and machine learning models")
    assert 0 <= result["score"] <= 100


def test_jd_pasted_as_one_block_is_split_into_chunks():
    jd = (
        "Build REST APIs using FastAPI • Train and evaluate machine learning models • "
        "Write unit tests with pytest for every new feature"
    )
    assert len(split_chunks(jd)) == 3


def test_blank_resume_gives_clear_error():
    with pytest.raises(ValueError, match="resume"):
        analyze("   \n  ", "Experience with Python and machine learning models")


def test_jd_with_only_short_lines_gives_clear_error():
    with pytest.raises(ValueError, match="job description"):
        analyze(RESUME, "Python\nSQL\nDocker")


def test_same_input_gives_same_score():
    jd = "Experience with Python and machine learning models"
    assert analyze(RESUME, jd)["score"] == analyze(RESUME, jd)["score"]