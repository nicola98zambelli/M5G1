FROM public.ecr.aws/lambda/python:3.12
RUN pip install --upgrade pip
COPY . ./
CMD ["main.lambda_handler"]