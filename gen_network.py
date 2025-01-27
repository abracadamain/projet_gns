import extraire_json
import gen_ip

def gen_address_network():
    '''
    Récupère toutes les adresses réseau
    '''
    data=extraire_json.read_intent_file("network_intents.json")
    address_network = []
    for ausys in data["network"]["autonomous_systems"]:
        for router in ausys["routers"]:
            dict_ip = gen_ip.allocate_ip_add_routeur("network_intents.json", router["hostname"])
            for address in dict_ip:
                if address != "Loopback0":
                    add_net = dict_ip[address][:-5]
                    if add_net not in address_network:
                        address_network.append(add_net)
    return address_network