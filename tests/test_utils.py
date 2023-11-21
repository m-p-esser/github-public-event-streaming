from src.utils import load_env_vars


def test_load_env_vars_successfully():
    env_vars = load_env_vars()
    assert len(env_vars) > 0
    assert isinstance(env_vars, dict)


if __name__ == "__main__":
    test_load_env_vars_successfully()
