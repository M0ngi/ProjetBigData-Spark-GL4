import sys
import requests
import time


def run():
    print("TCP Streaming started",  file=sys.stderr)
    while True:
        try:
            resp = requests.get("https://api.coincap.io/v2/rates/bitcoin")
            body = resp.json()
            print(body)
            
            time.sleep(1)
        except KeyboardInterrupt:
            print("Exiting...",  file=sys.stderr)
            break
