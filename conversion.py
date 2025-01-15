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
        "protocol" : "rip"
    },
    {
        "hostname": "Routeur2",
        "interfaces": [
            {"name": "GigabitEthernet1/0", "ip": "2001:1:1:1::2", "area":"0", "process-id":"1"},
            {"name": "GigabitEthernet2/0", "ip": "2001:1:1:2::2", "area":"3", "process-id":"2"},
            {"name" : "Loopback0", "ip" : "2002:2:2:2::2", "area":"55", "process-id":"410"}
        ],
        "routes": [
            {"destination": "0.0.0.0", "mask": "0.0.0.0", "next_hop": "192.168.2.254"}
        ],
        "protocol" : "ospf"
    }
]

giga = ["GigabitEthernet1/0", "GigabitEthernet2/0", "GigabitEthernet3/0"]

# Fonction pour générer la configuration d'un routeur
def generer_configuration(routeur):
    config = []
    config.append("!\n!\n!\nversion 15.2\service timestamps debug datetime msec\nservice timestamps log datetime msec")
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
    if routeur['protocol']=="rip":
        rip = 1
    elif routeur['protocol']=="ospf":
        ospf = 1

    # INTERFACES LOOPBACK  
    for interface in routeur['interfaces']:
        if interface['name'] == "Loopback0":
            adr_lb = interface['ip']  
            if ospf == 1:
                area = interface['area']  
                pro_id = interface ['process-id']
    config.append(f"!\ninterface Loopback0\n no ip address\n ipv6 address {adr_lb}/64\n ipv6 enable")
    if rip == 1:
        config.append(" ipv6 rip ng enable")
    if ospf == 1:
        config.append(f" ipv6 ospf {pro_id} area {area}")

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
            for interface in routeur['interfaces']:
                if interface['name'] == i:
                    adrip = interface['ip']
            config.append(f" ipv6 address {adrip}/64 \n ipv6 enable")
            if rip == 1:
                config.append(" ipv6 rip ng enable")
            if ospf == 1:
                for interface in routeur['interfaces']:
                    if interface['name'] == i:
                        area = interface['area']
                        pro_id = interface['process-id']
                        config.append(f" ipv6 ospf {pro_id} area {area}")
        else:
            config.append(f"!\ninterface {i}\n no ip adress \n shutdown \n negotiation auto")

    # for route in routeur['routes']:
    #     config.append(f"ip route {route['destination']} {route['mask']} {route['next_hop']}")
    config.append("!")
    return "\n".join(config)

# Génération des fichiers de configuration
for routeur in routeurs:
    filename = f"{routeur['hostname']}.cfg"
    with open(filename, "w") as file:
        file.write(generer_configuration(routeur))

print("Fichiers de configuration générés avec succès.")
