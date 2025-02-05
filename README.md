# Projet GNS - Pauline IGUE, Jingwen SHEN, Zoé FEUILLOY
## Fichier d'intention
Fichier JSON qui décrit l'architcture voulue du réseau, dans lequel sont listés tous les routeurs, triés par AS. Dans notre cas on a un réseau composé de 14 routeurs, divisé en deux AS (un qui utilise RIP et l'autre OSPF). Ces deux AS sont reliés en BGP par deux routeurs de bordure chacun. Le fichier décrit les informations suivantes :
* les AS
* les plages d'adresses ip pour chaque AS
* les protocoles IGP et EGP
* les routeurs avec leurs interfaces, networks et liens physiques
* les liens eBGP

## Comment configurer le réseau décrit par le fichier d'intention sur GNS3?
* créer l'architecture correspondante au fichier sur GNS3 
* lancer le code conversion.py
* les fichiers cfg de configuration pour chaque routeur sont générés 
* drag and drop chaque fichier cfg dans le routeur correspondant sur GNS3
* le réseau est configuré 

## Fonctionalités supportées :
* génération automatique des adresses ip dont loopback
* mise en place des protocoles de routage interne et externe

## Fonctionalités non supportées :
* policies
* telnet bot