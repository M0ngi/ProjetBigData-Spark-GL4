import sys
from confluent_kafka import Producer
import requests
import time
from crypto_streamer.config import conf


def acked(err, msg):
    if err is not None:
        print(f"Failed to deliver message: {str(msg)}: {str(err)}", file=sys.stderr)
    else:
        print(f"Message produced: {str(msg)}",  file=sys.stderr)


def run():
    print("Kafka streaming starting in 60 seconds...")
    time.sleep(60)
    producer = Producer(**conf)
    print(producer.list_topics())
    
    while True:
        try:
            resp = requests.get("https://api.coincap.io/v2/rates/bitcoin")
            body = resp.json()
            print(body)
            
            producer.produce("Crypto-Kafka", value=str(body), callback=acked)
            
            time.sleep(1)
        except KeyboardInterrupt:
            print("Exiting...")
            break