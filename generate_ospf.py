def generate_ospf_config(router: dict, ospf_config: dict) -> dict:
    """
    Generates OSPF configuration for a router in a structured dictionary format.

    Args:
        router (dict): The router for which to generate OSPF configuration.
        ospf_config (dict): OSPF configuration containing process ID and area information.

    Returns:
        dict: OSPF configuration as a dictionary.
    """
   
    process_id = ospf_config["process_id"]

    ospf_data = {
        "router": router["hostname"],
        "ospf": {
            "process_id": process_id,
            "networks": []
        }
    }

   
    for interface in router.get("interfaces", []):
        network = interface["network"].split('/')[0]
        mask_bits = int(interface["network"].split('/')[1])
        if mask_bits <= 32:
            wildcard_mask = '.'.join(str(255 - int(octet)) for octet in network.split('.'))
        else:
            wildcard_mask = "0.0.0.0"
        area_id = ospf_config.get("areas", {}).get(interface["network"], 0)
        ospf_data["ospf"]["networks"].append({
            "network": network,
            "wildcard_mask": wildcard_mask,
            "area": area_id
        })

    return ospf_data
