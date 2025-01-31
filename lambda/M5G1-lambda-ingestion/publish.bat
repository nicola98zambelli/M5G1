docker build -t gruppo1:M5G1-lambda-ingestion .
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin 314146336986.dkr.ecr.us-east-1.amazonaws.com/gruppo1:M5G1-lambda-ingestion
docker tag gruppo1:M5G1-lambda-ingestion 314146336986.dkr.ecr.us-east-1.amazonaws.com/gruppo1:M5G1-lambda-ingestion
docker push 314146336986.dkr.ecr.us-east-1.amazonaws.com/gruppo1:M5G1-lambda-ingestion