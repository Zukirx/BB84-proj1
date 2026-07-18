# Quantum-Safe Network Socket Pipeline (BB84 Protocol Emulation)

An empirical validation and simulation framework demonstrating **Quantum Key Distribution (QKD)** over standard distributed network architectures. This project models the physics of state vector collapse, sifting mechanisms, anomaly detection, and privacy amplification to establish information-theoretic security against an active adversary.

---

## Project Architecture & Security+ Alignment

This framework bridges the gap between quantum mechanics proofs and practical network infrastructure, mapping explicitly to **CompTIA Security+** domains:

* **Out-of-Band Key Exchange (Domain 2.0/3.0):** Emulates a secure quantum link to generate symmetric cryptographic key pools without transmitting the actual key material over public channels.
* **Anomaly-Based Intrusion Detection (IDS):** Implements a real-time statistical thermometer check. If the Quantum Bit Error Rate (QBER) breaks the theoretical boundary, the system flags a wiretap and fails secure.
* **Privacy Amplification:** Leverages the **avalanche effect** of the SHA-256 hashing algorithm to destroy partial information leakage, reducing an eavesdropper's stolen data utility to absolute zero.

---

## Empirical Verification & Replication Targets

This software acts as a validation test suite designed to replicate landmark QKD academic benchmarks:

1. **The Sifting Yield Boundary (50% Convergence):** Proves that Bob's random measurement bases align with Alice's encoding parameters exactly $50\%$ of the time over large scales.
2. **The Intercept-Resend Footprint (25% Threat Signature):** Validates that an active eavesdropper (Eve) intercepting the quantum channel inevitably introduces an explicit $25\%$ error rate into the sifted key pools.
3. **The Shor-Preskill Security Cutoff (11% Limit):** Enforces a hard systemic boundary that halts the pipeline if the calculated sample error ticks above $11\%$, blocking public data leakage during error correction.

---

## Directory Blueprint

```text
├── alice_client.py     # Transmitting Node (Encodes quantum state vectors)
├── bob_server.py       # Receiving/Measurement Node (Handles TCP ports & sifting matrix)
├── eve_proxy.py        # MitM Threat Interceptor (Injects wavefunction collapse anomalies)
├── run_experiment.py   # Automated Test Harness (Gathers metrics & outputs CSV logs)
└── README.md           # Documentation & Architectural Blueprint