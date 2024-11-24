import os
import yaml


def load_config(file_path: str = "config/config.yaml") -> dict:
    """
    Load configuration from a YAML file.

    Args:
        file_path (str): Path to the YAML configuration file.

    Returns:
        dict: Configuration dictionary.
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Configuration file not found: {file_path}")

    with open(file_path, "r") as file:
        config = yaml.safe_load(file)

    return config


def get_env_variable(key: str, default: str = None) -> str:
    """
    Retrieve an environment variable, with an optional default.

    Args:
        key (str): Environment variable name.
        default (str): Default value if the variable is not set.

    Returns:
        str: Value of the environment variable or default.
    """
    return os.getenv(key, default)
