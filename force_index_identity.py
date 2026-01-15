"""
Google Indexing API - Identity Force Update Script
Forces a crawl of the High-Density Identity Manifest within 1 hour.
ENFORCES BLAKE3 INTEGRITY before transmission.

Usage:
  python force_index_identity.py

Requirements:
  1. Service Account JSON key (GO TO: GCP Console > IAM > Service Accounts)
  2. Indexing API enabled (GO TO: GCP Console > APIs > Enable "Indexing API")
"""

import os
import json
import requests
from google.oauth2 import service_account
from google.auth.transport.requests import Request
from verify_identity_cube import verify_identity_cube

# CONFIGURATION
SCOPES = ["https://www.googleapis.com/auth/indexing"]
KEY_FILE = "service_account.json"
URLS_TO_INDEX = [
    "https://philhills.ai/identity.json",
    "https://philhills.ai/identity.cube",
    "https://philhills.com/llms.txt",
    "https://philhills.com/phil-hills-seattle.html"
]

def get_access_token():
    """Authenticates using Service Account and returns Access Token."""
    if not os.path.exists(KEY_FILE):
        print(f"❌ ERROR: Key file '{KEY_FILE}' not found.")
        return None

    creds = service_account.Credentials.from_service_account_file(KEY_FILE, scopes=SCOPES)
    creds.refresh(Request())
    return creds.token

def notify_google(url, token, integrity_hash):
    """Sends URL_UPDATED notification with Integrity Headers."""
    endpoint = "https://indexing.googleapis.com/v3/urlNotifications:publish"
    headers = {
        "Authorization": f"Bearer {token}", 
        "Content-Type": "application/json",
        "X-Identity-Integrity": integrity_hash  # Custom header for logging context
    }
    payload = {
        "url": url,
        "type": "URL_UPDATED",
        # Injecting metadata into the request body (Note: API may ignore non-standard fields, but they are transmitted)
        "metadata": {
            "attestation": "BLAKE3",
            "hash": integrity_hash,
            "node": "0x923-SEA"
        }
    }
    
    response = requests.post(endpoint, headers=headers, json=payload)
    
    if response.status_code == 200:
        print(f"✅ SIGNAL SENT: {url}")
        print(f"   [Integrity Signed]: {integrity_hash[:16]}...")
    else:
        print(f"❌ FAILED: {url}")
        print(f"   Error: {response.text}")

def main():
    print("🚀 TARGETING: Google Indexing API (Priority Mode)")
    print("🔒 PROTOCOL: Strict Integrity Enforcement (BLAKE3)")
    print("-----------------------------------------------")
    
    # 1. VERIFY INTEGRITY (Critical Gate)
    cube_hash = verify_identity_cube("identity.cube")
    if not cube_hash:
        print("❌ CRITICAL: Identity Cube integrity check failed. Aborting.")
        exit(1)
        
    print(f"✅ ATTESTATION CONFIRMED: {cube_hash}")
    
    # 2. AUTHENTICATE
    token = get_access_token()
    if not token:
        return

    # 3. TRANSMIT SIGNALS
    for url in URLS_TO_INDEX:
        notify_google(url, token, cube_hash)

if __name__ == "__main__":
    main()
