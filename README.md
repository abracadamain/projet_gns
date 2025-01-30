# Projet GNS - Pauline IGUE, Jingwen SHEN, Zoé FEUILLOY
### TAF :
* modifier gen_ip pour avoir le même sous réseau pour les 2 routeurs connectés localement mais dans des AS différents DONE V
* enlever IGP sur interface de bordure (sur le lien inter AS) DONE V
* ajouter loopback ibgp sur gns3 DONE V
* ajouter loopback dans script selon les nv fichiers de config
* tester les fichiers de config sur gns3

* modifier fichier intents pour 14 routeurs
* ligne 22 gen_ip : adapter le num du network correspondant au lien inter AS (quand on mettra 14 routeurs) ET ligne 61 conversion.py idem
* tester avec 14 routeurs

* nettoyer le code (print, imports, orga fonctions, ...)
* policies ospf en bonus

Loopback : 
Pour RX1 
 neighbor 2002:1:2:2::2 remote-as 11
 neighbor 2002:1:2:2::2 update-source Loopback0
 neighbor 2002:1:3:3::3 remote-as 11
 neighbor 2002:1:3:3::3 update-source Loopback0