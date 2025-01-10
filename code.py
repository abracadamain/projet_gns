# -*- coding: utf-8 -*-
"""
Created on Tue Jan  7 14:23:19 2025

@author: zfeui
"""

import json
import os

# from netmiko import ConnectHandler
# from nornir import InitNornir
# from napalm import get_network_driver

# import requests
# from gns3fy import Gns3Connector

# Charger les données JSON
def load_json(file_path):
    with open(file_path, 'r') as f:
        return json.load(f)

json_file = "network_intents.json"  # Nom du fichier JSON
data = load_json(json_file)  # Chargez le contenu du JSON


# Rechercher les routeurs d'un AS donné
def get_routers_by_as(data, as_number):
    for as_data in data["network"]["autonomous_systems"]:
        if as_data["as_number"] == as_number:
            return as_data["routers"]
    return []

# Récupérer la configuration BGP pour un AS donné
def get_bgp_config_by_as(data, as_number):
    for as_data in data["network"]["autonomous_systems"]:
        if as_data["as_number"] == as_number:
            return as_data.get("bgp", {})
    return {}

# Récupérer les informations de peering BGP entre deux AS
def get_bgp_peering(data, as1, as2):
    for peering in data["network"].get("bgp_peering", []):
        if (peering["as1"] == as1 and peering["as2"] == as2) or (peering["as1"] == as2 and peering["as2"] == as1):
            return peering["link"]
    return {}

# Rechercher les réseaux annoncés pour un AS donné
def get_advertised_networks(data, as_number):
    for as_data in data["network"]["autonomous_systems"]:
        if as_data["as_number"] == as_number:
            return as_data.get("bgp", {}).get("advertised_networks", [])
    return []

# Exemple d'utilisation
if __name__ == "__main__":
    # Charger les données JSON depuis un fichier
    json_file = "network_intents.json"  # Remplacer par le chemin du fichier JSON
    data = load_json(json_file)
    
    # Récupérer les routeurs pour l'AS1
    as1_routers = get_routers_by_as(data, 1)
    print("Routeurs dans AS1:")
    for router in as1_routers:
        print(f" - {router['hostname']}: {router['interfaces']}")

    # Récupérer la configuration BGP pour l'AS2
    as2_bgp_config = get_bgp_config_by_as(data, 2)
    print("\nConfiguration BGP pour AS2:")
    print(as2_bgp_config)

    # Obtenir les informations de peering entre AS1 et AS2
    peering_info = get_bgp_peering(data, 1, 2)
    print("\nPeering BGP entre AS1 et AS2:")
    print(peering_info)

    # Récupérer les réseaux annoncés pour l'AS1
    as1_networks = get_advertised_networks(data, 1)
    print("\nRéseaux annoncés pour AS1:")
    print(as1_networks)
