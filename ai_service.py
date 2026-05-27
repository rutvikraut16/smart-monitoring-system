from kafka import KafkaConsumer
import json

consumer = KafkaConsumer(
    'sensor-data',
    bootstrap_servers='localhost:9092',
    value_deserializer=lambda x: json.loads(x.decode('utf-8'))
)

print("AI Service Started...")

for message in consumer:
    data = message.value
    temperature = data["temperature"]
    print("Received:", data)
    if temperature > 70:
        print("🚨 ALERT: High Temperature Detected!")
    else:
        print("✅ Temperature Normal")