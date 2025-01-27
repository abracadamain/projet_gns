import extraire_json
import json
from gen_ip import allocate_ip_add_routeur

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
    as_number = None
    for as_data in network_data["network"]["autonomous_systems"]:
        if any(router["hostname"] == r["hostname"] for r in as_data["routers"]):
            as_number = as_data["as_number"]
            break
    if as_number is None:
        raise ValueError(f"No matching autonomous system found for router: {router['hostname']}")
    # Initialize eBGP configuration structure
    ebgp_config = {
        "router": router["hostname"],
        "bgp": {
            "as_number": as_number,
            "neighbors": []
        }
    }

    router_ip_info = allocate_ip_add_routeur("network_intents.json", router["hostname"])

    # Process eBGP links
    for link in network_data["network"].get("ebgp_links", []):
        if router["hostname"] not in link:
            continue

        # Determine the neighbor's hostname
        if link[1] == router["hostname"]:
            neighbor_name = link[0]
        else:
            neighbor_name = link[1]


        #find the neighboring routers
        autonomous_systems = network_data["network"]["autonomous_systems"]
        all_routers = []
        for as_data in autonomous_systems:
            all_routers.extend(as_data["routers"])
        filtered_routers = filter(lambda r: r["hostname"] == neighbor_name, all_routers)
        neighbor_router = next(filtered_routers, None)



        
        # Find the neighbor's interface connected to this router
        interface=neighbor_router["interfaces"]
        filtered_interface = filter(lambda interface: interface["connected"] == router["hostname"],interface)
        neighbor_interface = next(filtered_interface, None)

        if not neighbor_interface:
            continue

        # Find the AS number of the neighbor
        neighbor_as = None

        for as_data in network_data["network"]["autonomous_systems"]:
            if any(router["hostname"] == neighbor_name for router in as_data["routers"]):
                neighbor_as = as_data["as_number"]
                break
        if neighbor_as is None:
            raise ValueError(f"No matching autonomous system found for hostname: {neighbor_name}")

        # Find the local interface connecting to the neighbor
        local_interface = None

        for interface in router["interfaces"]:
            if interface["connected"] == neighbor_name:
                local_interface = interface
                break

        if not local_interface:
            continue
        

        # Get neighbor's IP information
        neighbor_ip_info = allocate_ip_add_routeur("network_intents.json", neighbor_name)

        # Add neighbor configuration
        ebgp_config["bgp"]["neighbors"].append({
            "neighbor_name": neighbor_name,
            "ip_address": neighbor_ip_info[neighbor_interface["name"]],
            "remote_as": neighbor_as
        })

    return ebgp_config

data=extraire_json.read_intent_file("network_intents.json")
as_data=extraire_json.extract_as_data(data,"200")
router=extraire_json.extract_router_data(as_data, "R21") 
ebgp_config = generate_ebgp_config(router, data)
print(ebgp_config)