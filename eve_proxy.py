# eve_proxy.py
import socket
import json
import random

def run_eve_proxy():
    ALICE_PORT = 8081  
    BOB_PORT = 8080    
    
    proxy_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    proxy_server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    proxy_server.bind(('127.0.0.1', ALICE_PORT))
    proxy_server.listen(1)
    
    try:
        alice_conn, _ = proxy_server.accept()
        raw_alice_data = alice_conn.recv(16384).decode('utf-8')
        payload = json.loads(raw_alice_data)
        alice_encoded_states = payload["quantum_states"]
        num_qubits = len(alice_encoded_states)
        
        # Intercept-Resend state collapse injection
        eve_bases = [random.choice(['Z', 'X']) for _ in range(num_qubits)]
        eve_tampered_states = []
        for i in range(num_qubits):
            alice_bit, alice_basis = alice_encoded_states[i].split('_')
            alice_bit = int(alice_bit)
            measured_bit = alice_bit if eve_bases[i] == alice_basis else random.choice([0, 1])
            eve_tampered_states.append(f"{measured_bit}_{eve_bases[i]}")
            
        # Connect to Bob
        bob_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        bob_client.connect(('127.0.0.1', BOB_PORT))
        
        # Forward corrupted quantum stream
        forward_payload = {"quantum_states": eve_tampered_states}
        bob_client.sendall(json.dumps(forward_payload).encode('utf-8'))
        
        # Proxy Phase 1: Pass Bob's bases to Alice
        raw_bob_bases = bob_client.recv(16384)
        alice_conn.sendall(raw_bob_bases)
        
        # Proxy Phase 2: Pass Alice's bases to Bob
        raw_alice_bases = alice_conn.recv(16384)
        bob_client.sendall(raw_alice_bases)
        
        # Proxy Phase 3: Pass Alice's sample indices to Bob
        raw_sample_indices = alice_conn.recv(16384)
        bob_client.sendall(raw_sample_indices)
        
        # Proxy Phase 4: Pass Bob's sample bits to Alice
        raw_bob_sample = bob_client.recv(16384)
        alice_conn.sendall(raw_bob_sample)
        
        # Proxy Phase 5: Pass Alice's final security verdict to Bob
        raw_verdict = alice_conn.recv(16384)
        bob_client.sendall(raw_verdict)
        
    except Exception as e:
        pass
    finally:
        proxy_server.close()
        try:
            bob_client.close()
        except:
            pass

if __name__ == "__main__":
    run_eve_proxy()