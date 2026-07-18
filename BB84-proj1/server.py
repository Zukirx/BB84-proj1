# server.py
from flask import Flask, render_template, jsonify, request
import random
import hashlib

app = Flask(__name__)

def compute_bb84(n_qubits, active_eve):
    # Baseline fiber-optic noise rate (3% chance a photon undergoes environmental phase shift)
    FIBER_NOISE_RATE = 0.03

    # 1. Alice prepares states
    a_bits = [random.choice([0, 1]) for _ in range(n_qubits)]
    a_bases = [random.choice(['Z', 'X']) for _ in range(n_qubits)]
    alice_states = [f"{a_bits[i]}_{a_bases[i]}" for i in range(n_qubits)]
    
    # 2. Simulate Fiber Noise & Eve Interception Channel
    channel_states = []
    eve_bases = [random.choice(['Z', 'X']) for _ in range(n_qubits)] if active_eve else []
    eve_bits = []
    
    for i in range(n_qubits):
        bit, basis = alice_states[i].split('_')
        bit = int(bit)
        
        # --- PHASE A: Active MitM Attack (If selected) ---
        if active_eve:
            measured_bit = bit if eve_bases[i] == basis else random.choice([0, 1])
            eve_bits.append(measured_bit)
            current_bit = measured_bit
            current_basis = eve_bases[i]
        else:
            current_bit = bit
            current_basis = basis

        # --- PHASE B: Fiber-Optic Environmental Noise Simulation ---
        if random.random() < FIBER_NOISE_RATE:
            # Physical light disruption flips the polarization state vector properties randomly
            current_bit = 1 - current_bit if random.choice([True, False]) else current_bit
            current_basis = 'X' if current_basis == 'Z' else 'Z'
            
        channel_states.append(f"{current_bit}_{current_basis}")

    # 3. Bob Measures
    b_bases = [random.choice(['Z', 'X']) for _ in range(n_qubits)]
    b_bits = []
    for i in range(n_qubits):
        bit, basis = channel_states[i].split('_')
        bit = int(bit)
        measured_bit = bit if b_bases[i] == basis else random.choice([0, 1])
        b_bits.append(measured_bit)

    # 4. Sifting Matrix
    sifted_indices = [i for i in range(n_qubits) if a_bases[i] == b_bases[i]]
    
    # 5. Dynamic Statistical Calculator (20% sample pool sizing)
    total_sifted = len(sifted_indices)
    sample_size = max(1, int(total_sifted * 0.20)) if total_sifted > 0 else 0
    sample_indices = random.sample(sifted_indices, sample_size) if sample_size > 0 else []
    
    mismatches = sum(1 for idx in sample_indices if a_bits[idx] != b_bits[idx])
    qber = (mismatches / sample_size) if sample_size > 0 else 0.0
    intrusion_alert = qber > 0.11
    
    # 6. Final Privacy Amplification Hash
    remaining_indices = [idx for idx in sifted_indices if idx not in sample_indices]
    a_secret = [a_bits[idx] for idx in remaining_indices]
    b_secret = [b_bits[idx] for idx in remaining_indices]
    
    alice_hash = hashlib.sha256("".join(map(str, a_secret)).encode()).hexdigest() if a_secret else "N/A"
    bob_hash = hashlib.sha256("".join(map(str, b_secret)).encode()).hexdigest() if b_secret else "N/A"

    return {
        "num_qubits": n_qubits,
        "a_bits": a_bits, "a_bases": a_bases,
        "eve_bits": eve_bits, "eve_bases": eve_bases,
        "b_bits": b_bits, "b_bases": b_bases,
        "sifted_indices": sifted_indices, "sample_indices": sample_indices,
        "qber": round(qber * 100, 2),
        "intrusion_alert": intrusion_alert,
        "alice_hash": alice_hash,
        "bob_hash": bob_hash
    }

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/simulate', methods=['POST'])
def simulate():
    data = request.json
    n_qubits = int(data.get('num_qubits', 40))
    active_eve = bool(data.get('active_eve', True))
    results = compute_bb84(n_qubits, active_eve)
    return jsonify(results)

if __name__ == '__main__':
    app.run(debug=True, port=5000)