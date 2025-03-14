import subprocess
import time

ZOOKEEPER_CONTAINER = "zookeeper"
KAFKA_CONTAINER = "kafka_server"
KAFKA_TOPICS = ["c2_commands", "agent_response"]

def run_command(command):
    """Run a shell command and return the output."""
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    return result.stdout.strip() if result.returncode == 0 else result.stderr.strip()

def container_exists(container_name):
    """Check if a Docker container is already running."""
    output = run_command(f"docker ps -a --format '{{{{.Names}}}}' | grep -w {container_name}")
    return container_name in output

def start_zookeeper():
    """Start Zookeeper if it's not already running."""
    if container_exists(ZOOKEEPER_CONTAINER):
        print(f"[✔] Zookeeper container '{ZOOKEEPER_CONTAINER}' already exists. Skipping...")
    else:
        print("[*] Starting Zookeeper...")
        run_command(f"docker run -d --name {ZOOKEEPER_CONTAINER} --network host -e ZOOKEEPER_CLIENT_PORT=2181 confluentinc/cp-zookeeper:latest")

def start_kafka():
    """Start Kafka if it's not already running."""
    if container_exists(KAFKA_CONTAINER):
        print(f"[✔] Kafka container '{KAFKA_CONTAINER}' already exists. Skipping...")
    else:
        print("[*] Starting Kafka...")
        run_command(f"docker run -d --name {KAFKA_CONTAINER} --network host -e KAFKA_ZOOKEEPER_CONNECT=localhost:2181 -e KAFKA_ADVERTISED_LISTENERS=PLAINTEXT://localhost:9092 confluentinc/cp-kafka:latest")

def wait_for_kafka():
    """Wait for Kafka to be ready."""
    print("[*] Waiting for Kafka to start...")
    time.sleep(15)  # Give Kafka some time to initialize

def create_topics():
    """Create Kafka topics if they don't already exist."""
    for topic in KAFKA_TOPICS:
        print(f"[*] Creating topic '{topic}' (if not exists)...")
        run_command(f"docker exec {KAFKA_CONTAINER} kafka-topics --create --if-not-exists --topic {topic} --bootstrap-server localhost:9092 --partitions 1 --replication-factor 1")

def setup_kafka():
    """Complete Kafka setup with Zookeeper, Kafka, and topic creation."""
    start_zookeeper()
    start_kafka()
    wait_for_kafka()
    create_topics()
    print("[✔] Kafka setup complete!")

if __name__ == "__main__":
    setup_kafka()
