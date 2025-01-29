FROM public.ecr.aws/lambda/python:3.12

# Upgrade pip
RUN pip install --upgrade pip

# Add and install requirements
ADD requirements.txt ./
RUN pip install -r requirements.txt

# Copy the script into the container
COPY DataProcessing.py ./

# Set the command to run the script
CMD ["python", "DataProcessing.py"]