def generate_ibgp_config(router: dict, as_data: dict) -> str:
    """
    Generates iBGP configuration for a router within an AS.

    Args:
        router (dict): The router for which to generate iBGP configuration.
        as_data (dict): AS data containing all routers and iBGP links.

    Returns:
        str: iBGP configuration as a string.
    """
    config_lines = []
    as_number = as_data["as_number"] 

    ibgp_config = {
        "router": router["hostname"],
        "bgp": {
            "as_number": as_number,
            "neighbors": []
        }
    }

    # Configure iBGP neighbors
    for link in as_data.get("ibgp_links", []):
        if router["hostname"] in link:
            if link[1]==router["hostname"]:
                neighbor_name = link[0]
            else:
                neighbor_name = link[1]
            neighbor_router = next(r for r in as_data["routers"] if r["hostname"] == neighbor_name)
            for iface in neighbor_router["interfaces"]:
                if iface["name"] == "Loopback0":
                    loopback = iface
                    break
            ibgp_config["bgp"]["neighbors"].append({
                "neighbor_ip": loopback["ip_address"],
                "remote_as": as_number,
                "update_source": "Loopback0"
            })

    return ibgp_config