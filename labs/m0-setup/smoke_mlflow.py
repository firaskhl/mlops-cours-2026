#!/usr/bin/env python3
"""Smoke test MLflow : création d'un run avec un artefact."""

import mlflow
import os

# Configuration depuis .env
mlflow.set_tracking_uri(os.getenv("MLFLOW_TRACKING_URI", "http://localhost:5000"))

# Créer une expérience "smoke-test" (mich hello-mlops!)
experiment_name = "smoke-test"
try:
    experiment_id = mlflow.create_experiment(experiment_name)
except Exception:
    experiment_id = mlflow.get_experiment_by_name(experiment_name).experiment_id

mlflow.set_experiment(experiment_name)

# Run avec run_name="hello-mlops" (mich smoke-test!)
with mlflow.start_run(run_name="hello-mlops"):
    mlflow.log_param("test", "smoke")
    mlflow.log_metric("accuracy", 0.42)  # Metric accuracy = 0.42
    
    # Créer un fichier hello.txt
    artifact_file = "/tmp/hello.txt"
    with open(artifact_file, 'w') as f:
        f.write("Hello from MLflow smoke test!\n")
    
    # Log artifact
    mlflow.log_artifact(artifact_file)
    os.unlink(artifact_file)
    
    print("✅ MLflow run créé avec succès!")
    print(f"   Experiment: {experiment_name}")
    print(f"   Run: hello-mlops")
    print(f"   Run ID: {mlflow.active_run().info.run_id}")
