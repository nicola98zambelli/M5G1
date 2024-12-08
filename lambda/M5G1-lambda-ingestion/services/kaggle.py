import os
import pandas as pd
import tempfile
from kaggle.api.kaggle_api_extended import KaggleApi

class KaggleDownloader:
    def __init__(self, competition_name, ):
        self.competition_name = competition_name
        # Inizializza e autentica l'API di Kaggle
        self.api = KaggleApi()
        self.api.authenticate()

    def load_data_as_dataframe(self, file_name):
        """
        Load a file from Kaggle directly into a pandas DataFrame using a temporary file.

        :param file_name: Name of the file to load (e.g., 'train.csv').
        :return: A pandas DataFrame containing the file data.
        """
        print(f"Downloading {file_name} from competition '{self.competition_name}' to a temporary file...")
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_file_path = os.path.join(temp_dir, file_name)
            self.api.competition_download_file(self.competition_name, file_name, path=temp_dir)

            if not os.path.exists(temp_file_path):
                raise FileNotFoundError(f"Failed to download {file_name}. Check the competition name and file name.")

            print(f"Loading {file_name} into a pandas DataFrame...")
            return pd.read_csv(temp_file_path)
