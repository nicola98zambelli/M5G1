docker build -t gruppo1:M5G1-lambda-exec-uuid .
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin 314146336986.dkr.ecr.us-east-1.amazonaws.com/gruppo1:M5-G1-lambda-trigger
docker tag gruppo1:M5G1-lambda-exec-uuid 314146336986.dkr.ecr.us-east-1.amazonaws.com/gruppo1:M5G1-lambda-exec-uuid
docker push 314146336986.dkr.ecr.us-east-1.amazonaws.com/gruppo1:M5G1-lambda-exec-uuid 
