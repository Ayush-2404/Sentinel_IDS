from scapy.all import sniff
from .feature_extractor import extract_features
from db.queries import insert_packet, insert_traffic_stat
from detection.rule_engine import RuleEngine
from detection.ml_engine import MLEngine
import time
import threading

rule_engine = RuleEngine()
ml_engine   = MLEngine()

# Packet counter for calculating packets/sec
_packet_count = 0
_count_lock   = threading.Lock()

def _record_traffic_rate():
    """Background task: writes packets/sec to DB every 5 seconds."""
    global _packet_count
    while True:
        time.sleep(5)
        with _count_lock:
            rate = _packet_count // 5
            _packet_count = 0
        insert_traffic_stat(rate)

def process_packet(packet):
    global _packet_count

    features = extract_features(packet)
    if not features:
        return

    # Increment counter
    with _count_lock:
        _packet_count += 1

    # Save to DB (non-blocking is better in production; fine for demo)
    insert_packet(
        features["src_ip"],
        features["dst_ip"],
        features["src_port"],
        features["dst_port"],
        features["protocol"],
        features["length"],
    )

    # Rule-based detection
    rule_engine.analyze(features)

    # ML-based detection
    ml_engine.analyze(features)


def start_sniffing(interface=None, packet_filter="ip"):
    """
    Entry point called by FastAPI on startup.
    Set interface=None to sniff on all interfaces (requires root/admin).
    """
    # Start the traffic rate recorder in its own thread
    rate_thread = threading.Thread(target=_record_traffic_rate, daemon=True)
    rate_thread.start()

    print("[Sniffer] Starting packet capture...")
    sniff(
        iface=interface,
        filter=packet_filter,
        prn=process_packet,
        store=False  # Don't keep packets in memory
    )