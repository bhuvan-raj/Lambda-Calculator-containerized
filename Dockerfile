FROM public.ecr.aws/lambda/python:3.8

# Install dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy application code
COPY app.py .
COPY templates/ ./templates/
COPY static/ ./static/

# Set the CMD to your handler
CMD ["app.lambda_handler"]
