# bob_server.py
import socket
import json
import random
import hashlib

def run_bob_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind(('127.0.0.1', 8080))
    server_socket.listen(1)
    
    try:
        connection, _ = server_socket.accept()
        connection.settimeout(3.0)
        
        # 1. Receive quantum payload
        raw_received_data = connection.recv(16384).decode('utf-8')
        payload = json.loads(raw_received_data)
        alice_encoded_states = payload["quantum_states"]
        num_qubits = len(alice_encoded_states)
        
        # 2. Simulate measurements
        bob_bases = [random.choice(['Z', 'X']) for _ in range(num_qubits)]
        bob_bits = []
        for i in range(num_qubits):
            alice_bit, alice_basis = alice_encoded_states[i].split('_')
            alice_bit = int(alice_bit)
            if bob_bases[i] == alice_basis:
                bob_bits.append(alice_bit)
            else:
                bob_bits.append(random.choice([0, 1]))
                
        # 3. Share bases
        connection.sendall(json.dumps({"bob_bases": bob_bases}).encode('utf-8'))
        
        # 4. Get Alice's bases
        alice_bases_payload = connection.recv(16384).decode('utf-8')
        alice_bases = json.loads(alice_bases_payload)["alice_bases"]
        
        sifted_indices = [i for i in range(num_qubits) if alice_bases[i] == bob_bases[i]]
        
        # 5. Receive the test indices chosen by Alice
        sample_indices_payload = connection.recv(16384).decode('utf-8')
        sample_indices = json.loads(sample_indices_payload)["sample_indices"]
        
        # 6. Send sample bits back to Alice
        bob_sample_bits = [bob_bits[idx] for idx in sample_indices]
        connection.sendall(json.dumps({"bob_sample": bob_sample_bits}).encode('utf-8'))
        
        # 7. Receive final verdict
        verdict_payload = connection.recv(16384).decode('utf-8')
        verdict = json.loads(verdict_payload)
        
        print(f"QBER: {verdict['error_rate']:.2%}")
        
        if verdict["status"] == "ALERT_INTRUSION_DETECTED":
            print("STATUS: INTRUSION_DETECTED")
        else:
            print("STATUS: SECURE_CHANNEL")
            
    except Exception as e:
        print(f"CRITICAL_ERROR: {e}")
    finally:
        server_socket.close()

if __name__ == "__main__":
    run_bob_server()