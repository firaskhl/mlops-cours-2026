# Image projet pour les pipelines Kubeflow et Airflow
FROM python:3.12-slim

WORKDIR /app

# Installation des dépendances
COPY pipelines/requirements.txt /tmp/requirements.txt

RUN pip install --no-cache-dir --root-user-action=ignore \
    -r /tmp/requirements.txt \
    && pip install --no-cache-dir --root-user-action=ignore \
    --no-deps kfp==2.17.0

# Copie des configurations du projet
COPY dataset.yaml params.yaml ./

# Copie du code métier du Lab 1
COPY src/ src/

# Copie des modules d'orchestration
COPY pipelines/__init__.py pipelines/stage.py pipelines/

# Configuration Python
ENV PYTHONPATH=/app \
    DATASET_CONFIG=/app/dataset.yaml \
    PYTHONUNBUFFERED=1

ARG VERSION=dev

LABEL org.opencontainers.image.title="scoring-pipeline" \
      org.opencontainers.image.version="${VERSION}"
