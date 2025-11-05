from kafka import KafkaConsumer
from pymongo import MongoClient
import json

consumer = KafkaConsumer(
    "btc",
    bootstrap_servers=["localhost:9094"],
    value_deserializer=lambda m: json.loads(m.decode()),
    enable_auto_commit=True,
    auto_offset_reset="earliest",
)
mongo = MongoClient("mongodb+srv://admin:PASS@cluster0.a1r0c.mongodb.net/?appName=Cluster0")
col = mongo.coins.btc

for msg in consumer:
    col.insert_one(msg.value)
    print("saved:", msg.value)

