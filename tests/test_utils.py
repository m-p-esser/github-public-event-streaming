from src.utils import load_env_vars, pascal_case_to_lower_case_with_hyphen


def test_load_env_vars_successfully():
    env_vars = load_env_vars()
    assert len(env_vars) > 0
    assert isinstance(env_vars, dict)


def test_pascal_case_to_lower_case_with_hyphen_sucessfully():
    modified_word = pascal_case_to_lower_case_with_hyphen("EventType")
    assert modified_word == "event-type"
