import json
from gen_ip import allocate_ip_add_routeur
# Exemple de script Python pour générer un fichier de configuration .cfg

# Définition des paramètres pour chaque routeur
routeurs = [
    {
        "hostname": "Routeur1",
        "interfaces": [
            {"name": "GigabitEthernet3/0", "ip": "2001:1:1:1::1"},
            {"name": "GigabitEthernet1/0", "ip": "2001:1:1:2::1"},
            {"name" : "Loopback0", "ip" : "2002:1:1:1::1"}
        ],
        "routes": [
            {"destination": "0.0.0.0", "mask": "0.0.0.0", "next_hop": "192.168.1.254"}
        ],
        "protocol" : "rip",
        "routeur-id" : "1.1.1.1",
        "AS":"11",
        "connected":"Routeur2"
    },
    {
        "hostname": "Routeur2",
        "interfaces": [
            {"name": "GigabitEthernet1/0", "ip": "2001:1:1:1::2", "area":"0"},
            {"name": "GigabitEthernet2/0", "ip": "2001:1:1:2::2", "area":"1"},
            {"name" : "Loopback0", "ip" : "2002:2:2:2::2", "area":"2"}
        ],
        "routes": [
            {"destination": "0.0.0.0", "mask": "0.0.0.0", "next_hop": "192.168.2.254"}
        ],
        "protocol" : "ospf",
        "process-id" : "2",
        "routeur-id" : "2.2.2.2",
        "AS":"22"
    }
]

giga = ["GigabitEthernet1/0", "GigabitEthernet2/0", "GigabitEthernet3/0"]

# Fonction pour générer la configuration d'un routeur
def generer_configuration(routeur, dict_ip, routing_protocol):
    giga = ["GigabitEthernet1/0", "GigabitEthernet2/0", "GigabitEthernet3/0"]
    config = []
    config.append("!\n!\n!\nversion 15.2\service timestamps debug datetime msec\nservice timestamps log datetime msec")
    config.append(f"!\nhostname {routeur["hostname"]}\n!")
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
        process_id = routeur["hostname"][1:]
    config.append(f"!\ninterface Loopback0\n no ip address\n ipv6 address {adr_lb}\n ipv6 enable")
    if rip == 1:
        config.append(" ipv6 rip ng enable")
    if ospf == 1:
        config.append(" ipv6 ospf " + process_id + f" area {area}")

    # INTERFACE FAST ETHERNET
    config.append("!\ninterface FastEthernet0/0 \n no ip address \n duplex full")
    for interface in routeur['interfaces']:
        if "FastEthernet" in interface['name']:
            config.append(f" ipv6 address {interface['ip']}")
    config.append(" ipv6 enable")
    if rip == 1:
        config.append(" ipv6 rip ng enable")

    # INTERFACES GIGABIT
    int=[]
    for interface in routeur['interfaces']:
        int.append(interface['name'])
    for i in giga:
        if i in int :
            config.append(f"!\ninterface {i}")
            config.append(f" no ip address\n negotiation auto")
            adrip = dict_ip[i]
            config.append(f" ipv6 address {adrip}/64 \n ipv6 enable")
            if rip == 1:
                config.append(" ipv6 rip ng enable")
            if ospf == 1:
                for interface in routeur['interfaces']:
                    if interface['name'] == i:
                        area = 0 #on met la même area pour toutes les interfaces de tous les routeurs
                        process_id = routeur["hostname"][1:] 
                        config.append(f" ipv6 ospf {process_id} area {area}")
        else:
            config.append(f"!\ninterface {i}\n no ip adress \n shutdown \n negotiation auto")

    return "\n".join(config)

def ajouter_bgp(config,routeurs):
    # BGP
    config.append("!\n!")
    rt_id = routeur['routeur-id']
    as_number = routeur['AS']
    config.append(f"routeur bgp {as_number}\n bgp router-id {rt_id}\n bgp log-neighbor-changes\n no bgp default ipv4-unicast")
    config.append(" NEIGHBOR @IP REMOTE-AS AS_N°")
    config.append("!\naddress-family ipv4\nexit-address-family\n!")
    config.append("address-family ipv6\n NETWORK ::/64\n NEIGHBOR @IP ACTVATE \nexit-address-family")

    # FIN
    config.append("!\nip forward-protocol nd\n!\n!\nno ip http server\nno ip http secure-server\n!")

    if rip == 1:
        config.append("ipv6 router rip ng\n redistribute connected")
    if ospf == 1:
        config.append(f"ipv6 router ospf {routeur['process-id']} \n router-id {routeur['routeur-id']}")
        
    config.append("!\n!\n!\n!\n!")
    config.append("control-plane\n!\n!")
    config.append("line con 0\n exec-timeout 0 0\n privilege level 15\n logging synchronous\n stopbits 1")
    config.append("line aux 0\n exec-timeout 0 0\nprivilege level 15\nlogging synchronous\n stopbits 1")
    config.append("line vty 0 4\n login")
    config.append("!\n!\nend")

    config.append("!")
    return "\n".join(config)

# Génération des fichiers de configuration
'''
for routeur in routeurs:
    filename = f"{routeur['hostname']}.cfg"
    with open(filename, "w") as file:
        file.write(generer_configuration(routeur))
'''

with open("network_intents.json", "r") as f :
    data = json.load(f)

for ausys in data["network"]["autonomous_systems"] :
    for routeur in ausys["routers"] :
       dict_ip = allocate_ip_add_routeur("network_intents.json", routeur["hostname"])
       filename = f"test {routeur['hostname']}.cfg"
       with open(filename, "w") as file:
           file.write(generer_configuration(routeur, dict_ip, ausys["routing_protocol"]))

print("Fichiers de configuration générés avec succès.")
