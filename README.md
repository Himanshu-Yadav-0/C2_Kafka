# C2 Kafka Project

This project is a **Command & Control (C2) system** using **Confluent Kafka, Flask, and Termux**. It enables remote command execution on target devices via a distributed Kafka-based architecture.

## 🔹 Current Project Status
- ✅ Git repository initialized & connected to GitHub.
- ✅ Virtual environment (`venv`) set up.
- ✅ Git branching system established.
- ⏳ Kafka setup in progress.

## 🔹 Git Branching Strategy
To maintain a structured and production-level workflow, we follow this branching strategy:

### **Main Branches**
- **`main`** → Stable, production-ready code. No direct commits.
- **`develop`** → Latest working version where all features are merged before reaching `main`.

### **Feature & Bugfix Branches**
- **`feature/<feature-name>`** → New features are developed here before merging into `develop`.
  - Example: `feature/kafka-setup`
- **`bugfix/<bug-name>`** → Bug fixes are handled separately to avoid breaking stable code.
  - Example: `bugfix/fix-kafka-timeout`

### **How to Work on a Feature**
1. Create a new feature branch:
   ```sh
   git checkout -b feature/<feature-name>
   git push origin feature/<feature-name>
   ```
2. Work on the feature and commit changes.
3. Once done, create a **Pull Request (PR) to `develop`**.
4. After review & testing, the feature is merged into `develop`.

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

