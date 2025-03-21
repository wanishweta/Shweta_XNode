# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Install the necessary dependencies (e.g., confluent-kafka)
RUN pip install confluent-kafka

# Set environment variables (optional, you can replace these with actual values)
ENV KAFKA_BROKER_URL=kafka:9093

# Set the working directory in the container
WORKDIR /app

# Copy the transactions.csv file into the container at /app/data
COPY ./transactions.csv /app/data/

# Copy the rest of the application files into the container
COPY . /app/

# Run the producer.py script as the container starts
CMD ["python3", "./producer.py"]
