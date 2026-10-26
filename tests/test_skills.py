from app.skills import extract_skills


def test_alias_maps_to_canonical_name():
    skills = extract_skills("Used sklearn and PyTorch for the model")
    assert {"scikit-learn", "pytorch"} <= skills


def test_cpp_is_detected():
    assert "c++" in extract_skills("Experienced in C++ and Python")


def test_java_is_not_javascript():
    skills = extract_skills("Built a frontend in JavaScript")
    assert "javascript" in skills
    assert "java" not in skills


def test_no_partial_word_match():
    # "ml" lives inside "html" but must not count as machine learning
    assert "machine learning" not in extract_skills("Built pages in HTML")


def test_postgresql_is_not_plain_sql():
    skills = extract_skills("Stored data in PostgreSQL")
    assert "postgresql" in skills
    assert "sql" not in skills


def test_case_insensitive_and_empty():
    assert "python" in extract_skills("PYTHON")
    assert extract_skills("") == set()

def test_negated_skill_is_not_counted():
    assert "tensorflow" not in extract_skills("Have not worked with TensorFlow or JAX yet")


def test_negation_does_not_leak_into_next_sentence():
    skills = extract_skills("Never used Spark. Built models in PyTorch.")
    assert "pytorch" in skills


def test_plain_algorithms_is_not_a_skill():
    assert "data structures and algorithms" not in extract_skills("ML concepts and algorithms")