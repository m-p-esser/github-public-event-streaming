""" Misc utility functions """
from dotenv import dotenv_values


def load_env_vars() -> dict:
    """Load environment variables from file and store as dict"""
    env_vars = dotenv_values("./make/base.env")
    environment = dotenv_values("./make/.env")  # dev, test or prod
    env_vars.update(environment)
    if len(environment) > 0:
        env_vars.update(environment)
    return env_vars


if __name__ == "__main__":
    env_vars = load_env_vars()
    print(env_vars)
