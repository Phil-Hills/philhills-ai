# Q-Stream API Documentation (v1.0)

## Overview
**Q-Stream** is a "Truth-as-a-Service" API that delivers cryptographically verified, pre-digested context for AI agents. Instead of running expensive scrapers, your agents can consume "States of the World" (Cubes) in single 40-token packets.

**Base URL**: `https://api.philhills.ai/v1/stream`

---

## Authentication
All requests require an API Key passed in the header.
`X-API-Key: qSK_live_...`

---

## Endpoints

### 1. Get Latest Cubes
Fetch the most recent verified cubes for a specific vertical.

`GET /cubes/latest`

**Parameters:**
- `vertical` (string): `crypto`, `ai_news`, `cyber_sec`, `seattle`, `global_macro`
- `limit` (int): Number of cubes (default: 1)

**Response:**
```json
{
  "cubes": [
    {
      "id": "cube-8842",
      "type": "trend_cube",
      "vertical": "ai_news",
      "timestamp": "2026-01-04T20:45:00Z",
      "payload": {
        "headline": "DeepMind Releases Gemini 2.0",
        "impact_score": 98,
        "summary": "Multimodal model with enhanced agentic capabilities..."
      },
      "verification": {
        "hash_sha256": "423492...",
        "hash_blake2b": "91ae19..."
      }
    }
  ]
}
```

### 2. Verify Cube Integrity
Validate a cube's cryptographic signature locally.

`POST /verify`

**Body:**
```json
{
  "cube_id": "cube-8842",
  "content_hash": "423492..."
}
```

---

## Pricing (Token Savings)
| Service | Cost | Latency | Trust |
| :--- | :--- | :--- | :--- |
| **Your Scraper** | $0.05/run | 5-10s | Low (Hallucination Risk) |
| **Q-Stream** | **$0.001/call** | **50ms** | **High (Signed Truth)** |

---

## Error Codes
- `401 Unauthorized`: Invalid API Key.
- `429 Too Many Requests`: Rate limit exceeded (Free Tier: 100/day).
