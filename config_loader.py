import json

CONFIG_PATH = 'config.json'

def load_config():
    """Loads the extraction patterns from config.json.

    Returns:
        dict: The 'extractor_patterns' mapping from the JSON file.

    Raises:
        FileNotFoundError: If the config file is not found.
        json.JSONDecodeError: If the config file is not valid JSON.
        KeyError: If the config file does not contain the required keys.
    """
    try:
        with open(CONFIG_PATH, 'r') as f:
            data = json.load(f)
            return data['extractor_patterns']
    except FileNotFoundError:
        print(f"Error: Configuration file '{CONFIG_PATH}' not found.")
        raise
    except json.JSONDecodeError as e:
        print(f"Error: The file '{CONFIG_PATH}' is poorly formatted: {e}")
        raise
    except KeyError as e:
        print(f"Error: The file '{CONFIG_PATH}' does not contain required key {e}.")
        raise
