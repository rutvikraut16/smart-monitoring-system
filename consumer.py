from kafka import KafkaConsumer
import json

consumer = KafkaConsumer(
    'sensor-data',
    bootstrap_servers='localhost:9092',
    value_deserializer=lambda x: json.loads(x.decode('utf-8'))
)

for message in consumer:
    data = message.value
    print("Received:", data)
    if data["temperature"] > 70:
        print("🔴 High Temperature Alert!")
    else:
        print("🟢 Normal Temperature")