from app.matcher import semantic_match

RESUME = [
    "Built REST APIs using FastAPI and deployed them with Docker",
    "Won first prize in an inter-college quiz",
    "Trained a classifier on sensor data and evaluated it with F1-score",
]


def test_best_match_is_the_relevant_line():
    result = semantic_match(RESUME, ["Experience building REST APIs with FastAPI"])
    assert result[0]["best_match"] == RESUME[0]


def test_one_result_per_jd_chunk():
    jd = ["Experience with Python and FastAPI", "Knowledge of machine learning models"]
    assert len(semantic_match(RESUME, jd)) == 2


def test_identical_text_scores_near_one():
    line = "Built REST APIs using FastAPI"
    assert semantic_match([line], [line])[0]["score"] > 0.99


def test_empty_inputs_return_empty_list():
    assert semantic_match([], ["Experience with Python"]) == []
    assert semantic_match(RESUME, []) == []