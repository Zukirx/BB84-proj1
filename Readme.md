# Quantum-Safe Key Distribution and Threat Emulation Surface

An empirical full-stack simulation framework modeling Quantum Key Distribution (QKD) via the BB84 protocol over an unsecure channel. This system demonstrates information-theoretic security boundaries, environmental fiber-optic signal degradation, and automated anomaly-based Intrusion Detection System (IDS) alerts based on the Shor-Preskill security limit.

## Architectural Overview

The application is structured as a full-stack platform consisting of an asynchronous Python backend API (Flask) paired with a responsive, high-fidelity real-time telemetry front-end dashboard (HTML5, CSS3, Vanilla JavaScript). 

Instead of relying on public-key mathematical complexity which is vulnerable to Shor's algorithm on quantum computers, this architecture simulates the exchange of quantum states represented by polarized photons across a physical fiber-optic link. Eavesdropping on this link collapses the state vector, introducing an unavoidable statistical fingerprint that is analyzed in real time.

## Core Features and Mechanics

### 1. Quantum State Encoding and Filtering
Alice generates random binary streams and translates them into specific polarization states using two conjugate bases:
* Rectilinear Basis (Z): Horizontal polarization represents bit 0, Vertical polarization represents bit 1.
* Diagonal Basis (X): 45-degree tilt represents bit 0, 135-degree tilt represents bit 1.

### 2. Fiber-Optic Environmental Disruption Noise
The simulation accounts for real-world physical line constraints such as thermal fluctuations, dark counts, and polarization rotation. A baseline noise parameter (set to 3%) randomly shifts the polarization state vector properties during flight down the channel. This replicates the minor natural error rates seen in clean, authentic networks before any adversarial tampering occurs.

### 3. Intercept-Resend Eavesdropping Simulation (Eve Proxy)
The adversary vector replicates the physics of the No-Cloning Theorem. Eve cannot clone or clone-and-intercept a flying state without measuring it first. When active, she forces a wavefunction collapse by checking the data frames using blindly guessed bases. If her guess mismatches Alice's configuration, the data angle snaps randomly, destroying the original transmission footprints.

### 4. Classical Sifting Matrix
Upon receiving the telemetry pulses, Bob randomly selects his measurement filters. Alice and Bob then communicate over a public classical channel to cross-reference only the names of the filters they utilized, discarding all bit positions where their measurement bases diverged.

### 5. Dynamic Anomaly-Based Intrusion Detection System
To verify line integrity, the system automatically slices out a dynamic sample subset representing exactly 20% of the sifted key pool to calculate the Quantum Bit Error Rate (QBER). 
* Clean Line State: QBER hovers safely between 1% and 5% due to natural fiber noise.
* Intercepted State: Eve's activity guarantees a mathematical error injection baseline of approximately 25%.
* Threshold Rule: If the calculated error rate breaches the strict 11% Shor-Preskill boundary, an intrusion alert trips, blocking key compilation and purging all volatile memory buffers.

### 6. Privacy Amplification
For keys that pass verification below the threshold, remaining data blocks are processed through a cryptographic SHA-256 hash function. This leverages the avalanche effect to reduce any partial statistical information an attacker might have leaked down to absolute zero.

## Project Directory Structure

```text
├── server.py          # Flask Web Engine & Core BB84 Protocol Simulator
├── requirements.txt  # Production dependencies manifest
├── templates/
│   └── index.html     # Dashboard User Interface DOM Frame Structure
└── static/
    ├── style.css      # Cyberpunk Monitoring Theme Layout Styles
    └── app.js         # Asynchronous API Handler & Telemetry Renderer


  ##  Link: https://quantum-key-exchange-simulator.onrender.com