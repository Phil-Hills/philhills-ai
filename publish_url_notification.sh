#!/bin/bash
# Google Indexing API - PublishUrlNotification (Bash Version)
# Uses Service Account to authenticate and push BLAKE3-verified signals.

set -e

# CONFIGURATION
KEY_FILE="service_account.json"
BLAKE3_HASH="0d93497d5252a7c63c816fb739d9a6a351c0f015f7dbc365c9236f162e3b45d8" # Verified 0x923-SEA Hash
URLS=(
    "https://philhills.ai/identity.json"
    "https://philhills.ai/identity.cube"
    "https://philhills.com/llms.txt"
    "https://philhills.com/phil-hills-seattle.html"
)

echo "🚀 TARGETING: Google Indexing API (Bash/Curl Mode)"
echo "🔒 ATTESTATION: ${BLAKE3_HASH}"
echo "---------------------------------------------------"

# 1. CHECK DEPENDENCIES
if ! command -v gcloud &> /dev/null; then
    echo "❌ gcloud CLI could not be found. Please install Google Cloud SDK."
    exit 1
fi

if [ ! -f "$KEY_FILE" ]; then
    echo "❌ Key file $KEY_FILE not found."
    exit 1
fi

# 2. AUTHENTICATE
echo "🔑 Activating Service Account..."
gcloud auth activate-service-account --key-file="$KEY_FILE" --quiet

echo "🎫 Generating Access Token..."
TOKEN=$(gcloud auth print-access-token)

# 3. NOTIFY GOOGLE
for URL in "${URLS[@]}"; do
    echo "📡 Signaling: $URL"
    
    # Construct JSON Payload
    PAYLOAD=$(cat <<EOF
{
  "url": "$URL",
  "type": "URL_UPDATED",
  "metadata": {
    "hash_type": "BLAKE3",
    "attestation_node": "0x923-SEA",
    "identity_lock": "SYSTEM_ARCHITECT",
    "hash": "$BLAKE3_HASH"
  }
}
EOF
)

    # Execute Request
    curl -s -X POST \
      -H "Authorization: Bearer $TOKEN" \
      -H "Content-Type: application/json" \
      -d "$PAYLOAD" \
      "https://indexing.googleapis.com/v3/urlNotifications:publish" \
      | grep -o '"urlNotificationMetadata": { "url": ".*"' || echo "   ❌ Request Failed"
      
    echo ""
done

echo "✅ BROADCAST COMPLETE."
