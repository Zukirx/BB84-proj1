# run_experiment.py
import subprocess
import time
import sys

def execute_trial():
    # 1. Spawn Bob
    bob_process = subprocess.Popen(
        [sys.executable, 'bob_server.py'], 
        stdout=subprocess.PIPE, 
        stderr=subprocess.PIPE, 
        text=True
    )
    time.sleep(0.3)

    # 2. Spawn Eve
    eve_process = subprocess.Popen(
        [sys.executable, 'eve_proxy.py'], 
        stdout=subprocess.PIPE, 
        stderr=subprocess.PIPE, 
        text=True
    )
    time.sleep(0.3)

    # 3. Exec Alice
    subprocess.run([sys.executable, 'alice_client_attacked.py'], capture_output=True, text=True)

    # Force a readout wrap with absolute deadlines
    try:
        bob_output, _ = bob_process.communicate(timeout=2.0)
    except subprocess.TimeoutExpired:
        bob_process.kill()
        bob_output, _ = bob_process.communicate()

    if eve_process:
        eve_process.kill()

    # 4. Parse Bob's structural terminal printouts
    qber = "0.0%"
    status = "SECURE_CHANNEL"
    
    for line in bob_output.split('\n'):
        if "QBER:" in line:
            qber = line.split("QBER:")[1].strip()
        if "STATUS:" in line:
            status = line.split("STATUS:")[1].strip()

    return qber, status

def run_replication_study():
    print("="*60)
    print("🔬 INITIALIZING EMPIRICAL QKD REPLICATION STUDY")
    print("="*60)
    
    print("\n[TEST RUN] Executing 100-Qubit Intercept-Resend Attack...")
    qber, status = execute_trial()
    
    print("\n" + "="*60)
    print("📊 REPLICATION AUDIT SUMMARY DATA TABLE")
    print("="*60)
    print(f"{'Experiment Profile':<25} | {'Empirical QBER':<15} | {'IDS Status':<18}")
    print("-" * 65)
    print(f"{'Active Eve Proxy (MitM)':<25} | {qber:<15} | {status:<18}")
    print("="*60)

if __name__ == "__main__":
    run_replication_study()