docker build -t gruppo1:M5-G1-DataProcessing .
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin 314146336986.dkr.ecr.us-east-1.amazonaws.com/gruppo1:M5-G1-DataProcessing
docker tag gruppo1:M5-G1-DataProcessing 314146336986.dkr.ecr.us-east-1.amazonaws.com/gruppo1:M5-G1-DataProcessing
docker push 314146336986.dkr.ecr.us-east-1.amazonaws.com/gruppo1:M5-G1-DataProcessing 
