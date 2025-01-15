def generate_ebgp_config(router: dict, network_data: dict) -> dict:
    """
    Generates eBGP configuration for a router in a structured dictionary format.

    Args:
        router (dict): The router for which to generate eBGP configuration.
        network_data (dict): Full network data containing AS and eBGP link information.

    Returns:
        dict: eBGP configuration as a dictionary.
    """
    # Find the AS number of the router
    as_number = next(
        as_data["as_number"]
        for as_data in network_data["network"]["autonomous_systems"]
        if router["hostname"] in [r["hostname"] for r in as_data["routers"]]
    )

    # Initialize eBGP configuration structure
    ebgp_config = {
        "router": router["hostname"],
        "bgp": {
            "as_number": as_number,
            "neighbors": []
        }
    }

    # Process eBGP links
    for link in network_data["network"].get("ebgp_links", []):
        # Check if the router is part of this link
        if router["hostname"] in link:
            # Determine the neighbor's hostname
            if link[1] == router["hostname"]:
                neighbor_name = link[0]
            else:
                neighbor_name = link[1]

            # Find the neighbor router's details
            neighbor_router = next(
                r for as_data in network_data["network"]["autonomous_systems"]
                for r in as_data["routers"]
                if r["hostname"] == neighbor_name
            )

            # Find the neighbor's interface connected to this router
            neighbor_interface = next(
                iface for iface in neighbor_router["interfaces"]
                if iface["connected"] == router["hostname"]
            )

            # Find the AS number of the neighbor
            neighbor_as = next(
                as_data["as_number"]
                for as_data in network_data["network"]["autonomous_systems"]
                if neighbor_name in [r["hostname"] for r in as_data["routers"]]
            )

            # Add neighbor configuration
            ebgp_config["bgp"]["neighbors"].append({
                "ip_address": neighbor_interface["ip_address"],
                "remote_as": neighbor_as
            })

    return ebgp_config
