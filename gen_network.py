import extraire_json
import gen_ip

def gen_address_network(as_number):
    '''
    Récupère toutes les adresses réseau d'un AS
    '''
    data=extraire_json.read_intent_file("network_intents.json")
    address_network = []
    for ausys in data["network"]["autonomous_systems"]:
        if ausys["as_number"] == as_number:
            for router in ausys["routers"]:
                dict_ip = gen_ip.allocate_ip_add_routeur("network_intents.json", router["hostname"])
                for address in dict_ip:
                    if address != "Loopback0":
                        for interface in router["interfaces"]:
                            bordure1 = [interface["connected"], router["hostname"]] in data["network"]["ebgp_links"] 
                            bordure2 = [router["hostname"], interface["connected"]] in data["network"]["ebgp_links"]
                            if interface["name"] == address and not (bordure1 or bordure2): #si ce n'est pas un lien eBGP
                                add_net = dict_ip[address][:-5]
                                if add_net not in address_network:
                                    address_network.append(add_net)
    return address_network