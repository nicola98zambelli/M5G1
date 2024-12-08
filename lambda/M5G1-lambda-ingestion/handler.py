import json
import pandas as pd
from services.s3 import S3
import os
from sklearn.model_selection import train_test_split
# to importe kaggle we ned to configure credentials dir  first
os.environ["KAGGLE_CONFIG_DIR"] = "./config/kaggle"
from services.kaggle import KaggleDownloader

def main(event, context):

    bucket_name ='data-remote-repository-cefriel'
    output_key_path = "gruppo-1/"
    train_file_name = 'train.csv'
    validation_file_name = 'validation.csv'
    test_file_name = 'test.csv'
    kaggle_competition = "house-prices-advanced-regression-techniques"
    downloader = KaggleDownloader(competition_name=kaggle_competition )

    df_train_kg = downloader.load_data_as_dataframe(file_name='train.csv')
    print(df_train_kg.head(5))
    print(df_train_kg.shape)
    train_df, valid_df = train_test_split(df_train_kg, test_size=0.2, random_state=42)
    print(train_df.shape)
    print(valid_df.shape)

    test_df = downloader.load_data_as_dataframe(file_name='test.csv')
    print(test_df.shape)

    S3.upload_csv(bucket_name, output_key_path + train_file_name, train_df)
    S3.upload_csv(bucket_name, output_key_path + validation_file_name, valid_df)
    S3.upload_csv(bucket_name, output_key_path + test_file_name, test_df)

    return None

if __name__ == "__main__":
    main(event=None, context=None)


