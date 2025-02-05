from gen_ip import allocate_ip_add_routeur
def generate_ibgp_config(router: dict, as_data: dict) -> str:
    """
    Generates iBGP configuration for a router within an AS.

    Args:
        router (dict): The router for which to generate iBGP configuration.
        as_data (dict): AS data containing all routers and iBGP links.

    Returns:
        str: iBGP configuration as a string.
    """
    as_number = as_data["as_number"] 

    ibgp_config = {
        "router": router["hostname"],
        "bgp": {
            "as_number": as_number,
            "neighbors": []
        }
    }
    # Configure iBGP neighbors
    for n_routeur in as_data["routers"]:
        if n_routeur["hostname"] != router["hostname"]:
            neighbor_name = n_routeur["hostname"]
            
            neighbor_ip_info=allocate_ip_add_routeur("network_intents.json",neighbor_name)    

            filtered_keys = [key for key in neighbor_ip_info.keys() if key != 'Loopback0']
            interface_name=filtered_keys[0]
                
            ibgp_config["bgp"]["neighbors"].append({
                "neighbor_name": neighbor_name, 
                "neighbor_ip":neighbor_ip_info[interface_name],
                "remote_as": as_data["as_number"],
                "update_source": neighbor_ip_info["Loopback0"],
            
            })

    return ibgp_config