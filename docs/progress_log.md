## [15-March-2025] Kafka & Zookeeper Setup Complete
- Automated Kafka setup script created.
- Script now:
  - Checks for existing containers.
  - Starts Zookeeper & Kafka if needed.
  - Creates required Kafka topics (`c2_commands`, `agent_response`).
- Verified everything is working.

## [16-March-2025] Debugging & Fixing Kafka Setup Issues
- Encountered issues with Kafka container crashing.
- Switched to Bitnami Kafka & Zookeeper images.
- Fixed missing environment variables:
  - Added `ALLOW_ANONYMOUS_LOGIN=yes` for Zookeeper.
  - Added `KAFKA_CFG_LISTENER_SECURITY_PROTOCOL_MAP=PLAINTEXT:PLAINTEXT` for Kafka.
- Increased wait time before creating topics to ensure Kafka is fully initialized.
- Verified that topics are created successfully after script execution.
- Tested manual topic creation & deletion commands to confirm stability.

