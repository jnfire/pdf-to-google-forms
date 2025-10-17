
import json

CONFIG_PATH = 'config.json'

def load_config():
    """Loads the extraction patterns from config.json."""
    try:
        with open(CONFIG_PATH, 'r') as f:
            return json.load(f)['extractor_patterns']
    except FileNotFoundError:
        print(f"Error: Configuration file '{CONFIG_PATH}' not found.")
        exit()
    except (json.JSONDecodeError, KeyError):
        print(f"Error: The file '{CONFIG_PATH}' is poorly formatted.")
        exit()
