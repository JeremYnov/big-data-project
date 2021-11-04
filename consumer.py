from kafka import KafkaConsumer
import json

c = KafkaConsumer('big-data-topic', bootstrap_servers='localhost:9092', api_version=(0, 10, 1))


for msg in c:
    # crypto = msg.value.decode("utf-8")
    crypto = json.loads(msg.value.decode("utf-8"))
    
    print(crypto)
    
    # print(crypto)
    print(type(crypto))