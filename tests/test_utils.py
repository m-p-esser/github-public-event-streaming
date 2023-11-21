import pathlib
from unittest.mock import mock_open, patch

from src.utils import load_env_vars, pascal_case_to_lower_case_with_hyphen


def test_load_env_vars_successfully():
    m = mock_open()
    with patch("__main__.open", m, create=False):
        test_file_name = "test.env"
        with open(test_file_name, "w") as f:
            f.write("ENV=dev")
            # Repeat as the functions expects two env files
        env_vars = load_env_vars(["test.env", "test.env"])
        print(env_vars)
        assert len(env_vars) > 0
        assert isinstance(env_vars, dict)
        pathlib.Path.unlink(pathlib.Path(test_file_name))


def test_pascal_case_to_lower_case_with_hyphen_sucessfully():
    modified_word = pascal_case_to_lower_case_with_hyphen("EventType")
    assert modified_word == "event-type"
