from app.parser import clean_text, split_chunks


def test_clean_text_collapses_spaces():
    assert clean_text("a   b\t c") == "a b c"


def test_split_on_bullets():
    text = "• Built a REST API using FastAPI\n• Trained a classifier on sensor data"
    assert split_chunks(text) == [
        "Built a REST API using FastAPI",
        "Trained a classifier on sensor data",
    ]


def test_wrapped_line_is_joined():
    text = "• Built a REST API using FastAPI and\ndeployed it with Docker"
    assert len(split_chunks(text)) == 1


def test_short_fragments_dropped():
    assert split_chunks("Python\nSQL\nEDUCATION") == []


def test_sentences_are_split():
    text = "Built a REST API with FastAPI. Deployed it using Docker containers."
    assert len(split_chunks(text)) == 2