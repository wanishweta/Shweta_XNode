import csv
import time
from confluent_kafka import Producer

# Kafka producer configuration
conf = {
    'bootstrap.servers': 'localhost:9092',  # Kafka server address
    'client.id': 'csv-producer'
}

# Create a producer instance
producer = Producer(conf)

# Kafka topic to which we will publish messages
topic = 'transactionlog'


# Function to send the CSV line to Kafka
def delivery_report(err, msg):
    """Delivery report callback to print status of message delivery."""
    if err is not None:
        print(f"Message delivery failed: {err}")
    else:
        print(f"Message delivered to {msg.topic()} [{msg.partition()}] at offset {msg.offset()}")


# Read the CSV file and send each line to Kafka every 5 seconds
def read_and_produce_csv(file_path):
    with open(file_path, newline='', encoding='utf-8') as file:
        reader = csv.reader(file)
        for row in reader:
            # Convert row to a CSV string and send to Kafka
            csv_line = ','.join(row)
            producer.produce(topic, key=None, value=csv_line, callback=delivery_report)

            # Wait for 5 seconds before sending the next line
            time.sleep(5)

            # Poll the producer to handle any callbacks (ensure messages are sent)
            producer.poll(0)

    # Flush any remaining messages in the producer buffer
    producer.flush()

from pathlib import Path

# Get the current directory of the script
current_dir = Path(__file__).resolve().parent

# Get the parent directory (previous directory)
parent_dir = current_dir.parent

# Print the parent directory path
print("Parent directory:", parent_dir)

# Specify the path to your CSV file

csv_file_path = '../InputFile/transactions.csv'
#csv_file_path = '/app/data/transactions.csv'

# Start reading from the CSV file and sending data to Kafka
read_and_produce_csv(csv_file_path)
