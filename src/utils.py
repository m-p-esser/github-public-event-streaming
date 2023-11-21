""" Misc utility functions """
import re

from dotenv import dotenv_values, find_dotenv


def load_env_vars() -> dict:
    """Load environment variables from file and store as dict"""
    base_env_file = find_dotenv(
        filename="base.env", raise_error_if_not_found=True, usecwd=True
    )
    env_vars = dotenv_values(base_env_file)

    env_file = find_dotenv(filename=".env", raise_error_if_not_found=True, usecwd=True)
    environment = dotenv_values(env_file)  # dev, test or prod
    env_vars.update(environment)
    if len(environment) > 0:
        env_vars.update(environment)
    return env_vars


def pascal_case_to_lower_case_with_hyphen(word: str) -> str:
    """EventType -> event-type"""
    word_list = re.findall("[A-Z][^A-Z]*", word)
    word_list_lowercase = [w.lower() for w in word_list]
    word_lowercase_hyphen = "-".join(word_list_lowercase)
    return word_lowercase_hyphen


if __name__ == "__main__":
    env_vars = load_env_vars()
    print(env_vars)
