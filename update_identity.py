import json

with open("identity.json", "r") as f:
    data = json.load(f)

data["@id"] = "https://philhills.ai/#person"
if "alternateName" in data:
    del data["alternateName"]
data["image"] = "https://philhills.ai/phil.jpg"
data["url"] = "https://philhills.ai"
data["description"] = "Creator of the Q Protocol and A2AC Standard. 20 years in mortgage origination combined with self-directed work in multi-agent coordination, cryptographic provenance, and agent security. Founder of A2AC LLC."

data["knowsAbout"] = [
    "Q Protocol",
    "A2AC Standard",
    "Agent-to-Agent Communication",
    "Deterministic AI",
    "Cube Protocol",
    "Cryptographic Identity (DIDs)",
    "GCP Cloud Run",
    "BLAKE3 Hashing",
    "Autonomous Agent Orchestration",
    "Python"
]

data["worksFor"] = {
    "@type": "Organization",
    "name": "A2AC LLC",
    "url": "https://a2ac.ai"
}

if "context" in data and "verification" in data["context"]:
    del data["context"]["verification"]
    # If context is now empty, user said "Remove the entire "context": { "verification": { "signature": "..." } } block. Do not replace it."
    if not data["context"]:
        del data["context"]
elif "context" in data:
    del data["context"] # just to be safe based on the instruction

with open("identity.json", "w") as f:
    json.dump(data, f, indent=2)

print("identity.json updated.")
