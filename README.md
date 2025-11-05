# Apache Kafka 

## 1. What is Apache Kafka?

* **Kafka** is a **real-time data streaming platform** that lets systems send and receive data instantly, like a live message queue.
* Developed by **LinkedIn (2011)** to handle billions of messages daily.
* Used by **Netflix, Uber, Airbnb** — any company dealing with **live data** such as transactions, sensor data, or user activity.

**Real-world idea:**
Imagine your phone apps (banking, Uber, YouTube) continuously sending small bits of data — Kafka makes sure that data moves fast, safely, and reliably.

---

## 2. Kafka's Architecture (The Building Blocks)

### Brokers and Clusters

* **Broker:** A Kafka server that stores and serves data.
* **Cluster:** A group of brokers working together (usually 3 or more).
* If one broker fails, others continue working → **fault tolerance**.

**Analogy:**
Think of brokers as different cashiers in a supermarket. If one breaks down, others continue serving customers.

---

### ZooKeeper vs KRaft

* **ZooKeeper:** Used to manage Kafka clusters (older system).
* **KRaft:** New system (from Kafka 2.8) that removes ZooKeeper.
  Simpler, faster, and scales better.
* **Recommendation:** Use **KRaft** for new Kafka setups.

---

## 3. Topics, Partitions, and Offsets

| Concept       | Description                                  | Analogy                       |
|---------------|----------------------------------------------|-------------------------------|
| **Topic**     | A category or stream name (e.g., "orders")   | A folder name                 |
| **Partition** | A slice of the topic for parallel processing | Dividing work among employees |
| **Offset**    | A unique ID for each message                 | A line number in a book       |

Kafka topics = **append-only logs** → old data is never modified, only new data added.

---

### Example:

```bash
kafka-topics.sh --create \
  --topic orders \
  --partitions 6 \
  --replication-factor 3 \
  --bootstrap-server localhost:9092
```

* 6 partitions = 6 consumers can work simultaneously.
* 3 replication = each piece of data has 3 backups.

---

## 4. Producers (Senders)

Producers send data into Kafka topics.

```python
from kafka import KafkaProducer
import json

producer = KafkaProducer(
    bootstrap_servers=['localhost:9092'],
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

producer.send('orders', value={'order_id': '001', 'amount': 99.99})
producer.flush()
```

### Key Concepts

* **Keys** → decide which partition stores the message.
* **Acks** (Acknowledgements):
  * `acks=0` → Fast, not reliable.
  * `acks=1` → Medium, leader only.
  * `acks=all` → Most reliable.

---

## 5. Consumers (Receivers)

Consumers read and process data from Kafka topics.

```python
from kafka import KafkaConsumer
import json

consumer = KafkaConsumer(
    'orders',
    bootstrap_servers=['localhost:9092'],
    group_id='order-processors',
    value_deserializer=lambda m: json.loads(m.decode('utf-8'))
)

for message in consumer:
    print("Processing:", message.value)
```

### Consumer Groups

* Many consumers can share a topic.
* Kafka assigns partitions automatically.
* If one consumer dies, others take over its work.

---

## 6. Delivery Semantics

| Type              | Description                      | Use Case         |
|-------------------|----------------------------------|------------------|
| **At-most-once**  | May lose messages                | Metrics          |
| **At-least-once** | No loss, but duplicates possible | Most systems     |
| **Exactly-once**  | No loss, no duplicates           | Finance, Banking |

Exactly-once → achieved using **idempotent producers** and **transactions**.

---

## 7. Replication & Fault Tolerance

* Each partition has **1 leader** and **followers**.
* Followers copy data from the leader.
* If leader fails, a follower becomes the new leader.

**Replication factor = 3** means 3 copies → high reliability.

---

## 8. Kafka Security Basics

### ACLs (Access Control Lists)

Control who can **read** or **write** topics.

```bash
# Give write access
kafka-acls.sh --add \
--allow-principal User:data-engineer \
--operation Write \
--topic orders
```

### Encryption (TLS)

Encrypts data moving across the network.

### Authentication (SASL)

Verifies user identity before allowing access.

---

## 9. Data Retention Policies

Kafka automatically deletes or compacts old data.

* **Time-based:** Delete after X hours
  `log.retention.hours=168`
* **Size-based:** Delete after topic reaches X GB
  `log.retention.bytes=10737418240`
* **Compaction:** Keep only the latest value per key
  `log.cleanup.policy=compact`

---

## 10. Real-World Use Cases

| Company      | Use Case                               | Impact                    |
|--------------|----------------------------------------|---------------------------|
| **Netflix**  | Real-time monitoring & recommendations | 700B events/day           |
| **LinkedIn** | Activity streams, notifications        | Origin of Kafka           |
| **Uber**     | Dynamic pricing & tracking             | Petabytes/day             |
| **Airbnb**   | Event-driven microservices             | Real-time fraud detection |

---

## 11. Monitoring and Optimization

### Key Metrics:

* **Consumer Lag** – delay between producer and consumer.
* **Under-Replicated Partitions** – signals risk of data loss.
* **CPU/Disk I/O** – for cluster health.

### Performance Tips:

```python
KafkaProducer(
    compression_type='snappy',  # Compress messages
    batch_size=32768,           # Larger batches
    linger_ms=10                # Wait to collect messages
)
```

Bigger batches = higher throughput, lower network cost.

---

## 12. Summary

| Concept         | Meaning                        |
|-----------------|--------------------------------|
| **Broker**      | Kafka server                   |
| **Topic**       | Named data stream              |
| **Partition**   | Split of topic for parallelism |
| **Producer**    | Sends data                     |
| **Consumer**    | Reads data                     |
| **Offset**      | Message ID                     |
| **Replication** | Data backup                    |
| **KRaft**       | New cluster manager            |
| **ACL & TLS**   | Security features              |
| **Retention**   | Controls old data deletion     |

---
