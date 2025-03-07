# Use the AWS Lambda Python base image
FROM public.ecr.aws/lambda/python:3.9

# Install dependencies
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY . ${LAMBDA_TASK_ROOT}

CMD [ "main.handler" ]

