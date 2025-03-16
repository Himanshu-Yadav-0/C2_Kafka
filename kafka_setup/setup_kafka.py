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
    """Check if a Docker container exists (running or stopped)."""
    output = run_command(f"docker ps -a --format '{{{{.Names}}}}' | grep -w {container_name}")
    return container_name in output

def container_running(container_name):
    """Check if a Docker container is running."""
    output = run_command(f"docker ps --format '{{{{.Names}}}}' | grep -w {container_name}")
    return container_name in output

def start_or_restart_container(container_name, run_command_str):
    """Start the container if it doesn't exist, restart if it's stopped."""
    if container_running(container_name):
        print(f"[✔] {container_name} is already running.")
    elif container_exists(container_name):
        print(f"[*] {container_name} exists but is stopped. Restarting...")
        run_command(f"docker start {container_name}")
    else:
        print(f"[*] Starting {container_name}...")
        run_command(run_command_str)

def start_zookeeper():
    """Start or restart Zookeeper."""
    start_or_restart_container(
        ZOOKEEPER_CONTAINER,
        f"docker run -d --name {ZOOKEEPER_CONTAINER} --network host "
        f"-e ALLOW_ANONYMOUS_LOGIN=yes "
        f"bitnami/zookeeper:latest"
    )

def start_kafka():
    """Start or restart Kafka with correct configurations."""
    start_or_restart_container(
        KAFKA_CONTAINER,
        f"docker run -d --name {KAFKA_CONTAINER} --network host "
        f"-e KAFKA_ZOOKEEPER_CONNECT=localhost:2181 "
        f"-e KAFKA_ADVERTISED_LISTENERS=PLAINTEXT://localhost:9092 "
        f"-e KAFKA_CFG_LISTENER_SECURITY_PROTOCOL_MAP=PLAINTEXT:PLAINTEXT "
        f"bitnami/kafka:latest"
    )

def wait_for_kafka():
    """Wait for Kafka to be ready."""
    print("[*] Waiting for Kafka to start...")
    time.sleep(30)  # Increased wait time for stability

def topic_exists(topic):
    """Check if a Kafka topic already exists using the correct path."""
    topics = run_command(f"docker exec {KAFKA_CONTAINER} /opt/bitnami/kafka/bin/kafka-topics.sh --list --bootstrap-server localhost:9092")
    return topic in topics.split("\n")

def create_topics():
    """Create Kafka topics if they don't already exist."""
    for topic in KAFKA_TOPICS:
        if topic_exists(topic):
            print(f"[✔] Topic '{topic}' already exists. Skipping...")
        else:
            print(f"[*] Creating topic '{topic}'...")
            run_command(f"docker exec {KAFKA_CONTAINER} /opt/bitnami/kafka/bin/kafka-topics.sh --create --topic {topic} --bootstrap-server localhost:9092 --partitions 1 --replication-factor 1")
            print(f"[✔]Topic Created......")
            run_command(f"docker exec {KAFKA_CONTAINER} kafka-topics.sh --list --bootstrap-server localhost:9092")

def setup_kafka():
    """Complete Kafka setup with Zookeeper, Kafka, and topic creation."""
    start_zookeeper()
    start_kafka()
    wait_for_kafka()
    create_topics()
    print("[✔] Kafka setup complete!")

if __name__ == "__main__":
    setup_kafka()
