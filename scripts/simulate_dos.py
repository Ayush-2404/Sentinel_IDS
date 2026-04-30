from scapy.all import IP, TCP, send
import requests
import time

FAKE_ATTACKER = "10.0.0.100"
TARGET        = "192.168.1.7"   # ← actual IP
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

print(f"[Sim] DoS flooding from {FAKE_ATTACKER}...")

for i in range(200):
    send(IP(src=FAKE_ATTACKER, dst=TARGET)/TCP(dport=80, flags="S"), verbose=False)
    time.sleep(0.01)

trigger_alert(
    FAKE_ATTACKER,
    "dos_attack",
    f"200 packets in 2s from {FAKE_ATTACKER} — flood detected"
)

print("[Sim] DoS simulation complete — alert triggered.")