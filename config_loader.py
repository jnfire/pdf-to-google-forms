import json

CONFIG_PATH = 'config.json'

def load_config():
    """Loads the extraction patterns from config.json.

    Returns:
        dict: The 'extractor_patterns' mapping from the JSON file.

    Exits with code 1 and prints a helpful message if the file is missing or malformed.
    """
    try:
        with open(CONFIG_PATH, 'r') as f:
            data = json.load(f)
            return data['extractor_patterns']
    except FileNotFoundError:
        print(f"Error: Configuration file '{CONFIG_PATH}' not found.")
        exit(1)
    except json.JSONDecodeError as e:
        print(f"Error: The file '{CONFIG_PATH}' is poorly formatted: {e}")
        exit(1)
    except KeyError as e:
        print(f"Error: The file '{CONFIG_PATH}' does not contain required key {e}.")
        exit(1)
