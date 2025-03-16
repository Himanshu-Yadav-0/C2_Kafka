# Kafka & Docker Debugging Guide

This document contains solutions to common issues when running Kafka with Docker using Bitnami images.

Issues occured to me on 17/march/2025, and yea chatgpt wrote this for me, but guys i still maintain the doc.

## 🚀 1. Containers Stuck in "Created" State

### ❌ Issue:
When running `docker ps -a`, Kafka and Zookeeper appear in "Created" state and won’t start.

### 🔍 Check Container Status:
```sh
docker ps -a
```
If Kafka or Zookeeper is stuck in "Created", try starting them manually:
```sh
docker start zookeeper
docker start kafka_server
```

### ✅ Solution:
If they fail to start and you see an error about a missing network, remove the containers and recreate them:
```sh
docker rm -f kafka_server zookeeper
docker network create kafka_network
```
Then, recreate the containers:
```sh
docker run -d --name zookeeper \
  --network kafka_network \
  -p 2181:2181 \
  -e ALLOW_ANONYMOUS_LOGIN=yes \
  bitnami/zookeeper:latest
```
```sh
docker run -d --name kafka_server \
  --network kafka_network \
  -p 9092:9092 \
  -e KAFKA_ZOOKEEPER_CONNECT=zookeeper:2181 \
  -e KAFKA_LISTENERS=PLAINTEXT://0.0.0.0:9092 \
  -e KAFKA_ADVERTISED_LISTENERS=PLAINTEXT://localhost:9092 \
  -e ALLOW_PLAINTEXT_LISTENER=yes \
  bitnami/kafka:latest
```
Now verify:
```sh
docker ps
```

## 🚀 2. Kafka Broker Not Available (NoBrokersAvailable)

### ❌ Issue:
Python Kafka client (`kafka-python`) throws an error:
```makefile
kafka.errors.NoBrokersAvailable: NoBrokersAvailable
```
This happens when Kafka is not reachable on `localhost:9092`.

### ✅ Solution:
Check if Kafka is running:
```sh
docker ps
```
If Kafka is missing, start it:
```sh
docker start kafka_server
```
Check if Kafka is listening on port 9092:
```sh
netstat -an | findstr 9092
```
If port 9092 is empty, restart Kafka with the correct configurations.

Check logs for errors:
```sh
docker logs kafka_server
```
If you see "Address already in use" or "Connection refused", ensure Kafka is started with:
```sh
-e KAFKA_ADVERTISED_LISTENERS=PLAINTEXT://localhost:9092
```

## 🚀 3. `docker exec` Command Path Issues in Git Bash

### ❌ Issue:
Running `docker exec` in Git Bash gives an error:
```perl
OCI runtime exec failed: exec: "C:/Program Files/Git/opt/bitnami/kafka/bin/kafka-topics.sh": no such file or directory
```
This happens because Git Bash converts Linux paths (`/opt/...`) into Windows paths (`C:/Program Files/Git/...`).

### ✅ Solution 1: Use `winpty`
In Git Bash, prepend `winpty` before `docker exec`:
```sh
winpty docker exec -it kafka_server /opt/bitnami/kafka/bin/kafka-topics.sh --list --bootstrap-server localhost:9092
```

### ✅ Solution 2: Use CMD or PowerShell
Run the command in Command Prompt (CMD) or PowerShell instead:
```sh
docker exec -it kafka_server /opt/bitnami/kafka/bin/kafka-topics.sh --list --bootstrap-server localhost:9092
```

## 🚀 4. Kafka Config Argument Issue in Python

### ❌ Issue:
Python script fails with:
```css
TypeError: KafkaProducer.__init__() takes 1 positional argument but 2 were given
```
Caused by passing Kafka configuration incorrectly:
```python
Config = {
    'bootstrap_server': 'localhost:9092'
}
producer = KafkaProducer(Config)  # ❌ Incorrect
```

### ✅ Solution:
Use `**Config` to unpack dictionary keys as arguments:
```python
Config = {
    'bootstrap_servers': 'localhost:9092'  # ✅ Correct key name
}
producer = KafkaProducer(**Config)
```

## 🚀 5. Kafka Topics Not Listing (No Such File or Directory)

### ❌ Issue:
Running:
```sh
docker exec -it kafka_server /opt/bitnami/kafka/bin/kafka-topics.sh --list --bootstrap-server localhost:9092
```
Throws:
```perl
exec: "C:/Program Files/Git/opt/bitnami/kafka/bin/kafka-topics.sh": no such file or directory
```

### ✅ Solution:
Check if Kafka is running:
```sh
docker ps
```
If it's not running:
```sh
docker start kafka_server
```
Enter the Kafka container:
```sh
docker exec -it kafka_server bash
```
Then, manually check if Kafka is installed:
```sh
ls -l /opt/bitnami/kafka/bin/
```
If the directory exists, run the command from inside the container:
```sh
/opt/bitnami/kafka/bin/kafka-topics.sh --list --bootstrap-server localhost:9092
```
If using Git Bash, switch to CMD/PowerShell.

## 🚀 6. Debugging Checklist

### ✅ Check if Kafka & Zookeeper are running:
```sh
docker ps
```
### ✅ Check container logs for errors:
```sh
docker logs kafka_server
docker logs zookeeper
```
### ✅ Ensure correct Kafka connection settings in Python:
```python
KafkaProducer(bootstrap_servers='localhost:9092')
```
### ✅ Use CMD/PowerShell for `docker exec` commands
### ✅ If using Git Bash, use `winpty docker exec ...`

## 🎯 Final Notes
- Always check logs (`docker logs kafka_server`) for debugging.
- If Kafka is unreachable, verify port `9092` (`netstat -an | findstr 9092`).
- If `docker exec` fails in Git Bash, use CMD or PowerShell.
