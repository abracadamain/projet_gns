def generate_rip_config(router: dict) -> str:
    """
    Generates RIP configuration for a router.

    Args:
        router (dict): Dictionary containing router details (hostname, interfaces, etc.).

    Returns:
        str: The RIP configuration as a string.
    """
    config_lines = []

    # Start RIP configuration
    config_lines.append("router rip")
    config_lines.append(" version ng")  # Use RIPng for better support
    config_lines.append(" no auto-summary")  # Disable automatic summarization

    # Add networks based on router's interfaces
    for interface in router.get("interfaces", []):
        # Add only physical interfaces to RIP (excluding loopbacks)
        if not interface["name"].startswith("Loopback"):
            network = interface["network"].split('/')[0]  # Extract the network address
            config_lines.append(f" network {network}")

    # Return the full configuration as a single string
    return "\n".join(config_lines)
