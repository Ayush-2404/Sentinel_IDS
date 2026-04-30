from scapy.all import IP, TCP, send
import requests
import time

FAKE_ATTACKER = "10.0.0.101"
TARGET        = "192.168.1.7"   # ← your actual IP
API_BASE      = "http://localhost:8000"

def trigger_alert(src_ip, attack_type, details):
    try:
        requests.post(f"{API_BASE}/api/alerts/manual", json={
            "src_ip":      src_ip,
            "attack_type": attack_type,
            "confidence":  1.0,
            "details":     details
        }, timeout=2)
    except Exception as e:
        print(f"[Sim] Alert API error: {e}")

print(f"[Sim] Brute force from {FAKE_ATTACKER}...")

for i in range(30):
    send(IP(src=FAKE_ATTACKER, dst=TARGET)/TCP(dport=22, flags="S"), verbose=False)
    time.sleep(0.1)

trigger_alert(
    FAKE_ATTACKER,
    "brute_force",
    f"30 repeated attempts to port 22 from {FAKE_ATTACKER}"
)

print("[Sim] Brute force complete — alert triggered.")