# Projet GNS - Pauline IGUE, Jingwen SHEN, Zoé FEUILLOY

On crée sur GNS3 un réseau composé de 14 routeurs, divisés en deux AS (un qui utilise RIP et l'autre OSPF). Ces deux AS sont reliés par BGP. 
En lançant le code conversion.py, on génère les fichiers de configuration pour chaque routeur à partir du fichier JSON d'intentions, dans lequel sont listés tous les routeurs, triés par AS. Dans ce fichier on a : 
* les AS
* les protocoles
* les plages d'adresses ip
* les routeurs avec leurs interfaces, networks et liens physiques
* les liens eBGP

