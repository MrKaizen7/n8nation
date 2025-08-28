#!/bin/bash
# N8Nation Knowledge Base Auto-Updater
# Save this as: /workspaces/n8n_local_docker_ngrok/n8nation/docs/ai-copilot/auto_update.sh

# Setup environment
cd "$(dirname "$0")"
export GOOGLE_API_KEY="${GOOGLE_API_KEY}"

# Log file
LOG_FILE="knowledge_updates.log"

echo "$(date): Starting knowledge base update" >> $LOG_FILE

# Run updater
python3 knowledge_updater.py >> $LOG_FILE 2>&1

# Check if successful
if [ $? -eq 0 ]; then
    echo "$(date): Update completed successfully" >> $LOG_FILE
else
    echo "$(date): Update failed" >> $LOG_FILE
fi

echo "$(date): Auto-update cycle finished" >> $LOG_FILE
echo "----------------------------------------" >> $LOG_FILE
