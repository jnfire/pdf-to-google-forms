import json

CONFIG_PATH = 'config.json'

def load_config():
    """Loads the configuration from config.json.

    Returns:
        dict: The configuration data from the JSON file.

    Raises:
        FileNotFoundError: If the config file is not found.
        json.JSONDecodeError: If the config file is not valid JSON.
    """
    try:
        with open(CONFIG_PATH, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Error: Configuration file '{CONFIG_PATH}' not found.")
        return {}
    except json.JSONDecodeError as e:
        print(f"Error: The file '{CONFIG_PATH}' is poorly formatted: {e}")
        raise
