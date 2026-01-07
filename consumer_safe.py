from confluent_kafka import Consumer, Producer, KafkaException
import json
from prometheus_client import Counter, start_http_server



poison_pill_counter = Counter('poison_pills_total', 'Total poison pills detected')


start_http_server(9200)
print("Prometheus metrics available on http://localhost:9200")


conf = {
    "bootstrap.servers": "localhost:9095,localhost:9097,localhost:9102",
    "group.id": "test-consumer",
    "auto.offset.reset": "earliest"
}

consumer = Consumer(conf)
consumer.subscribe(["marks"])

dlq = Producer({"bootstrap.servers": "localhost:9095,localhost:9097,localhost:9102"})
clean_producer = Producer({"bootstrap.servers": "localhost:9095,localhost:9097,localhost:9102"})
print("Listening to 'marks' topic...")

try:
    while True:
        msg = consumer.poll(1.0)
        if msg is None:
            continue
        if msg.error():
            raise KafkaException(msg.error())

        try:
            data = json.loads(msg.value().decode("utf-8"))
            print("Received:", data)

            score = int(data["score"])
            print("Processed:", score)

            clean_producer.produce(
                topic="marks_clean",
                value=json.dumps(data).encode("utf-8"),
                key=str(data.get("id"))
            )
            clean_producer.flush()

        except Exception as e:
            print("Poison pill detected:", msg.value())
            poison_pill_counter.inc() 
            dlq.produce(
                topic="marks_dlq",
                value=json.dumps({
                    "original_message": msg.value().decode("utf-8"),
                    "error": str(e)
                }).encode("utf-8")
            )
            dlq.flush()
            continue

except KeyboardInterrupt:
    print("Stopping consumer...")

finally:
    consumer.close()
