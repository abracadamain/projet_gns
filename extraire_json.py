import json

def read_intent_file(filepath: str) -> dict:
    """
    Reads the JSON intent file and returns it as a Python dictionary.

    Args:
        filepath (str): Path to the JSON file.

    Returns:
        dict: Parsed JSON data as a dictionary.
    """
    with open(filepath, 'r') as file:
        data = json.load(file)
    return data