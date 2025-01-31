from sagemaker.sklearn.estimator import SKLearn
from sagemaker import get_execution_role
import os
import json
import boto3

def training():
    # Specifica la regione per SageMaker e S3
    region = os.environ.get("AWS_REGION", "us-east-1")  # Puoi cambiare 'us-west-2' con la regione che desideri

    sm_boto3 = boto3.client("sagemaker", region_name=region)  # Aggiungi la regione
    s3_client = boto3.client("s3", region_name=region)  # Aggiungi la regione

    if os.environ.get("MODEL_BUCKET_URI") is None:
        print("Using default model bucket")
    s3_bucket = os.environ.get("MODEL_BUCKET_URI") if os.environ.get("MODEL_BUCKET_URI") else "s3://model-remote-repository-cefriel"
    if os.environ.get("MODEL_FOLDER") is None:
        print("Using default model folder")
    s3_prefix = os.environ.get("MODEL_FOLDER") if os.environ.get("MODEL_FOLDER") else "gruppo-1/model"
    
    FRAMEWORK_VERSION = "1.2-1"

    if os.environ.get("SCRIPT") is None:
        print("Using default script")
    script = os.environ.get("SCRIPT") if os.environ.get("SCRIPT") else "random_forest_regressor.py"
    n_estimators = os.environ.get("N_ESTIMATORS") if os.environ.get("N_ESTIMATORS") else 100
    
    sklearn_estimator = SKLearn(
        entry_point=script,
        role=get_execution_role(),
        instance_count=1,
        instance_type="ml.m5.large",
        framework_version=FRAMEWORK_VERSION,
        base_job_name="Custom-sklearn",
        hyperparameters={
            "n_estimators": n_estimators,     #100
            "random_state": 0,
        },
        use_spot_instances=True,
        max_wait=7200,
        max_run=3600,
        output_path=f"{s3_bucket}/{s3_prefix}",
    )
    
    sklearn_estimator.fit(wait=True)
    sklearn_estimator.latest_training_job.wait(logs="None")
    artifact = sm_boto3.describe_training_job(
        TrainingJobName=sklearn_estimator.latest_training_job.name
    )["ModelArtifacts"]["S3ModelArtifacts"]
    outputs = {"MODEL_URI":artifact, "MODEL_SCRIPT": script}
    print(outputs)
    json_data = json.dumps(outputs)
    
    output_bucket = os.environ.get("DATA_URI") if os.environ.get("DATA_URI") else "data-remote-repository-cefriel"
    output_path = os.environ.get("DATA_URI") if os.environ.get("DATA_URI") else "gruppo-1/outputs/model_artifacts"+ script[:-3] +".json"
    
    s3_client.put_object(
        Bucket=output_bucket,       
        Key=output_path,      
        Body=json_data,
        ContentType="application/json"  # Set correct content type
    )

training()
