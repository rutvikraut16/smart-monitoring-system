from kafka import KafkaConsumer
import json

consumer = KafkaConsumer(
    'sensor-data',
    bootstrap_servers='localhost:9092',
    auto_offset_reset='earliest',
    value_deserializer=lambda x: json.loads(x.decode('utf-8'))
)

print("Consumer Started...")

for message in consumer:

    data = message.value

    print("Received:", data)

    temp = data["temperature"]

    if temp > 70:
        print("High Temperature Alert")
    else:
        print("Normal Temperature")