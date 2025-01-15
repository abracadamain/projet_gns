import extraire_json
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
'''
as_data = {
    "as_number": 100,
    "routers": [
        {
            "hostname": "R11",
            "interfaces": [
                {"name": "GigabitEthernet1/0", "ip_address": "2001:db8:1::1", "network": "2001:db8:1::/64", "connected": "R12"},
                {"name": "Loopback0", "ip_address": "2001:db8:100::1", "network": "2001:db8:100::1/128", "connected": None}
            ]
        },
        {
            "hostname": "R12",
            "interfaces": [
                {"name": "GigabitEthernet1/0", "ip_address": "2001:db8:1::2", "network": "2001:db8:1::/64", "connected": "R11"},
                {"name": "GigabitEthernet2/0", "ip_address": "2001:db8:2::1", "network": "2001:db8:2::/64", "connected": "R13"},
                {"name": "Loopback0", "ip_address": "2001:db8:100::2", "network": "2001:db8:100::2/128", "connected": None}
            ]
        },
        {
            "hostname": "R13",
            "interfaces": [
                {"name": "GigabitEthernet2/0", "ip_address": "2001:db8:2::2", "network": "2001:db8:2::/64", "connected": "R12"},
                {"name": "Loopback0", "ip_address": "2001:db8:100::3", "network": "2001:db8:100::3/128", "connected": None}
            ]
        }
    ],
    "ibgp_links": [["R11", "R12"], ["R12", "R13"], ["R11", "R13"]]
}
router = {
    "hostname": "R11",
    "interfaces": [
        {"name": "GigabitEthernet1/0", "ip_address": "2001:db8:1::1", "network": "2001:db8:1::/64", "connected": "R12"},
        {"name": "Loopback0", "ip_address": "2001:db8:100::1", "network": "2001:db8:100::1/128", "connected": None}
    ]
}
# 调用 generate_ibgp_config 函数
ibgp_config = generate_ibgp_config(router, as_data)
print(ibgp_config)
'''