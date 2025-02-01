import os
import boto3
from io import StringIO
import pandas as pd
import json

def endpoint_test():
    #load resources
    boto3.setup_default_session(region_name="us-east-1")  # Cambia con la tua regione
    s3 = boto3.resource('s3')
    s3_client = boto3.client("s3")
    sm_boto3 = boto3.client("sagemaker")
    sagemaker_runtime = boto3.client("sagemaker-runtime")
    #get env variables
    if os.environ.get("BUCKET") is None:
        print("Using default bucket")
    bucket_name = os.environ.get("BUCKET") if os.environ.get("BUCKET") else 'data-remote-repository-cefriel'
    if os.environ.get("TEST_PATH") is None:
        print("Using default test set")
    test_file = os.environ.get("TEST_PATH") if os.environ.get("TEST_PATH") else 'gruppo-1/processed/test.csv'
    if os.environ.get("SCRIPT") is None:
        print("Using default script")
    script = os.environ.get("SCRIPT") if os.environ.get("SCRIPT") else "random_forest_regressor.py"
    if os.environ.get("FEATURES") is None:
        print("Using default features")
    features = os.environ.get("FEATURES") if os.environ.get("FEATURES") else [
        'MSSubClass', 'LotArea', 'OverallQual', 'OverallCond', 'YearBuilt', 
        'YearRemodAdd', 'MasVnrArea', 'BsmtFinSF1', 'BsmtFinSF2', 'BsmtUnfSF', 'TotalBsmtSF', 
        '1stFlrSF', '2ndFlrSF', 'LowQualFinSF', 'GrLivArea', 'BsmtFullBath', 'BsmtHalfBath', 
        'FullBath', 'HalfBath', 'BedroomAbvGr', 'KitchenAbvGr', 'TotRmsAbvGrd', 'Fireplaces', 
        'GarageYrBlt', 'GarageCars', 'GarageArea', 'WoodDeckSF', 'OpenPorchSF', 'EnclosedPorch', 
        '3SsnPorch', 'ScreenPorch', 'PoolArea', 'MiscVal', 'MoSold', 'YrSold'
    ]
    if os.environ.get("ENDPOINT_DATA_URI") is None:
        print("Using default output bucket")
    endpoint_bucket = os.environ.get("ENDPOINT_DATA_URI") if os.environ.get("ENDPOINT_DATA_URI") else "data-remote-repository-cefriel"
    if os.environ.get("ENDPOINT_OUTPUT_PATH") is None:
        print("Using default endpoint artifatcs path")
    endpoint_path = os.environ.get("ENDPOINT_OUTPUT_PATH") if os.environ.get("ENDPOINT_OUTPUT_PATH") else "gruppo-1/outputs/endpoint_"+ script[:-3] +".json"
    #load data
    obj = s3.Object(bucket_name, test_file)
    data = obj.get()['Body'].read()
    data_string = data.decode('utf-8')
    data_file = StringIO(data_string)
    X_test = pd.read_csv(data_file)
    print("Test shape: ", X_test.shape)
    print("NaN entries: ", X_test.isna().values.sum())
    payload = X_test.to_csv(index=False)
    #load endpoint
    response = s3_client.get_object(Bucket=endpoint_bucket, Key=endpoint_path)
    content = response['Body'].read().decode('utf-8')
    endpoint_data = json.loads(content)
    endpoint_name = endpoint_data["ENDPOINT_NAME"]
    print(endpoint_name)
    #send prediction
    response = sagemaker_runtime.invoke_endpoint(
        EndpointName=endpoint_name,
        ContentType="text/csv",
        Body=payload
    )
    print(response)

    print("DELITING ENDPOINT FOR RESOURCE MANAGEMENT")
    print("Future improvements, A/B testing and various Deployment options")
    sm_boto3.delete_endpoint(EndpointName=endpoint_name)


if __name__ == "__main__":
    endpoint_test()





