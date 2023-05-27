Var API UK Electricity forecasting




Dans le cadre du cursus MLops via l’organisme de formation DataScientest, pour la promotion de Janvier 2023, nous avons été sollicités pour réaliser un projet.
L'objectif de cette formation est de rendre les data scientists opérationnels dans la production et le déploiement de modèles.
Notre projet porte sur un modèle VAR, que nous avons le plaisir de vous présenter.
Le modèle VAR pour Vector Autoregression est un modèle de séries temporelles qui permet de prédire plusieurs variables dans le temps.


Objectif
L’objectif de ce projet est de créer une application web à partir d’un modèle de forecasting VAR dont le dataset porte sur la consommation d'électricité au Royaume-Uni entre 2009 et 2023.
Notre modèle VAR, un algorithme multivarié, permet de prédire à la fois la demande nationale d’électricité en Grande-Bretagne pour une période selectionnée, puis toutes les autres variables qui ont été données pour s'adapter au modèle.

Pour en savoir plus sur le modèle VAR, vous pouvez lire cet excellent article : 
datascientest.com/le-modele-var






Les outils d’ingénierie des données utilisés pour notre application

Le développement de cette application nous a permis d’exploiter l’ensemble des outils ci-dessous, liés à l'ingénierie des données :

- Programmation avancée avec Python
- Bash Linux
- Versionnement du code avec Git et GitHub
- Tests unitaires
- Sécurisation et création d'API avec FastAPI
- Conteneurisation avec Docker
- Automatisation avec AirFlow et MLFlow
- Service de cloud computing : Google Cloud Platform

Concrètement, le modèle de prédiction VAR est déployé à l'aide de FastAPI et de Docker.
L’industrialisation de notre modèle time series se fait sur Google Cloud Platform et via IHM.
De ce fait, nous avons déployé cette solution clé en main sur le Cloud, avec ce lien publique pour se connecter :

Notre application hébergée sur le cloud GCP, est composée de différents micro-services FastAPI conteneurisés avec Docker.
Un container unique déploie toute l'API.
Nous avons créé une interface WEB Front pour notre API. Cette interface interactive permet aux utilisateurs finaux d'utiliser l’outil de manière intuitive, via différentes features répondant aux besoins métiers.














Clarification des dossiers sur GitHub
Le code complet est open-source, vous pouvez le consulter ou même le télécharger sur notre dépôt GitHub.
https://github.com/gambitl/Var_API_UK_Electricity_forecasting.git

.idea : regroupe les fichiers xml & iml
dataset : historic_demand_2009_2023_noNaN
fichier_pre_api : comprend la sauvegarde de notre modèle « modele_var_projet_mle_21032023 » puis les scripts de modélisation et predict
web_app : regroupe l’ensemble des sous dossiers de l’application web :
.la database,
.les templates html,
.les fichiers statics,
.la sauvegarde de notre modèle « modele_var_projet_mle_21032023 »,
.app : centralise tous les scripts (main, predict, dataviz, about, ipynb_checkpoints)
main.py : fichier classé dans le dossier web_app/app et à partir duquel on lance notre application
requirements : liste des packages utilisés

Présentation de l’application
Retrouvez toutes les informations concernant ce projet sur le lien « ………… »
Plus précisément, vous y trouverez :
Une introduction au contexte
Une exploration statistique qui permet de sélectionner une durée et d'afficher le graphique associé, ou de visualiser l'effet de certaines caractéristiques sur la cible (demande nationale).
Une application interactive des prédictions de la consommation d’électricité en fonction du nombre de période que l’on souhaite prédire (une période = une demi-heure)
Les prédictions d’un ensemble de variable selon notre modèle VAR
Des informations complémentaires à propos de notre projet
Explore the dataset
Le dataset sur lequel repose notre application, a été sélectionné sur Kaggle.
Il provient du National Grid ESO qui est l'opérateur du système électrique pour la Grande-Bretagne.
Ce gestionnaire du réseau électrique a recueilli des informations sur la demande d'électricité en Grande-Bretagne depuis 2009. L'ensemble de données est mis à jour deux fois par heure, ce qui représente 48 entrées par jour.

Cet ensemble de données est donc idéal pour les prévisions de séries temporelles.
Sur la page « Explore the dataset » de notre application, vous pouvez sélectionner une durée et afficher le graphique associé, ou visualiser l'effet de certaines caractéristiques sur la cible (demande nationale).


Test Unitaire

Sur les pages principales de l’application :
- La page d’accueil
- Le dataviz
- Les prédictions
- About this project

 
Sur la qualité des données du dataset :
- Inspection du dataset de base
- Standardisation des données :
.variable au bon type,
.contrôle des valeurs manquantes,
.valeurs nulles,
.erreur de placement des virgules,
.les espaces,
.les arrondis

- Mesure du degré de pertinence des variables sélectionnées en fonction notamment de leur distribution

 
Sur les valeurs statistiques du dataset :
- Afficher les données statistiques
- Contrôler si existence valeur aberrante pour les variables
- Afficher la distribution de la variable sondée
- Contrôler valeur négative éventuelle et justification
- Ajout valeur aberrante dans une variable pour tester le degré de sensibilité
- Testing via l'automated testing avec pytest

Cloud GCP


Prédictions
L’application developpé permet de réaliser des prédictions.

Etant donné que notre modèle est un "VAR", un algorithme multivarié, il ne prédit pas seulement la demande nationale pour une période donnée, mais aussi toutes les autres variables qui ont été données pour s'adapter au modèle.

Sur notre application, vous devez indiquer le nombre de périodes que vous souhaitez prédire (une période = une demi-heure).

Équipe
Projet supervisé par Alban de DataScientest
Julien PROST | julienprost71@gmail.com
Victor DI STEFANO | victordistefano2@gmail.com
Jérémy LAVERGNE | jeremy.lav2009@gmail.com

Check out our LinkedIn profiles, links below
Jérémy                                                                  Julien                                                             Victor                                                            
