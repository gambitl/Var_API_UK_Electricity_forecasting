# 📈 Projet de prédiction du prix du cours du gaz naturel au Royaume-Uni

Ce projet se focalise sur la mise en production d'un modèle de séries temporelles multivarié visant à prédire le prix du cours du gaz naturel au Royaume-Uni. Le modèle est réalisé en utilisant la librairie `statsmodels`.

## Architecture

Le projet est mis en production sur Google Cloud Platform (GCP) en utilisant les services suivants :

1. 📂 **Google Cloud Storage** : les données d'entraînement sont stockées dans un bucket Google Cloud Storage dédié.
2. 🐳 **API et container Docker** : le modèle est rendu accessible au public via une API hébergée dans un container Docker. Il expose une page HTML.
3. 🔨 **Google Cloud Build** : intégration continue et déploiement du container Docker grâce à Google Cloud Build.
4. ☁️ **Google Cloud Run** : déploiement du container Docker sur Google Cloud Run, permettant d'exécuter l'API.
5. 🎛️ **Google Cloud Composer** : le fichier Python du DAG Airflow, situé dans le dossier "dag_airflow" du projet, est utilisé pour ré-entraîner le modèle toutes les heures. Le DAG s'exécute sur la brique Google Cloud Composer.
6. 📊 **MLFlow** : toutes les métriques d'entraînement et les artefacts, tels que le modèle, sont sauvegardés et historisés en utilisant la librairie Python MLFlow. Les données de MLFlow sont stockées dans un autre bucket Google Cloud Storage dédié.
7. 🗄️ **PostgreSQL** : les données de MLFlow sont également sauvegardées dans une base de données PostgreSQL.
8. 💻 **Google Cloud Compute Engine** : la brique MLFlow s'exécute sur une machine virtuelle créée à l'aide de Google Cloud Compute Engine.

## Configuration et déploiement

1. 🚀 Créez un projet sur Google Cloud Platform et configurez les services nécessaires, tels que Google Cloud Build, Google Cloud Run et Google Cloud Composer.
2. 📦 Créez les buckets Google Cloud Storage nécessaires, l'un pour stocker les données d'entraînement et l'autre pour sauvegarder les sorties de MLFlow. Mettez à jour les chemins correspondants dans le code.
3. ⚙️ Configurez les paramètres spécifiques du projet, tels que les identifiants d'accès à GCP, les chemins vers les données d'entraînement, etc.
4. 🖥️ Créez une machine virtuelle sur Google Cloud Compute Engine et configurez l'environnement MLFlow.
5. 🗃️ Créez une base de données PostgreSQL pour stocker les données de MLFlow et configurez les paramètres de connexion dans le code.
6. 🔄 Mettez en place le DAG Airflow en important dans l'interface de Composer le fichier Python du DAG situé dans le dossier "dag_airflow" du projet.
7. 🚢 Construisez le container Docker grâce à la brique Google Cloud Build (vous pouvez configurez une CI automatique en liant votre repo GIT comme nous l'avons fait) et déployez-le sur Google Cloud Run.

## Documentation

La documentation détaillée sur la construction des différents services cloud et les démarches à suivre se trouve dans le dossier `docs` du projet. 📚
