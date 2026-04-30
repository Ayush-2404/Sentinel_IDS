from collections import defaultdict
from datetime import datetime, timedelta
from db.queries import insert_alert, block_ip

# Thresholds — tuning demo environment
PORT_SCAN_THRESHOLD     = 5    # distinct ports from one IP in 15 sec
BRUTE_FORCE_THRESHOLD   = 8    # requests from one IP to one port in 15 sec
DOS_THRESHOLD           = 30   # total packets from one IP in 15 sec

WINDOW_SECONDS = 15


class RuleEngine:
    def __init__(self):
        # IPs to never alert on — add your own machine's IPs here
        self.WHITELIST = {
            "127.0.0.1",
            "::1",
            "192.168.1.7",    # my actual IP
        }
        
        # {src_ip: [(dst_port, timestamp), ...]}
        self._port_events   = defaultdict(list)
        # {(src_ip, dst_port): [timestamp, ...]}
        self._request_events = defaultdict(list)
        # {src_ip: [timestamp, ...]}
        self._packet_events  = defaultdict(list)
        # Prevent duplicate alerts in quick succession
        self._alerted: set  = set()

    def _cleanup_old(self, event_list, window=WINDOW_SECONDS):
        cutoff = datetime.now() - timedelta(seconds=window)
        return [e for e in event_list if e[-1] > cutoff]

    def analyze(self, features: dict):
        src_ip   = features["src_ip"]
        
        # Skip whitelisted IPs
        if src_ip in self.WHITELIST:
            return

        dst_port = features["dst_port"]
        now      = datetime.now()

        # ── Port Scan Detection ──────────────────────────────
        self._port_events[src_ip].append((dst_port, now))
        self._port_events[src_ip] = self._cleanup_old(self._port_events[src_ip])
        distinct_ports = len(set(e[0] for e in self._port_events[src_ip]))
        if distinct_ports > PORT_SCAN_THRESHOLD:
            self._fire("port_scan", src_ip,
                       f"Scanned {distinct_ports} ports in {WINDOW_SECONDS}s")

        # ── Brute Force Detection ────────────────────────────
        key = (src_ip, dst_port)
        self._request_events[key].append((now,))
        self._request_events[key] = self._cleanup_old(self._request_events[key])
        if len(self._request_events[key]) > BRUTE_FORCE_THRESHOLD:
            self._fire("brute_force", src_ip,
                       f"{len(self._request_events[key])} requests to port {dst_port} in {WINDOW_SECONDS}s")

        # ── DoS Detection ────────────────────────────────────
        self._packet_events[src_ip].append((now,))
        self._packet_events[src_ip] = self._cleanup_old(
            self._packet_events[src_ip], window=5)
        if len(self._packet_events[src_ip]) > DOS_THRESHOLD:
            self._fire("dos_attack", src_ip,
                       f"{len(self._packet_events[src_ip])} packets in 5s")

    def _fire(self, attack_type: str, src_ip: str, details: str):
        """Fires an alert and auto-blocks the IP. Deduplicates within 30s."""
        alert_key = f"{attack_type}:{src_ip}"
        cutoff = datetime.now() - timedelta(seconds=30)

        # Prune stale dedup entries (stored as (key, time))
        self._alerted = {
            (k, t) for k, t in self._alerted if t > cutoff
        }

        if alert_key not in {k for k, _ in self._alerted}:
            print(f"[RULE ALERT] {attack_type.upper()} from {src_ip}: {details}")
            insert_alert(src_ip, attack_type, confidence=1.0, details=details)
            block_ip(src_ip, reason=f"Auto-blocked: {attack_type}")
            self._alerted.add((alert_key, datetime.now()))