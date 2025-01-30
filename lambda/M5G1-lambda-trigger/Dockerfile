FROM public.ecr.aws/lambda/python:3.12
RUN pip install --upgrade pip
ADD requirements.txt ./
RUN pip install -r requirements.txt
COPY . ./
CMD ["main.lambda_handler"]