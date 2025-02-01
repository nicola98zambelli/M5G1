from sagemaker.sklearn.model import SKLearnModel
from time import gmtime, strftime
from sagemaker import get_execution_role
import os
import boto3
import json

def endpoint_creation(model_data = None, script = None):
    FRAMEWORK_VERSION = "1.2-1"
    
    model_name = "Custom-sklearn-model-" + strftime("%Y-%m-%d-%H-%M-%S", gmtime())
    script = os.environ.get("SCRIPT") if os.environ.get("SCRIPT") else "random_forest_regressor.py"
    output_bucket = os.environ.get("OUTPUT_BUCKET") if os.environ.get("OUTPUT_BUCKET") else "data-remote-repository-cefriel"
    output_path = os.environ.get("OUTPUT_PATH") if os.environ.get("OUTPUT_PATH") else "gruppo-1/outputs/model_artifacts_"+ script[:-3] +".json"
    s3_client = boto3.client("s3")
    response = s3_client.get_object(Bucket=output_bucket, Key=output_path)
    content = response['Body'].read().decode('utf-8')
    training_output = json.loads(content)

    print(training_output)
    if model_data is None:
        model_data = training_output["MODEL_URI"]

    model = SKLearnModel(
        name=model_name,
        model_data= model_data,   #model uri
        role=get_execution_role(),
        entry_point="random_forest_regressor.py",
        framework_version=FRAMEWORK_VERSION,
    )
    
    endpoint_name = "Custom-sklearn-model-" + strftime("%Y-%m-%d-%H-%M-%S", gmtime())
    print("EndpointName={}".format(endpoint_name))
    
    predictor = model.deploy(
        initial_instance_count=1,
        instance_type="ml.m4.xlarge",
        endpoint_name=endpoint_name,
    )
    
    outputs = {"ENDPOINT_NAME":endpoint_name, "SCRIPT": script}
    print(outputs)
    
    json_data = json.dumps(outputs)
    
    # Initialize S3 client
    s3_client = boto3.client("s3")

    endpoint_bucket = os.environ.get("ENDPOINT_DATA_URI") if os.environ.get("ENDPOINT_DATA_URI") else "data-remote-repository-cefriel"
    endpoint_path = os.environ.get("ENDPOINT_OUTPUT_PATH") if os.environ.get("ENDPOINT_OUTPUT_PATH") else "gruppo-1/outputs/endpoint_"+ script[:-3] +".json" 
    # Upload JSON to S3
    s3_client.put_object(
        Bucket=endpoint_bucket,       
        Key=endpoint_path,       
        Body=json_data,
        ContentType="json"  # Set correct content type
    )

    return endpoint_name


if __name__ == "__main__":
    endpoint_creation()