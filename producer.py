from kafka import KafkaProducer
import json
import random
import time

producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

while True:

    temp = random.randint(20, 100)

    data = {
        "temperature": temp
    }

    producer.send("sensor-data", data)

    print("Produced:", data)

    time.sleep(2)