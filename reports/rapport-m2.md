# Rapport comparatif — Kubeflow Pipelines vs Airflow (Lab 2)

**Binôme :** Ghofrane Khadhar · Nour Garali · **Date :** 18/11/2026 · **Machine :** VM Ubuntu 24.04 sous VMware (4 CPU, 12 Go RAM, cluster kind à 3 nœuds) ·
**Dataset :** Statlog German Credit (`dataset.yaml`)

## 1. Contexte

Nous avons migré le pipeline DVC du Lab 1 (credit scoring, 1000 lignes, 20 variables, cible good/bad) vers deux orchestrateurs : un pipeline Kubeflow Pipelines (`scoring-pipeline`) et un DAG Airflow (`scoring_dag`). Les deux comptent 6 steps : ingest, validate, prepare, train, evaluate, register. Chaque step est un pod du cluster kind qui exécute le même code du Lab 1 dans la même image `localhost:5001/scoring-pipeline:1.0.0`. MLflow trace les runs (`launched_by=kfp` ou `airflow`) et le Model Registry reçoit le modèle. Les trois orchestrateurs (DVC, KFP, Airflow) ont produit le même résultat : ROC AUC 0.809405.

## 2. Résultats quantitatifs

| Mesure | KFP | Airflow |
|---|---|---|
| Installation de zéro (min) | non mesuré (réseau ~1 Mo/s) | non mesuré (plusieurs essais, coupures TLS) |
| Temps jusqu'au premier run réussi (min) | non mesuré | non mesuré |
| Durée d'un run complet (min) | non mesuré | environ 2,3 (23:11:31 à 23:13:53) |
| Relance avec les mêmes paramètres | 3 steps sur 6 servis par le cache (train toujours ré-exécuté) | pas de cache natif : tout est ré-exécuté |
| Hot-reload (min) | non mesuré | non mesuré |
| Lignes de code propres à l'orchestrateur | 282 (components.py 193 + scoring_pipeline.py 89) | 70 (scoring_dag.py) |
| Mémoire consommée par l'outil | non mesurée (cluster kind environ 2,4 Go, partagé avec MLflow et le stockage) | environ 1,96 Go (docker stats) |

## 3. Analyse qualitative

### Developer experience

KFP demande plus de code (composants typés, entrées et sorties déclarées) mais donne en échange des artefacts typés, un graphe lisible et un cache. Airflow est plus court : un DAG de 70 lignes dont les tasks lancent `pipelines.stage` via le KubernetesPodOperator. En contrepartie, Airflow ne transporte aucun fichier : chaque task recopie le dossier de travail depuis et vers S3, et seules de petites valeurs passent par XCom.

### Scaling

Dans les deux cas, un step est un pod avec des ressources déclarées (`set_memory_limit` côté KFP, `container_resources` côté Airflow). Côté KFP, nous avons ajouté retries, timeouts et contrôle du cache. Airflow est simple à lancer sur le poste, mais ses 7 conteneurs occupent environ 2 Go de RAM en permanence, alors que Kubeflow vit dans le cluster.

### Debugging

Les deux outils affichent les logs d'un step dans leur UI. KFP rend le lineage visible en un clic (artefact, step, run, `kfp_run_id` dans MLflow). Avec Airflow, il faut parcourir le préfixe S3 du run et lire les logs. Pendant le lab, la plupart des incidents venaient du réseau (ImagePullBackOff, DNS, TLS handshake timeout) et non des orchestrateurs. Le rejeu local d'une task Airflow (`python -m pipelines.stage ... --workspace /tmp/ws`) s'est révélé très pratique.

## 4. Recommandation

Nous choisirions KFP pour des pipelines de ML où le lineage des artefacts, le cache et les entrées/sorties typées comptent, sur un cluster Kubernetes déjà disponible. Nous choisirions Airflow pour orchestrer des workflows variés (données, ETL, planification cron) dans une équipe qui dispose déjà d'Airflow, à condition d'accepter de gérer soi-même le passage des fichiers via S3.

## 5. Limites de la comparaison

Nous avons travaillé sur un seul poste (VM 12 Go) avec un réseau lent et instable, ce qui fausse les temps d'installation et de premier run, d'où les mentions non mesuré. Les durées KFP n'ont pas été relevées et le hot-reload n'a pas été mesuré. KFP n'a pas été testé sur un cluster managé, ni Airflow avec le KubernetesExecutor. Le dataset est petit (1000 lignes) : cela ne dit rien du passage à l'échelle réel ni du parallélisme.
