# Rapport comparatif — Kubeflow Pipelines vs Airflow (Lab 2)

**Binôme :** OualiRoudaina et Ghouil Nour · **Date :** 16/11/2026 · **Machine :** PC Windows 11, 12 processeurs logiques, 31 Go de RAM ; VM VirtualBox de 6 vCPU et 12 Go ·
**Dataset :** german-credit

## 1. Contexte

Le pipeline de scoring du Lab 1 (download, validate, prepare, train, evaluate, register) a été porté sur deux orchestrateurs : 6 steps dans les deux cas, sur le dataset german-credit (1000 lignes, 20 variables). Chaque step tourne dans un pod du cluster kind, à partir de la même image « projet » `scoring-pipeline:1.0.0` qui embarque le code du Lab 1. KFP et Airflow partagent donc le code métier, MLflow (runs et Model Registry) et `pipelines/stage.py`. Seul l'orchestrateur change.

## 2. Résultats quantitatifs

| Mesure | KFP | Airflow |
|---|---|---|
| Installation de zéro (min) | non mesuré proprement (perturbé par une saturation de la VM) | environ 8 (`make airflow`, dont l'extraction d'une image de 502 Mo) |
| Temps jusqu'au premier run réussi (min) | environ 12 (premier run, image à tirer) | environ 2 (image déjà présente) |
| Durée d'un run complet (min) | 7,5 à 9,5 (runs 2 à 4) | 2 (118 s) |
| Relance avec les mêmes paramètres (min) | 7,5 à 9,5, mais 3 pods exécutés au lieu de 5 (cache) | non applicable (pas de cache) |
| Hot-reload : modifier un step et voir le résultat (min) | non mesuré | non mesuré |
| Lignes de code propres à l'orchestrateur | 283 (`components.py` 193 + `scoring_pipeline.py` 90) | 71 (`scoring_dag.py`) |
| Mémoire consommée par l'outil (Go, `docker stats`) | non isolable : les nœuds kind (4,4 Go) hébergent aussi MLflow et le stockage | environ 1,9 (conteneurs Airflow) |

## 3. Analyse qualitative

### Developer experience

Le DAG Airflow est plus court (71 lignes contre 283) parce que `pipelines/stage.py` fait le transport des fichiers via S3. Avec KFP, les artefacts typés (Dataset, Model, Metrics) et leurs métadonnées s'affichent dans l'UI sans code supplémentaire, ce qui compense la verbosité. Tester sans cluster est possible dans les deux cas : `kfp.local` pour KFP, `python -m pipelines.stage … --workspace <dossier>` pour Airflow.

### Scaling

Chaque step est un pod dans les deux outils. KFP consomme 2 pods par step (un *driver* puis l'exécution) et ajoute le cache, qui évite de relancer les steps de données : 3 pods exécutés au lieu de 5. Airflow n'a qu'un pod par task, ce qui l'a rendu plus rapide sur ce petit pipeline. Cette explication reste une hypothèse : nous n'avons pas isolé la part des pods *driver* dans l'écart de durée.

### Debugging

KFP donne le lineage en un clic (artefact, step, run, métadonnées dont le md5 des données), et `kfp_run_id` relie un run MLflow à son run KFP. Avec Airflow, il faut parcourir les logs et le préfixe S3 du run. Dans les deux outils, les logs d'un step sont dans l'UI.

## 4. Recommandation

Choisir KFP quand le pipeline est centré sur l'ML : artefacts typés, métriques dans l'UI, cache pour itérer sur l'entraînement, lineage. Choisir Airflow pour des pipelines de données planifiés et hétérogènes, avec un écosystème de connecteurs, quand l'équipe le maîtrise déjà et que les fichiers volumineux ne circulent pas entre steps. Dans les deux cas, garder une image versionnée comme unité de livraison et un seul code métier.

## 5. Limites de la comparaison

Un seul dataset de 1000 lignes, un cluster kind local sur une VM, sans vrai cluster managé. Les durées incluent des effets de cache d'images et de charge de la VM (KFP a tourné pendant une période de saturation). Nous n'avons pas utilisé le KubernetesExecutor d'Airflow, pas mesuré le hot-reload, ni testé des steps en parallèle ou des échecs provoqués. Les chiffres sont indicatifs, pas des benchmarks.
