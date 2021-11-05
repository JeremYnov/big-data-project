from kafka import KafkaConsumer
import json

c = KafkaConsumer('crypto_news', bootstrap_servers='localhost:9092', api_version=(0, 10, 1))


for msg in c:
    crypto = json.loads(msg.value.decode("utf-8"))
    print(crypto)
    print(type(crypto))