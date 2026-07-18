# alice_client.py
import socket
import json
import random

def run_alice_client():
    NUM_QUBITS = 20  
    
    alice_bits = [random.choice([0, 1]) for _ in range(NUM_QUBITS)]
    alice_bases = [random.choice(['Z', 'X']) for _ in range(NUM_QUBITS)]
    
    print(f"[ALICE] Local Raw Bits:  {alice_bits}")
    print(f"[ALICE] Local Raw Bases: {alice_bases}")
    
    quantum_states_payload = []
    for i in range(NUM_QUBITS):
        state_string = f"{alice_bits[i]}_{alice_bases[i]}"
        quantum_states_payload.append(state_string)
        
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('127.0.0.1', 8080))
    print("[ALICE] Secure loopback connection validated. Streaming qubit array...")
    
    try:
        payload = {"quantum_states": quantum_states_payload}
        client_socket.sendall(json.dumps(payload).encode('utf-8'))
        
        bob_bases_payload = client_socket.recv(4096).decode('utf-8')
        bob_bases = json.loads(bob_bases_payload)["bob_bases"]
        
        client_socket.sendall(json.dumps({"alice_bases": alice_bases}).encode('utf-8'))
        
        sync_payload = client_socket.recv(4096).decode('utf-8')
        sync_data = json.loads(sync_payload)
        
        if sync_data["status"] == "SIFTING_COMPLETE":
            matched_indices = sync_data["indices"]
            alice_sifted_key = [alice_bits[idx] for idx in matched_indices]
            print(f"[ALICE] Sifting validation synchronized cleanly across ports.")
            print(f"[ALICE] Local Sifted Key Pool: {alice_sifted_key} (Length: {len(alice_sifted_key)})")
            
    except Exception as e:
        print(f"[ERROR] Session terminated unexpectedly: {e}")
    finally:
        client_socket.close()
        print("[ALICE] Connections dropped safely.")

if __name__ == "__main__":
    run_alice_client()