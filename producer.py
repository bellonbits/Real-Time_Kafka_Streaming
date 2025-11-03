from kafka import KafkaProducer
from data_gen import gen
import json, time

producer = KafkaProducer(bootstrap_servers=['localhost:9094'],
                         value_serializer=lambda v: json.dumps(v).encode())

try:
    while True:
        for r in gen():
            producer.send("btc", r)
            print("sent:", r)
        time.sleep(4)
except KeyboardInterrupt:
    print("stopped")
