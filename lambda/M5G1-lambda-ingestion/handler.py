import json
import os
import logging
from typing import Dict, Any, Optional

import pandas as pd

# Ensure Kaggle config directory exists before importing
KAGGLE_CONFIG_DIR = "./config/kaggle"
os.environ["KAGGLE_CONFIG_DIR"] = KAGGLE_CONFIG_DIR
from services.s3 import S3
from services.kaggle import KaggleDownloader

# Configure logging
logging.basicConfig(
    level=logging.INFO, 
    format='%(asctime)s - %(levelname)s: %(message)s'
)
logger = logging.getLogger(__name__)

def load_config() -> Dict[str, str]:
    """Load configuration from environment variables with defaults."""
    return {
        'bucket_name': os.getenv('S3_BUCKET', 'data-remote-repository-cefriel'),
        'output_key_path': os.getenv('S3_OUTPUT_PATH', 'gruppo-1/'),
        'kaggle_competition': os.getenv('KAGGLE_COMPETITION', 'house-prices-advanced-regression-techniques'),
        'kaggle_config_dir': KAGGLE_CONFIG_DIR
    }

def main(event: Optional[Dict] = None, context: Any = None, debug: bool = False) -> Dict[str, Any]:
    """
    Main Lambda handler for downloading and processing Kaggle dataset.
    
    :param event: AWS Lambda event
    :param context: AWS Lambda context
    :param debug: Enable debug logging
    :return: Lambda response dictionary
    """
    if debug:
        logger.setLevel(logging.DEBUG)

    try:
        config = load_config()
        os.environ["KAGGLE_CONFIG_DIR"] = config['kaggle_config_dir']

        downloader = KaggleDownloader(competition_name=config['kaggle_competition'])
        
        df_train_kg = downloader.load_data_as_dataframe('train.csv')
        logger.debug(f"Training data shape: {df_train_kg.shape}")

        # to avoid sklearn library we do the same thing in pandas
        #train_df, valid_df = train_test_split(df_train_kg, test_size=0.2, random_state=42)
        test_size = 0.2
        random_state = 42
        test_len = int(len(df_train_kg) * test_size)
        valid_df = df_train_kg.sample(n=test_len, random_state=random_state)
        train_df = df_train_kg.drop(valid_df.index)   
        test_df = downloader.load_data_as_dataframe('test.csv')

        # Upload to S3
        file_names = {
            'train': 'train.csv', 
            'validation': 'validation.csv', 
            'test': 'test.csv'
        }
        
        for key, df in [('train', train_df), ('validation', valid_df), ('test', test_df)]:
            S3.upload_csv(
                config['bucket_name'], 
                f"{config['output_key_path']}{file_names[key]}", 
                df
            )

        logger.info("Data processing completed successfully")
        return {
            'statusCode': 200,
            'body': json.dumps('Data processing completed')
        }

    except Exception as e:
        logger.exception(f"Data processing failed: {e}")
        return {
            'statusCode': 500,
            'body': json.dumps(f'Error: {str(e)}')
        }

if __name__ == "__main__":
    main(debug=True)