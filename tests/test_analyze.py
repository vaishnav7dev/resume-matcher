import pytest

from app.matcher import analyze, calibrate

RESUME = """\
Built REST APIs in Python and deployed them with Docker
Trained a classifier on sensor data and evaluated it with F1-score
Fine-tuned a pretrained model for image classification using PyTorch
"""


def test_calibrate_maps_bounds_to_zero_and_one():
    assert calibrate(0.10, lo=0.10, hi=0.55) == 0.0
    assert calibrate(0.55, lo=0.10, hi=0.55) == 1.0
    assert calibrate(0.90, lo=0.10, hi=0.55) == 1.0  # clipped at the top
    assert calibrate(0.00, lo=0.10, hi=0.55) == 0.0  # clipped at the bottom


def test_calibrate_midpoint():
    assert calibrate(0.325, lo=0.10, hi=0.55) == pytest.approx(0.5)


def test_resume_against_itself_scores_near_100():
    result = analyze(RESUME, RESUME)
    assert result["score"] >= 99
    assert result["missing_skills"] == []


def test_unrelated_job_scores_low():
    jd = (
        "Manage a restaurant kitchen and train catering staff\n"
        "Prepare menus and order fresh ingredients every week"
    )
    assert analyze(RESUME, jd)["score"] < 30


def test_skills_matched_and_missing():
    jd = "We need strong Python programming skills and experience with Kubernetes"
    result = analyze(RESUME, jd)
    assert "python" in result["matched_skills"]
    assert result["missing_skills"] == ["kubernetes"]


def test_jd_without_known_skills_uses_meaning_only():
    jd = "Looking for a curious person who enjoys solving difficult problems"
    result = analyze(RESUME, jd)
    assert result["coverage"] is None
    assert result["score"] == result["semantic"]


def test_weak_requirements_are_reported():
    jd = "Manage a restaurant kitchen and train catering staff"
    assert analyze(RESUME, jd)["weak_requirements"]


def test_empty_text_raises_clear_error():
    with pytest.raises(ValueError):
        analyze("", "Experience with Python and Docker")
    with pytest.raises(ValueError):
        analyze(RESUME, "")


def test_result_has_expected_keys():
    result = analyze(RESUME, "Experience with Python and Docker and PyTorch models")
    assert 0 <= result["score"] <= 100
    assert set(result) == {
        "score", "semantic", "coverage", "matched_skills",
        "missing_skills", "weak_requirements", "matches",
    }
def test_every_match_has_a_fit_between_0_and_100():
    result = analyze(RESUME, "Experience with Python and Docker and PyTorch models")
    assert all(0 <= m["fit"] <= 100 for m in result["matches"])