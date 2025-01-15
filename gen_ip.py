import json

def allocate_ip_add_routeur(f_intents, routeur_hostname) :
    """Alloue les adresses IP d'un routeur pour chaque interface, incluant le loopback.
    Return : dictionnaire des adresses IP allouées"""
    with open(f_intents, "r") as f :
        data = json.load(f)

    dict_ip = {}
    fin = False
    for i in range (len(data["autonomous_systems"])) :
        aut_sys = data["autonomous_systems"][i]
        routers = aut_sys["routers"]
        for j in range(len(routers)) :
            router = routers[j]
            if router["hostname"] == routeur_hostname :
                num_hostname = router["hostname"][1:] # On enlève le premier caractère R
                dict_ip["Loopback0"] = aut_sys["ip_range"][:-3] + num_hostname + "/128"
                for k in range(len(router["interfaces"])) :
                    interface = router["interfaces"][k]
                    adresse = aut_sys["ip_range"][:-4] + interface["network"] + ":" + num_hostname + "/64"
                    dict_ip[interface["name"]] = adresse
                break
                fin = True
        if fin :
            break # On a trouvé le routeur
    
    return dict_ip
                    
#allocate_ip_add_routeur("network_intents.json", "R12")
                