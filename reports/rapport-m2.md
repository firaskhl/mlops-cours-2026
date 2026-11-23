# Rapport M2 — Orchestration de pipelines ML avec KFP et Airflow

## 1. Contexte

L'objectif de ce laboratoire est de mettre en place et de comparer deux solutions d'orchestration de workflows de Machine Learning : Kubeflow Pipelines (KFP) et Apache Airflow.

Le projet consiste à développer un pipeline de scoring de crédit permettant de traiter un jeu de données, de préparer les données, d'entraîner un modèle, d'évaluer ses performances et d'enregistrer le modèle obtenu.

L'environnement technique repose sur Kubernetes avec Kind pour simuler un cluster local. Les composants principaux utilisés sont Kubeflow Pipelines pour l'orchestration ML, Apache Airflow pour l'orchestration alternative, MLflow pour le suivi des expériences et des modèles, Docker pour la construction et l'exécution de l'image du pipeline, ainsi qu'un stockage S3 compatible pour le partage des fichiers entre les tâches.

L'objectif est également de garantir la reproductibilité des exécutions et de comparer les avantages et les limites des deux approches.

## 2. Résultats

Le pipeline de scoring a été décomposé en six étapes principales :

1. **Ingest** : récupération des données nécessaires au traitement.
2. **Validate** : vérification de la conformité des données.
3. **Prepare** : préparation des données avant l'entraînement.
4. **Train** : entraînement du modèle de Machine Learning.
5. **Evaluate** : évaluation des performances du modèle.
6. **Register** : enregistrement ou promotion du modèle dans MLflow.

L'image Docker du pipeline a été construite et publiée dans le registre local sous le nom `localhost:5001/scoring-pipeline:1.0.0`. Les composants KFP ont été définis et le pipeline a été compilé puis téléversé dans Kubeflow Pipelines.

Les premières exécutions KFP ont permis de vérifier le fonctionnement de l'orchestration et l'intégration avec MLflow. Les expériences sont suivies dans MLflow, avec le tag `launched_by=kfp`, et le modèle est enregistré sous le nom `scoring-model`.

Une seconde orchestration a été mise en place avec Airflow. Le DAG `scoring_dag` reprend les six étapes du pipeline et utilise des KubernetesPodOperator pour exécuter chaque étape dans un pod Kubernetes. Les données intermédiaires sont partagées via le stockage S3, tandis que XCom permet de transmettre les petites informations nécessaires entre les tâches, notamment l'identifiant du run MLflow.

Résultats finaux à renseigner après validation :

- Nombre de runs KFP réussis : [nombre observé].
- Exécution du DAG Airflow : [réussie ou non].
- Nombre de tâches Airflow réussies : [nombre sur six].
- Run MLflow Airflow avec le tag `launched_by=airflow` : [présent ou absent].
- Contrôles finaux : [nombre de contrôles réussis sur 18].

## 3. Analyse

Kubeflow Pipelines est particulièrement adapté aux workflows de Machine Learning. Il permet de structurer les traitements en composants réutilisables, de gérer les dépendances entre les étapes et de suivre les exécutions. Il facilite également la gestion des artefacts et la reproductibilité des expériences.

Airflow propose une approche plus générale de l'orchestration. Son DAG permet de représenter clairement les dépendances entre les tâches et son interface facilite le suivi de leur état et la consultation des journaux d'exécution.

Dans cette implémentation, KubernetesPodOperator permet à Airflow de lancer les étapes du pipeline dans des pods indépendants. Le partage des données via S3 et la transmission des informations légères via XCom permettent de conserver une séparation entre les tâches.

Les deux outils peuvent donc répondre à des besoins complémentaires : KFP est orienté vers les workflows ML, tandis qu'Airflow offre une orchestration plus généraliste et flexible.

## 4. Recommandation

Pour un projet principalement consacré au Machine Learning, Kubeflow Pipelines constitue un choix pertinent grâce à son intégration avec les composants ML, la gestion des artefacts et le suivi des exécutions.

Airflow est intéressant lorsque le projet nécessite d'orchestrer plusieurs types de traitements, notamment des tâches de préparation, d'intégration et de traitement de données qui dépassent le seul cycle de vie d'un modèle ML.

Le choix doit donc dépendre des besoins du projet, de l'infrastructure disponible et des compétences de l'équipe. Dans certains environnements, les deux solutions peuvent être utilisées conjointement.

## 5. Limites

Les expérimentations ont été réalisées sur un environnement local avec Kind. Celui-ci permet de simuler un cluster Kubernetes, mais ne représente pas entièrement les contraintes d'un environnement de production distribué.

Les ressources matérielles disponibles limitent également le nombre de services pouvant fonctionner simultanément. L'exécution d'Airflow, de Kubeflow Pipelines, de MLflow et des pods Kubernetes peut entraîner une consommation importante de mémoire et de ressources CPU.

Le stockage S3 utilisé dans ce laboratoire est une solution locale compatible S3. Il ne permet donc pas de mesurer toutes les caractéristiques d'un service de stockage cloud réel.

Enfin, les résultats de performance obtenus dans cet environnement ne peuvent pas être généralisés à une infrastructure de production. Une validation supplémentaire sur un cluster distant, avec des ressources adaptées et des données représentatives, serait nécessaire.
