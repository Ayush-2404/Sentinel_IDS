from scapy.all import IP, TCP, UDP, ICMP

def extract_features(packet) -> dict | None:
    if not packet.haslayer(IP):
        return None

    ip = packet[IP]
    protocol = "OTHER"
    src_port  = 0
    dst_port  = 0

    if packet.haslayer(TCP):
        protocol = "TCP"
        src_port = packet[TCP].sport
        dst_port = packet[TCP].dport
    elif packet.haslayer(UDP):
        protocol = "UDP"
        src_port = packet[UDP].sport
        dst_port = packet[UDP].dport
    elif packet.haslayer(ICMP):
        protocol = "ICMP"

    return {
        "src_ip":   ip.src,
        "dst_ip":   ip.dst,
        "src_port": src_port,
        "dst_port": dst_port,
        "protocol": protocol,
        "length":   len(packet),
        "ttl":      ip.ttl,
    }


# Maps a single packet to the 10 UNSW-NB15 features our model was trained on.
# Single packets don't have flow-level stats (dur, sbytes etc.) so we approximate.
PROTO_MAP   = {"TCP": "tcp", "UDP": "udp", "ICMP": "icmp", "OTHER": "other"}
SERVICE_MAP = {
    80: "http", 443: "https", 21: "ftp", 22: "ssh",
    23: "telnet", 25: "smtp", 53: "dns", 3306: "mysql",
}

def packet_to_ml_vector(features: dict, encoders: dict) -> list:
    """
    Converts packet dict → numeric vector matching UNSW-NB15 feature order:
    proto, service, state, dur, sbytes, dbytes, sttl, dttl, sloss, dloss
    """
    def encode(col, val):
        le = encoders.get(col)
        if le is None:
            return 0
        val_str = str(val)
        if val_str in le.classes_:
            return int(le.transform([val_str])[0])
        return -1  # unseen label

    proto   = PROTO_MAP.get(features["protocol"], "other")
    service = SERVICE_MAP.get(features["dst_port"], "-")
    state   = "INT"   # single-packet approximation

    return [
        encode("proto",   proto),
        encode("service", service),
        encode("state",   state),
        0,                        # dur — unknown for single packet
        features["length"],       # sbytes — approximate with packet length
        0,                        # dbytes — unknown
        features["ttl"],          # sttl
        0,                        # dttl — unknown
        0,                        # sloss
        0,                        # dloss
    ]