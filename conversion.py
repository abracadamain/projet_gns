from gen_ip import allocate_ip_add_routeur
from generate_ibgp import generate_ibgp_config
from generate_ebgp import generate_ebgp_config
from itertools import chain
from extraire_json import read_intent_file
from gen_network import gen_address_network

def generer_configuration(routeur, dict_ip, routing_protocol):
    giga = ["GigabitEthernet1/0", "GigabitEthernet2/0", "GigabitEthernet3/0"]
    config = []
    config.append("!\n!\n!\nversion 15.2\nservice timestamps debug datetime msec\nservice timestamps log datetime msec")
    config.append(f"!\nhostname {routeur['hostname']}\n!")
    config.append("boot-start-marker\nboot-end-marker\n!\n!\n!\nno aaa new-model\nno ip icmp rate-limit unreachable\nip cef")
    config.append("!\n!\n!\n!\n!")
    config.append("no ip domain lookup\nipv6 unicast-routing\nipv6 cef\n!\n!")
    config.append("multilink bundle-name authenticated")
    config.append("!\n!\n!\n!\n!\n!\n!")
    config.append("ip tcp synwait-time 5")
    config.append("!\n!\n!\n!\n!\n!\n!")

    rip = 0
    ospf = 0
    if routing_protocol=="RIP":
        rip = 1
    elif routing_protocol=="OSPF":
        ospf = 1

    # INTERFACES LOOPBACK  
    adr_lb = dict_ip['Loopback0']
    if ospf == 1:
        area = 0
        process_id = routeur['hostname'][1:]
    config.append(f"!\ninterface Loopback0\n no ip address\n ipv6 address {adr_lb}\n ipv6 enable")
    if rip == 1:
        config.append(" ipv6 rip ng enable")
    if ospf == 1:
        config.append(" ipv6 ospf " + process_id + f" area {area}")

    # INTERFACE FAST ETHERNET
    config.append("!\ninterface FastEthernet0/0 \n no ip address \n duplex full")
    for interface in routeur['interfaces']:
        if "FastEthernet" in interface['name']:
            found = True
            config.append(f" ipv6 address {dict_ip[interface['name']]}")
            config.append(" ipv6 enable")
            if rip == 1:
                config.append(" ipv6 rip ng enable")
            break
        else :
            found = False
    if not found:
        config.append(" ipv6 enable")

    # INTERFACES GIGABIT
    int=[]
    for interface in routeur['interfaces']:
        int.append(interface['name'])
    for i in giga:
        if i in int :
            config.append(f"!\ninterface {i}")
            config.append(f" no ip address\n negotiation auto")
            adrip = dict_ip[i]
            config.append(f" ipv6 address {adrip} \n ipv6 enable")
            for interface in routeur['interfaces']:
                if interface['name'] == i:
                    if interface["network"] != "5" : #si ce n'est pas une interface de bordure (entre 2 AS)
                        if rip == 1:
                            config.append(" ipv6 rip ng enable")
                        if ospf == 1:
                            area = 0 #on met la même area pour toutes les interfaces de tous les routeurs
                            process_id = routeur["hostname"][1:] 
                            config.append(f" ipv6 ospf {process_id} area {area}")
        else:
            config.append(f"!\ninterface {i}\n no ip address \n shutdown \n negotiation auto")
    
    return config

def ajouter_bgp(config, dict_ibgp, dict_ebgp, bordure, as_number):
    # BGP
    address_network = gen_address_network(as_number)
    config.append("!\n!")
    num = dict_ibgp['router'][1:]
    rt_id = num + "." + num + "." + num + "." + num
    as_number = dict_ibgp['bgp']['as_number']
    config.append(f"router bgp {as_number}\n bgp router-id {rt_id}\n bgp log-neighbor-changes\n no bgp default ipv4-unicast")
    for neighbor in chain(dict_ibgp['bgp']['neighbors'], dict_ebgp['bgp']['neighbors']):
        n_as = neighbor['remote_as']
        if 'update_source' in neighbor :
            n_loopback = neighbor['update_source'][:-4]
            config.append(f" neighbor {n_loopback} remote-as {n_as}")
            config.append(f" neighbor {n_loopback} update-source Loopback0")

    config.append(" !\n address-family ipv4\n exit-address-family\n !")
    config.append(" address-family ipv6")
    if bordure : #si c'est un routeur de bordure (entre 2 AS)
        for add in address_network:
            config.append(f"  network {add}/64")
    for neighbor in chain(dict_ibgp['bgp']['neighbors'], dict_ebgp['bgp']['neighbors']): 
        n_ip = neighbor['neighbor_ip'][:-3]
        config.append(f"  neighbor {n_ip} activate")
        if 'update_source' in neighbor :
            n_loopback = neighbor['update_source'][:-4]
            config.append(f"  neighbor {n_loopback} activate")

    config.append(" exit-address-family")
    return config

def gen_fin_config(config, routeur, routing_protocol):
    # FIN
    config.append("!\nip forward-protocol nd\n!\n!\nno ip http server\nno ip http secure-server\n!")

    if routing_protocol == "RIP":
        config.append("ipv6 router rip ng\n redistribute connected")
    if routing_protocol == "OSPF":
        process_id = routeur["hostname"][1:]
        rt_id = process_id + "." + process_id + "." + process_id + "." + process_id
        config.append(f"ipv6 router ospf {process_id} \n router-id {rt_id}")
        
    config.append("!\n!\n!\n!\n!")
    config.append("control-plane\n!\n!")
    config.append("line con 0\n exec-timeout 0 0\n privilege level 15\n logging synchronous\n stopbits 1")
    config.append("line aux 0\n exec-timeout 0 0\n privilege level 15\n logging synchronous\n stopbits 1")
    config.append("line vty 0 4\n login")
    config.append("!\n!\nend")

    config.append("!")
    return "\n".join(config)

data = read_intent_file("network_intents.json")
routeurs_bordure = data["network"]["ebgp_links"][0]
for ausys in data["network"]["autonomous_systems"] :
    for routeur in ausys["routers"] :
       bordure = routeur["hostname"] in routeurs_bordure #si le routeur est en bordure d'AS
       dict_ip = allocate_ip_add_routeur("network_intents.json", routeur["hostname"])
       filename = f"test {routeur['hostname']}.cfg"
       dict_ibgp = generate_ibgp_config(routeur, ausys)
       dict_ebgp = generate_ebgp_config(routeur, data)

       with open(filename, "w") as file:
           conf = generer_configuration(routeur, dict_ip, ausys["routing_protocol"])
           conf = ajouter_bgp(conf, dict_ibgp, dict_ebgp, bordure, ausys["as_number"])
           file.write(gen_fin_config(conf, routeur, ausys["routing_protocol"]))

print("Fichiers de configuration générés avec succès.")
