# Auteur/Email :
CAYAMBO Vincent / cayambo.e2105488@etud.univ-ubs.fr  
CHAPRON Lucas / chapron.e2105151@etud.univ-ubs.fr  
HIDOUX Cassiopée / hidoux.1908932@etud.univ-ubs.fr  
HORLAVILLE Pierre / horlaville.2100726@etud.univ-ubs.fr  

# Réalisation
Parser - CHAPRON Lucas  
WEB - CAYAMBO Vincent / CHAPRON Lucas / HIDOUX Cassiopée / HORLAVILLE Pierre  
CAS - CAYAMBO Vincent

# Contenu du dossier

## db
Contient le docker pour le serveur de la base de données.

### init.sql
Contient le fichier d'initialisation de la base de données.

## excel (apparait après l'execution du parser)
Contient le fichier excel que l'utilisateur crée.

## .env
Variable d'environnement pour le docker-compose.

## app

### addons
Contient les fichiers décrivant le header et le footer du site web. 

### cas-ecole
Contient la configuration du cas de l'école

### css
Contient les fichiers css du site web.  

### images
Contient les images du site web.

### js
Contient les fichiers javascript du site web.

### json
Contient les fichiers json utile pour le site web.

### parser
Contient les fichiers python du parser. Voir le readme.md du dossier parser pour plus d'informations.

### www
Contient les fichiers html du site web.

### .env
Variable d'environnement pour la connexion à la base de données.

### app.py
Fichier principal du site web.

### Dockerfile
Fichier de configuration du docker pour le site web.

### requirements.txt
Fichier contenant les dépendances python du site web.

# Getting started
Le site web est disponible sous 2 façons différentes : 
- En local
- Via docker (uniquement si CAS héberger ailleurs que via docker -> pas fonctionnel en l'état)

## En local
### Prérequis
- Python 3.*
- Un serveur de base de données (MySQL, MariaDB, etc.)
- Un moyen de lancer d'exécuter des fichiers .sh

### Installation
- Cloner le projet
- Configurer votre serveur de base de données avec le fichier db/init.sql/bdplanning.sql
- Installer les dépendances python en se mettant dans le dossier /app et en exécutant la commande suivante : `pip install -r requirements.txt`
- Allez dans le dossier /app/cas-ecole
- Lancez la commande ``docker build --no-cache -t cas-ecole .``
- Exécutez ``sh unix_keygen.sh`` ou ouvrez``windows_keygen.sh`` en fonction de votre système d'exploitation
- Allez dans le dossier /app
- Lancer l'app.py ``python app.py``
- Se rendre à l'adresse ``http://localhost:8002``
- Utilisateurs autorisés(login:mdp)->hidoux.cassio.e0000001:cassio,chap.lucas.e0000002:lucas,horlaville.pierre.e0000003:pierre,cay.vincent.e0000004:vincent

## Via docker:
Pour lancer le site web, il faut installer docker et docker-compose.  
Pour installer docker, suivez les instructions sur le site officiel : https://docs.docker.com/engine/install/  
Pour installer docker-compose, suivez les instructions sur le site officiel : https://docs.docker.com/compose/install/  

### Build Unix (ne marche pas):
- Cloner le projet
- Changez les paramètres de connexion à la base de données dans le fichier app.py et parser.py
- Allez dans le dossier racine du projet
- Lancez la commande ``docker-compose up -d cas``
- Lancez la commande ``docker-compose up -d db``
- Lancez la commande ``docker-compose up app``
- Si vous avez une erreur de connexion à la base de données, faites ``Ctrl + C`` pour arrêter les dockers puis réexécutez la commande ``docker-compose up``
- Aller sur un navigateur à l'adresse ``http://localhost:8002``






