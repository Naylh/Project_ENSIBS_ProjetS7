# Auteur/Email :  
CHAPRON Lucas / chapron.e2105151@etud.univ-ubs.fr

# Contenu du dossier

## Data (visible après exécution du parser)

Les données d'entrées pour l'analyse des plannings. Ce sont des fichiers .ics qui est un format contenant l'ensemble des événements importés via "export agenda" > Générer une URL.

## parserProjet.py

Fichier source permettant de lancer une analyse sur un seul fichier .ics et ainsi créer les fichiers json nécessaires à l'application WEB.

## makeExcel.py

Fichier source permettant de créer un fichier excel correspondant à l'occupation des salles sur une période donnée.

## parser.js et routine.py
Fichier permettant d'exécuter le parser de manière régulière. Non fonctionnel

# Getting started

En l'état n'est utilisable qu'avec l'application WEB mais si vous modifiez les informations nécessaire dans les fichiers python pour le délier vous pourrez l'utiliser.

Allez dans le dossier racine /app et installez les dépendances de python :

`pip install -r requirements.txt`

Enfin démarrez le script de création des fichiers JSON avec la commande suivante pour connaître leur fonctionnement :

`python3 parser.py -h`

Démarrez le script de création du fichier Excel avec la commande suivante pour connaître leur fonctionnement : 

`python3 makeExcel.py -h`
