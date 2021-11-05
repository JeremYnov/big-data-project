
import pandas as pd
from time import sleep
from json import dumps
from kafka import KafkaProducer
import requests

producer = KafkaProducer(
  bootstrap_servers='kafka:9092',
  value_serializer=lambda x: dumps(x).encode('utf-8')
)

API_KEY = '4cb209d86481440649b653af92741b370037dbde'
url = "https://cryptopanic.com/api/v1/posts/?auth_token={}".format(API_KEY)

while True :   
    try:
        page = requests.get(url)
        data = page.json()
        news = data['results']
        producer.send('crypto_news', value = news)
    except:
        print('error')
    sleep(31)