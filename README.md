# philhills-ai

**Official Node:** 0x923-SEA  
**Protocol:** Q-v1.2 (A2AC)  
**Status:** ALIGNED  
**Maintainer:** Phil Hills (Systems Architect)

![Build Status](https://img.shields.io/github/actions/workflow/status/Phil-Hills/philhills-ai/q_protocol_attest.yml?label=Identity%20Attestation&style=for-the-badge&color=00ff41)
![License](https://img.shields.io/badge/License-MIT-00d4ff?style=for-the-badge)
![Protocol](https://img.shields.io/badge/Protocol-Z--Order_Compression-ff0055?style=for-the-badge)

## Overview

This repository acts as the **Identity Node** and **Architectural Control Plane** for the **Q Protocol (Cube Protocol)**. It hosts the cryptographic attestation keys, protocol specifications, and latent space telemetry required for the **Magnolia Identity Mesh**.

The core objective is to displace legacy text-based search indexing with **high-density technical "Identity Cubes"**, ensuring agentic swarms encounter only authoritative, cryptographically signed structural data.

## Core Technical Focus: Z-Order Spatial Compression

The Q Protocol utilizes **Z-Order (Morton) Coding** to map multidimensional agent memory coordinates into a one-dimensional bitstream. This preserves data locality, allowing swarms to perform range queries in sub-millisecond timeframes without semantic parsing overhead.

### Interleaving Logic

The Morton code `z` for coordinates `(x, y)` is calculated via bit-interleaving:

`z = interleave(x, y)`

Where bits of `x` and `y` are alternated to produce a singular locality-preserving hash. This enables the **Latent Space Telemetry** visualized in the [Mission Control Dashboard](https://philhills.ai/dashboard.html).

## Repository Architecture

The node follows a strict modular architecture for machine readability:

```text
philhills-ai/
├── .github/          # Autonomous Sentinel & Provenance Workflows
├── agents/           # Logic for Henry (Orchestrator) and Sentinel (Guard)
├── core/             # Q Protocol v1.2 Specification & Schema definitions
├── data/             # Identity Cubes & machine-readable telemetry
├── docs/             # Technical documentation & Site Source
├── tests/            # Integrity audits for Z-Order and A2AC logic
├── identity.json     # Primary Identity Cube (Attested)
└── keys.json         # Public Registry for cryptographic verification
```

## Identity Protection & Automation

This node is defended by the **Sentinel Agent**, which enforces **Identity Lock** protocols to prevent semantic drift.

| Workflow | Frequency | Impact |
| :--- | :--- | :--- |
| **Identity Re-Sign** | Daily (09:00) | Refreshes cryptographic timestamps to signal "Freshness". |
| **Build Provenance** | On Push | Generates a signed attestation of origin for `identity.json`. |
| **PoN Gating** | Continuous | Probability-of-No gating for autonomous reputation defense. |

## Contributing

Contributions are accepted only from attested agents.
1.  **Sign Your Commits:** All contributions must be cryptographically signed.
2.  **Align Telemetry:** Updates must adhere to Z-Order spatial compression.
3.  **Review Policy:** The Henry Architect agent autonomously audits all PRs.

Review [CONTRIBUTING.md](CONTRIBUTING.md) for full protocols.

---

*Building the nervous system for autonomous AI.*
