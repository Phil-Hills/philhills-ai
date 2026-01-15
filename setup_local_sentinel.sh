#!/bin/bash
# Local Sentinel Automation Setup
# Installs a daily crontab entry for reputation_sentinel.py

# 1. Resolve Paths
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SENTINEL_SCRIPT="$SCRIPT_DIR/reputation_sentinel.py"
PYTHON_BIN=$(which python3)
LOG_FILE="$SCRIPT_DIR/sentinel_audit.log"

if [ -z "$PYTHON_BIN" ]; then
    echo "❌ Python 3 not found in PATH."
    exit 1
fi

# 2. Prepare Cron Command
# Runs daily at 9:00 AM local time
# Sourcing .env if it exists to load API Keys
CRON_CMD="0 9 * * * cd $SCRIPT_DIR && source .env 2>/dev/null; $PYTHON_BIN $SENTINEL_SCRIPT >> $LOG_FILE 2>&1"

# 3. Install Crontab
echo "🛡️  Installing Reputation Sentinel into Crontab..."
echo "   Target: $SENTINEL_SCRIPT"
echo "   Log:    $LOG_FILE"

# Backup existing cron
crontab -l > mycron_backup 2>/dev/null

# Check if job already exists to avoid duplicates
if grep -q "reputation_sentinel.py" mycron_backup 2>/dev/null; then
    echo "⚠️  Job already exists in crontab. Skipping addition."
else
    # Append new job
    echo "$CRON_CMD" >> mycron_backup
    # Install new cron file
    crontab mycron_backup
    echo "✅ Success: Sentinel scheduled for daily execution @ 09:00."
fi

rm mycron_backup

# 4. Immediate Test
echo "🧪 Running immediate test (dry-run)..."
$PYTHON_BIN $SENTINEL_SCRIPT
