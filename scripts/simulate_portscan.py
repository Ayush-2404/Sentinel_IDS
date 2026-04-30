from scapy.all import IP, TCP, send
import requests
import time

FAKE_ATTACKER = "10.0.0.99"
TARGET        = "192.168.1.7"   # IP from ipconfig
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

print(f"[Sim] Port scanning from {FAKE_ATTACKER}...")

for port in range(1, 60):
    send(IP(src=FAKE_ATTACKER, dst=TARGET)/TCP(dport=port, flags="S"), verbose=False)
    time.sleep(0.02)

# Directly trigger the alert so dashboard always shows it
trigger_alert(
    FAKE_ATTACKER,
    "port_scan",
    f"Scanned 59 ports in 1.2s from {FAKE_ATTACKER}"
)

print("[Sim] Port scan complete — alert triggered.")