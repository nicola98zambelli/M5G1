import io
import boto3

# Utility class for interacting with S3 storage
class S3:
    @staticmethod
    def get_object(bucket_name, object_key):
        """
        Retrieves an object from a specified S3 bucket
        Used for downloading files from S3
        """
        s3 = boto3.client('s3', region_name='us-east-1')
        obj = s3.get_object(Bucket=bucket_name, Key=object_key)
        return obj

    @staticmethod
    def upload_csv(bucket_name, object_key, dataframe):
        """
        Uploads a pandas DataFrame as a CSV to S3
        """
        s3 = boto3.client('s3', region_name='us-east-1')
        try:
            # creating csv buffer in memory
            csv_buffer = io.StringIO()
            dataframe.to_csv(csv_buffer, sep=';', index=False)
            # upload csv to s3
            s3.put_object(Bucket=bucket_name, Key=object_key, Body=csv_buffer.getvalue())
            print(f"CSV successfully uploaded: {object_key} in {bucket_name}")
        except Exception as e:
            print(f"Error during the uploading of CSV to S3: {e}")
            raise