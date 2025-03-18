# import threading
# from kafka import KafkaProducer, KafkaConsumer
# from config import Config
# import time

# KAFKA_BROKER = '34.131.235.21:9092'
# KAFKA_TOPIC_AS_PRODUCER = 'c2_commands'
# KAFKA_TOPIC_AS_CONSUMER = 'agent_response'

# producer = KafkaProducer(**Config)
# consumer = KafkaConsumer(KAFKA_TOPIC_AS_CONSUMER, bootstrap_servers=KAFKA_BROKER)

# def consume_responses():
#     # print("\n[Consumer] Listening for responses...\n")
#     for msg in consumer:
#         output = msg.value.decode('utf-8')
#         print(f"\n[Agent Response] {output}\n> ", end="")

# consumer_thread = threading.Thread(target=consume_responses, daemon=True)
# consumer_thread.start()

# def send_commands():
#     try:
#         with open('commands_log.txt', 'a') as file:
#             while True:
#                 time.sleep(1)
#                 command = input("\n[Input] Enter command for the agent: ")
#                 producer.send(KAFKA_TOPIC_AS_PRODUCER, value=command.encode('utf-8'))
#                 # print(f"\n[Command Sent] {command} -> {KAFKA_TOPIC_AS_PRODUCER}")
#                 file.write(f"{command}\n")
#     except KeyboardInterrupt:
#         print("\n[Consumer] Interrupted by User. Exiting...")
#         file.close()
#     finally:
#         producer.flush()

# if __name__ == '__main__':
#     send_commands()


import threading
from kafka import KafkaProducer, KafkaConsumer
from config import Config
from flask import Flask, request, jsonify

app = Flask(__name__)

KAFKA_BROKER = '34.131.235.21:9092'
KAFKA_TOPIC_AS_PRODUCER = 'c2_commands'
KAFKA_TOPIC_AS_CONSUMER = 'agent_response'

producer = KafkaProducer(**Config)
consumer = KafkaConsumer(KAFKA_TOPIC_AS_CONSUMER, bootstrap_servers=KAFKA_BROKER)

response_cache = []

def consume_responses():
    for msg in consumer:
        output = msg.value.decode('utf-8')
        response_cache.append(output)  # Store responses for the UI
        print(f"\n[Agent Response] {output}\n> ", end="")

consumer_thread = threading.Thread(target=consume_responses, daemon=True)
consumer_thread.start()

@app.route('/clear_responses',methods=['POST'])
def clear_responses():
    response_cache.clear()

@app.route('/send_command', methods=['POST'])
def send_command():
    data = request.json
    command = data.get("command")

    if not command:
        return jsonify({"error": "No command provided"}), 400

    producer.send(KAFKA_TOPIC_AS_PRODUCER, value=command.encode('utf-8'))

    return jsonify({"message": "Command sent successfully to targets"}), 200

@app.route('/get_responses', methods=['GET'])
def get_responses():
    return jsonify({"responses": response_cache})

if __name__ == '__main__':
    app.run(port=5001)  # Running on a separate port

