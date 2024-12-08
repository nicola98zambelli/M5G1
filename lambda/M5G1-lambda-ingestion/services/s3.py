import io
import boto3

class S3:
    @staticmethod
    def get_object(bucket_name, object_key):
        s3 = boto3.client('s3', region_name='us-east-1')
        obj = s3.get_object(Bucket=bucket_name, Key=object_key)
        return obj

    @staticmethod
    def upload_csv(bucket_name, object_key, dataframe):
        s3 = boto3.client('s3', region_name='us-east-1')
        try:
            # Creare un buffer CSV in memoria
            csv_buffer = io.StringIO()
            # dataframe.to_csv(csv_buffer, index=False)  # Salva il DataFrame come CSV in memoria
            dataframe.to_csv(csv_buffer, sep=';', index=False)
            # Caricare il CSV in S3
            s3.put_object(Bucket=bucket_name, Key=object_key, Body=csv_buffer.getvalue())
            print(f"CSV caricato con successo: {object_key} in {bucket_name}")
        except Exception as e:
            print(f"Errore durante il caricamento del CSV: {e}")
            raise