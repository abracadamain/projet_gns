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
def extract_as_data(intent_data: dict, as_number: int) -> dict:
    """
    Extracts information about a specific Autonomous System (AS) from the intent file.

    Args:
        intent_data (dict): Full intent data as a dictionary.
        as_number (int): The AS number to extract.

    Returns:
        dict: Data for the specified AS, or an empty dictionary if not found.
    """
    for as_data in intent_data.get("network", {}).get("autonomous_systems", []):
        if as_data["as_number"] == as_number:
            return as_data
    return {}
def extract_router_data(as_data: dict,hostname: str) -> list:
    """
    Extracts all router details from the AS data.

    Args:
        as_data (dict): Data for a specific Autonomous System.

    Returns:
        list: A list of router dictionaries, or an empty list if no routers are found.
    """
    for router in as_data.get("routers", []):
        if router["hostname"] == hostname:
            return router
    return {} 
