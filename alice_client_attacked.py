# alice_client.py
import socket
import json
import random

def run_alice_client():
    NUM_QUBITS = 100  
    
    alice_bits = [random.choice([0, 1]) for _ in range(NUM_QUBITS)]
    alice_bases = [random.choice(['Z', 'X']) for _ in range(NUM_QUBITS)]
    
    quantum_states_payload = [f"{alice_bits[i]}_{alice_bases[i]}" for i in range(NUM_QUBITS)]
    
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('127.0.0.1', 8081)) 
    
    try:
        payload = {"quantum_states": quantum_states_payload}
        client_socket.sendall(json.dumps(payload).encode('utf-8'))
        
        bob_bases_payload = client_socket.recv(16384).decode('utf-8')
        bob_bases = json.loads(bob_bases_payload)["bob_bases"]
        client_socket.sendall(json.dumps({"alice_bases": alice_bases}).encode('utf-8'))
        
        sifted_indices = [i for i in range(NUM_QUBITS) if alice_bases[i] == bob_bases[i]]
        
        sample_size = min(20, len(sifted_indices))
        sample_indices = random.sample(sifted_indices, sample_size)
        
        client_socket.sendall(json.dumps({"sample_indices": sample_indices}).encode('utf-8'))
        
        bob_sample_payload = client_socket.recv(16384).decode('utf-8')
        bob_sample_bits = json.loads(bob_sample_payload)["bob_sample"]
        
        alice_sample_bits = [alice_bits[idx] for idx in sample_indices]
        mismatched_bits = sum(1 for a, b in zip(alice_sample_bits, bob_sample_bits) if a != b)
        error_rate = mismatched_bits / sample_size if sample_size > 0 else 0
        
        if error_rate > 0.11:
            verdict = {"status": "ALERT_INTRUSION_DETECTED", "error_rate": error_rate}
        else:
            verdict = {"status": "CHANNEL_CLEAN", "error_rate": error_rate}
            
        client_socket.sendall(json.dumps(verdict).encode('utf-8'))
        
    except Exception as e:
        pass
    finally:
        client_socket.close()

if __name__ == "__main__":
    run_alice_client()