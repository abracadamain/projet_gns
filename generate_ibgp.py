import extraire_json
import json
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
    config_lines = []
    as_number = as_data["as_number"] 

    ibgp_config = {
        "router": router["hostname"],
        "bgp": {
            "as_number": as_number,
            "neighbors": []
        }
    }
    router_ip_info = allocate_ip_add_routeur("network_intents.json", router["hostname"])
    # Configure iBGP neighbors
    for link in as_data.get("ibgp_links", []):
        if router["hostname"] in link:
            # Determine the neighbor's hostname
            if link[1] == router["hostname"]:
                neighbor_name = link[0]
            else:
                neighbor_name = link[1]
            
            routers = as_data["routers"]
            filtered_routers = filter(lambda r: r["hostname"] == neighbor_name, routers)
            neighbor_router = next(filtered_routers, None)
            
            interface_name = None
            for interface in router["interfaces"]:
                if interface["connected"]==neighbor_name:
                    interface_name=interface["name"] 
                    break
            if not interface_name:
                filtered_keys = [key for key in neighbor_ip_info.keys() if key != 'Loopback0']
                interface_name=filtered_keys[0]
            neighbor_ip_info=allocate_ip_add_routeur("network_intents.json",neighbor_name)    
                
            
            
            ibgp_config["bgp"]["neighbors"].append({
                "neighbor_name": neighbor_name, 
                "neighbor_ip":neighbor_ip_info[interface_name],
                "remote_as": as_data["as_number"],
                "update_source": neighbor_ip_info["Loopback0"],
            
            })

    return ibgp_config
data=extraire_json.read_intent_file("network_intents.json")
as_data=extraire_json.extract_as_data(data,100)
router=extraire_json.extract_router_data(as_data, "R11") 
ibgp_config = generate_ibgp_config(router, as_data)
print(ibgp_config)