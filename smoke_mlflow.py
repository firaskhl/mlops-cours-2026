import mlflow

# Configure l'URI de tracking vers le serveur MLflow local
mlflow.set_tracking_uri("http://localhost:5000")
mlflow.set_experiment("hello-mlops")

with mlflow.start_run():
    mlflow.log_param("greeting", "hello")
    mlflow.log_metric("accuracy", 1.0)

    # Crée un artefact hello.txt
    with open("hello.txt", "w") as f:
        f.write("Hello MLflow from MLOps Lab 0!")

    mlflow.log_artifact("hello.txt")
    print("Run MLflow exécuté et artefact enregistré avec succès !")
