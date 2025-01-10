from ipaddress import ip_network

def allocate_ip_addresses(as_data: dict, ip_range: str) -> dict:
    """
    Allocates IP addresses for physical interfaces and loopback interfaces in an AS.

    Args:
        as_data (dict): AS data containing routers and their interfaces.
        ip_range (str): IP range to allocate addresses from (e.g., "10.0.0.0/16").

    Returns:
        dict: Updated AS data with allocated IP addresses for interfaces.
    """
    # Parse the IP range
    network = ip_network(ip_range)
    physical_subnets = network.subnets(new_prefix=30)  # /30 for point-to-point physical links
    loopback_subnets = network.subnets(new_prefix=32)  # /32 for loopback interfaces

    # Allocate loopback addresses
    for router in as_data["routers"]:
        loopback_address = next(loopback_subnets).network_address
        router["interfaces"].append({
            "name": "Loopback0",
            "ip_address": str(loopback_address),
            "network": str(loopback_address) + "/32",
            "connected": None
        })

    # Allocate physical interface addresses
    for link in as_data.get("ibgp_links", []):
        router1_name, router2_name = link
        router1 = next(router for router in as_data["routers"] if router["hostname"] == router1_name)
        router2 = next(router for router in as_data["routers"] if router["hostname"] == router2_name)
        
        # Get the next /30 subnet for the link
        subnet = next(physical_subnets)
        ip1, ip2 = list(subnet.hosts())  # Two usable IPs in the /30 subnet

        # Assign IPs to the respective interfaces
        router1["interfaces"].append({
            "name": f"GigabitEthernet{len(router1['interfaces'])}/0",
            "ip_address": str(ip1),
            "network": str(subnet),
            "connected": router2_name
        })
        router2["interfaces"].append({
            "name": f"GigabitEthernet{len(router2['interfaces'])}/0",
            "ip_address": str(ip2),
            "network": str(subnet),
            "connected": router1_name
        })

    return as_data
as_data = {
    "as_number": 100,
    "routers": [
        {"hostname": "RX1", "interfaces": []},
        {"hostname": "RX2", "interfaces": []},
        {"hostname": "RX3", "interfaces": []}
    ],
    "ibgp_links": [
        ["RX1", "RX2"],
        ["RX2", "RX3"],
        ["RX3", "RX1"]
    ]
}

ip_range = "10.0.0.0/24"
print(allocate_ip_addresses(as_data,ip_range))