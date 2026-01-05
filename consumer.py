from confluent_kafka import Consumer, KafkaException
import json

conf = {
    "bootstrap.servers": "localhost:9095,localhost:9102,localhost:9097",
    "group.id": "test-consumer",
    "auto.offset.reset": "earliest"
}

consumer = Consumer(conf)
topic = "marks"


consumer.subscribe([topic])

print(f"Listening to Kafka topic '{topic}'...")

try:
    while True:
        msg = consumer.poll(1.0) 
        if msg is None:
            continue
        if msg.error():
            raise KafkaException(msg.error())
        data = json.loads(msg.value().decode("utf-8"))
        print("Received:", data)

        score = int(data["score"])
        print("Processed:", score)

except KeyboardInterrupt:
    print("Stopping consumer...")

finally:
    consumer.close()
