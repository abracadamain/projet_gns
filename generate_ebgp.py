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
'''data=extraire_json.read_intent_file("network_intents.json")
router=extraire_json.extract_router_data()'''
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