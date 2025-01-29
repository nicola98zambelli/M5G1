import pandas as pd
import boto3
from io import StringIO


def main():
    features = [
        'MSSubClass', 'LotArea', 'OverallQual', 'OverallCond', 'YearBuilt', 
        'YearRemodAdd', 'MasVnrArea', 'BsmtFinSF1', 'BsmtFinSF2', 'BsmtUnfSF', 'TotalBsmtSF', 
        '1stFlrSF', '2ndFlrSF', 'LowQualFinSF', 'GrLivArea', 'BsmtFullBath', 'BsmtHalfBath', 
        'FullBath', 'HalfBath', 'BedroomAbvGr', 'KitchenAbvGr', 'TotRmsAbvGrd', 'Fireplaces', 
        'GarageYrBlt', 'GarageCars', 'GarageArea', 'WoodDeckSF', 'OpenPorchSF', 'EnclosedPorch', 
        '3SsnPorch', 'ScreenPorch', 'PoolArea', 'MiscVal', 'MoSold', 'YrSold'
    ]
    
    s3 = boto3.resource('s3')
    
    #bucket_name = os.environ.get("BUCKET")                   #'data-remote-repository-cefriel'
    bucket_name = 'data-remote-repository-cefriel'
    
    #train_file = os.environ.get("RAW_TRAIN_PATH")                     #'gruppo-1/raw/train.csv'
    train_file = 'gruppo-1/train.csv'
    #validation_file = os.environ.get("RAW_VAL_PATH")                  #'gruppo-1/raw/validation.csv'
    validation_file = 'gruppo-1/validation.csv'
    #test_file = os.environ.get("RAW_TEST_PATH")                       #'gruppo-1/raw/test.csv'
    test_file = 'gruppo-1/test.csv'
    #train data
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
    
    train_df['MasVnrArea'] = train_df['MasVnrArea'].fillna(train_df['MasVnrArea'].mean())
    train_df['GarageYrBlt'] = train_df['GarageYrBlt'].fillna(train_df['GarageYrBlt'].mean())
    val_df['MasVnrArea'] = val_df['MasVnrArea'].fillna(val_df['MasVnrArea'].mean())
    val_df['GarageYrBlt'] = val_df['GarageYrBlt'].fillna(val_df['GarageYrBlt'].mean())
    test_df['MasVnrArea'] = test_df['MasVnrArea'].fillna(test_df['MasVnrArea'].mean())
    test_df['GarageYrBlt'] = test_df['GarageYrBlt'].fillna(test_df['GarageYrBlt'].mean())
    
    train_df = train_df[features+["SalePrice"]]
    val_df = val_df[features+["SalePrice"]]
    test_df = test_df[features]

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
    main()
