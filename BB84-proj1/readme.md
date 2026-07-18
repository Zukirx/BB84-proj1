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