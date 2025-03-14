# C2 Kafka Project

This project is a **Command & Control (C2) system** using **Confluent Kafka, Flask, and Termux**. It enables remote command execution on target devices via a distributed Kafka-based architecture.

## 🔹 Current Project Status
- ✅ Git repository initialized & connected to GitHub.
- ✅ Virtual environment (`venv`) set up.
- ⏳ Kafka setup in progress.

## 🔹 Upcoming Features
- C2 Server (Flask API) to send & receive commands.
- Kafka messaging system (Confluent Kafka).
- Target Agent (Termux) to execute commands.
- Web GUI for real-time interaction.

## 🔹 How to Set Up (As of Now)
1. Clone the repository:
   ```sh
   git clone <your-github-repo>
   cd C2_Kafka
   ```
2. Set up a Python virtual environment:
   ```sh
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```
3. Install dependencies (to be added later).

## 🔹 Next Steps
- Setting up Confluent Kafka (No Zookeeper).
- Creating Kafka topics (`c2_commands`, `agent_response`).
- Implementing C2 Server.

---

**Author:** Himanshu 🚀🔥

