# C2 Kafka Project

This project is a **Command & Control (C2) system** built using **Kafka, Flask**. It enables remote command execution on target devices through a distributed Kafka-based architecture. Users can send commands via a web interface, and responses from agents are displayed in real-time.


## 🛠️ How It Works
1. **Users** send commands via the Web UI.
2. The **C2 server** acts as a Kafka producer, publishing commands to the `c2_commands` topic.
3. The **Agent**, running on a remote system, consumes commands from `c2_commands`, executes them, and sends responses to the `agent_response` topic.
4. The **C2 server** listens to `agent_response` and pushes the output to the Web UI in real-time.

## 📂 Project Structure
```
C2_Kafka_Project/
│── agent/                # Agent script running on target machines
│   ├── agent.py
│
│── c2_server/            # Backend API handling commands
│   ├── c2_server.py
│   ├── config.py
│
│── kafka_setup/          # Kafka setup and configuration
│   ├── setup_kafka.py
│
│── web_gui/              # Web UI for user interaction
│   ├── templates/
│   │   ├── index.html    # Frontend page
│   ├── app.py           # Flask-based Web UI backend
│
│── venv/                 # Virtual environment
│── README.md             # Project documentation
```

## 🔧 Setup & Execution
### 1️⃣ Prerequisites
- Python 3.x installed
- Kafka set up and running (on GCP VM)
- Docker installed (if containerizing)

### 2️⃣ Clone the Repository
```sh
git clone https://github.com/Himanshu-Yadav-0/C2_Kafka
cd C2_Kafka
```

### 3️⃣ Install Dependencies
```sh
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```
## 🖥️ Running Everything on Cloud

### 4️⃣ Start Kafka (On Your Cloud VM)
If Kafka is not running, start it using Docker:
```sh
docker start <name of your kafka container>
```
Also run Zookeeper with kafka.

### 5️⃣ Run the C2 Server (On Cloud VM)
```sh
cd c2_server
python c2_server.py
```

### 6️⃣ Run the Web UI (On Cloud VM)
```sh
cd web_gui
python app.py
```
Access the UI at `http://<vm-external-ip>:5000`

### 7️⃣ Run the Agent (On Target Device)
On the machine where commands will be executed:
```sh
cd agent
python agent.py
```

## 🖥️ Running Everything Locally
If you want to run the entire system on a local machine, follow these steps:

1️⃣ **Start Kafka Locally:**
```sh
docker start <kafka_container_name> & 
docker start <zookeeper_container_name>
```

2️⃣ **Run the C2 Server:**
```sh
cd c2_server
python c2_server.py
```

3️⃣ **Run the Web UI:**
```sh
cd web_gui
python app.py
```
Access the UI at `http://127.0.0.1:5000`

4️⃣ **Run the Agent on the Same Machine or Another Local Device:**
```sh
cd agent
python agent.py
```

Make sure your Kafka broker is properly configured to allow communication between these components.

## 🌍 Deployment on GCP
If deploying on a GCP VM, ensure that:
- Your firewall rules allow inbound traffic on required ports (Kafka, Flask UI, etc.)
- The Web UI listens on `0.0.0.0` to allow external access:
  ```python
  app.run(host='0.0.0.0', port=5000)
  ```
- The Kafka broker is accessible from both the C2 server and the agent.

## 🤝 Contributing
We welcome contributions! Feel free to:
- Improve the Web UI (React, better styling, real-time updates)
- Optimize Kafka producer-consumer logic
- Add authentication for secure access
- Report issues & suggest enhancements

## 📢 Final Notes
The project is now fully functional. Users must run `agent.py` on their target machine before using the C2 server.

For any queries or improvements, feel free to contribute!

My words: I know this documentation is trash but yea you know, at least it is there. Wanna talk about the project contact me at cyber.himanshuyadav@gmail.com

---
**Author:** Himanshu 🚀🔥
