from kafka import KafkaConsumer

c = KafkaConsumer('big-data-topic', bootstrap_servers='localhost:9092', api_version=(0, 10, 1))


for msg in c:
    crypto = msg.value
    print(crypto)
    print(type(crypto))