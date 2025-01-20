import extraire_json
import json
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
            # Find the AS number of the neighbor
            autonomous_systems = network_data["network"]["autonomous_systems"]
            neighbor_as = None
            for as_data in autonomous_systems:
                router_hostnames = []
                for router in as_data["routers"]:
                    router_hostnames.append(router["hostname"])
                if neighbor_name in router_hostnames:
                    neighbor_as = as_data["as_number"]
                    break
            # Add neighbor configuration
            ebgp_config["bgp"]["neighbors"].append({
                "neighbor_name": neighbor_name, 
                "ip_address": neighbor_interface.get("ip_address", ""),
                "remote_as": neighbor_as
                
            })

    return ebgp_config
data=extraire_json.read_intent_file("network_intents.json")
as_data=extraire_json.extract_as_data(data,200)
router=extraire_json.extract_router_data(as_data, "R21") 
ebgp_config = generate_ebgp_config(router, data)
print(ebgp_config)
'''network_data = {
    "network": {
        "autonomous_systems": [
            {
                "as_number": 100,
                "routers": [
                    {
                        "hostname": "R11",
                        "interfaces": [
                            {"name": "GigabitEthernet1/0", "ip_address": "2001:1:1::1", "network": "2001:1:1::/64", "connected": "R21"},
                            {"name": "Loopback0", "ip_address": "2001:100::1", "network": "2001:100::1/128", "connected": None}
                        ]
                    }
                ]
            },
            {
                "as_number": 200,
                "routers": [
                    {
                        "hostname": "R21",
                        "interfaces": [
                            {"name": "GigabitEthernet1/0", "ip_address": "2001:2:2::1", "network": "2001:2:2::/64", "connected": "R11"},
                            {"name": "Loopback0", "ip_address": "2001:200::1", "network": "2001:200::1/128", "connected": None}
                        ]
                    }
                ]
            }
        ],
        "ebgp_links": [
            ["R11", "R21"]
        ]
    }
}
router = {
    "hostname": "R11",
    "interfaces": [
        {"name": "GigabitEthernet1/0", "ip_address": "2001:1:1::1", "network": "2001:1:1::/64", "connected": "R21"},
        {"name": "Loopback0", "ip_address": "2001:100::1", "network": "2001:100::1/128", "connected": None}
    ]
}
# 调用 generate_ebgp_config 函数
ebgp_config = generate_ebgp_config(router, network_data)
print(ebgp_config)
'''