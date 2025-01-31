# M5G1
## Architecture Overview
This project implements a machine learning pipeline in AWS that automates data ingestion from Kaggle, processes the data, and trains models using Amazon SageMaker. We might describe the flow in two layers:
  * Data ingestion layer: an EventBridge schedule triggers weekly the initial Lambda function ```M5G1-lambda-ingestion```, which communicates with the Kaggle API to fetch data. Raw data is stored in an S3 bucket at ```s3://data-remote-repository-cefnai/gruppo-1/raw/```.
  * Processing Layer: a second Lambda function ```M5G1-lambda-trigger``` triggers the StepFunction ```M5-G1-sfJobsWaterfall``` that orchestrates sequential SageMaker jobs. Another Lambda function ```M5-G1-lambda-exec-uuid``` generates unique execution IDs for job naming consistency. Each stage interacts with a specific S3 bucket to properly store the precessed data, models and outputs.

All Lambda functions are containerized with their images stored in ECR, so that Kaggle tokens and credentials are securely stored. SageMaker runs containerized data processing and training scripts.
All Docker images are built and pushed to ECR using provided ```publish.bat``` scripts.
We also implemented GitHub Actions to automate build and deployment of Lambda images and SageMaker jobs to ECR. Actions are triggered enytime we merge an update of the Lambda / jobs scripts from ```dev``` to the ```main``` branch.

Finally, here's the architecture technical overview:
![M5-G1-architecture-draft (1)](https://github.com/user-attachments/assets/8ac0759a-5231-4ce9-99fc-c2c29bc6fcbb)


