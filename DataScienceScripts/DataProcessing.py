from sagemaker import get_execution_role
import pandas as pd
import boto3
import os
from io import StringIO


def data_processing():
    features = os.environ.get("FEATURES") if os.environ.get("FEATURES") else [
        'MSSubClass', 'LotArea', 'OverallQual', 'OverallCond', 'YearBuilt', 
        'YearRemodAdd', 'MasVnrArea', 'BsmtFinSF1', 'BsmtFinSF2', 'BsmtUnfSF', 'TotalBsmtSF', 
        '1stFlrSF', '2ndFlrSF', 'LowQualFinSF', 'GrLivArea', 'BsmtFullBath', 'BsmtHalfBath', 
        'FullBath', 'HalfBath', 'BedroomAbvGr', 'KitchenAbvGr', 'TotRmsAbvGrd', 'Fireplaces', 
        'GarageYrBlt', 'GarageCars', 'GarageArea', 'WoodDeckSF', 'OpenPorchSF', 'EnclosedPorch', 
        '3SsnPorch', 'ScreenPorch', 'PoolArea', 'MiscVal', 'MoSold', 'YrSold'
    ]
    
    s3 = boto3.resource('s3')

    if os.environ.get("BUCKET") is None:
        print("Using default bucket")
    bucket_name = os.environ.get("BUCKET") if os.environ.get("BUCKET") else 'data-remote-repository-cefriel'
    if os.environ.get("RAW_TRAIN_PATH") is None:
        print("Using default train data")
    train_file = os.environ.get("RAW_TRAIN_PATH") if os.environ.get("RAW_TRAIN_PATH") else'gruppo-1/raw/train.csv'
    if os.environ.get("RAW_VALIDATION_PATH") is None:
        print("Using default validation data")
    validation_file = os.environ.get("RAW_VALIDATION_PATH") if os.environ.get("RAW_VALIDATION_PATH") else'gruppo-1/raw/validation.csv'
    if os.environ.get("RAW_TEST_PATH") is None:                       #'gruppo-1/raw/test.csv'
        print("Using default test data")
    test_file = os.environ.get("RAW_TEST_PATH") if os.environ.get("RAW_TEST_PATH") else 'gruppo-1/raw/test.csv'

    obj = s3.Object(bucket_name, train_file)
    data = obj.get()['Body'].read()
    data_string = data.decode('utf-8')
    data_file = StringIO(data_string)
    train_df = pd.read_csv(data_file, sep=";")
    
    #validation data
    obj = s3.Object(bucket_name, validation_file)
    data = obj.get()['Body'].read()
    data_string = data.decode('utf-8')
    data_file = StringIO(data_string)
    val_df = pd.read_csv(data_file, sep=";")
    
    #test data
    obj = s3.Object(bucket_name, test_file)
    data = obj.get()['Body'].read()
    data_string = data.decode('utf-8')
    data_file = StringIO(data_string)
    test_df = pd.read_csv(data_file, sep=";")

    train_df = train_df[features+["SalePrice"]]
    val_df = val_df[features+["SalePrice"]]
    test_df = test_df[features]
    
    train_df['MasVnrArea'] = train_df['MasVnrArea'].fillna(train_df['MasVnrArea'].mean())
    train_df['GarageYrBlt'] = train_df['GarageYrBlt'].fillna(train_df['GarageYrBlt'].mean())
    train_df = train_df.dropna()
    val_df['MasVnrArea'] = val_df['MasVnrArea'].fillna(val_df['MasVnrArea'].mean())
    val_df['GarageYrBlt'] = val_df['GarageYrBlt'].fillna(val_df['GarageYrBlt'].mean())
    val_df = val_df.dropna()
    test_df['MasVnrArea'] = test_df['MasVnrArea'].fillna(test_df['MasVnrArea'].mean())
    test_df['GarageYrBlt'] = test_df['GarageYrBlt'].fillna(test_df['GarageYrBlt'].mean())
    test_df = test_df.dropna()

    output = {}
    output["BUCKET"] = bucket_name 
    output["TRAIN_PATH"] = 'gruppo-1/processed/train.csv'
    output["VAL_PATH"] = 'gruppo-1/processed/validation.csv'
    output["TEST_PATH"] = 'gruppo-1/processed/test.csv'
    
    csv_buffer = StringIO()
    train_df.to_csv(csv_buffer, index=False)
    s3.Bucket(bucket_name).put_object(Key=output["TRAIN_PATH"], Body=csv_buffer.getvalue())

    csv_buffer = StringIO()
    val_df.to_csv(csv_buffer, index=False)
    s3.Bucket(bucket_name).put_object(Key=output["VAL_PATH"], Body=csv_buffer.getvalue())

    csv_buffer = StringIO()
    test_df.to_csv(csv_buffer, index=False)
    s3.Bucket(bucket_name).put_object(Key=output["TEST_PATH"], Body=csv_buffer.getvalue())

    return output


if __name__ == "__main__":
    data_processing()





















