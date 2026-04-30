from .connection import get_conn, release_conn
from datetime import datetime

# ─── Packets ────────────────────────────────────────────────

def insert_packet(src_ip, dst_ip, src_port, dst_port, protocol, length):
    conn = get_conn()
    try:
        with conn.cursor() as cur:
            cur.execute("""
                INSERT INTO packets (src_ip, dst_ip, src_port, dst_port, protocol, length)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (src_ip, dst_ip, src_port, dst_port, protocol, length))
        conn.commit()
    finally:
        release_conn(conn)

def get_packet_count():
    conn = get_conn()
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT COUNT(*) FROM packets")
            return cur.fetchone()[0]
    finally:
        release_conn(conn)

def get_top_source_ips(limit=10):
    conn = get_conn()
    try:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT src_ip, COUNT(*) as count
                FROM packets
                GROUP BY src_ip
                ORDER BY count DESC
                LIMIT %s
            """, (limit,))
            return [{"ip": row[0], "count": row[1]} for row in cur.fetchall()]
    finally:
        release_conn(conn)

# ─── Alerts ─────────────────────────────────────────────────

def insert_alert(src_ip, attack_type, confidence=1.0, details=""):
    conn = get_conn()
    try:
        with conn.cursor() as cur:
            cur.execute("""
                INSERT INTO alerts (src_ip, attack_type, confidence, details)
                VALUES (%s, %s, %s, %s)
            """, (src_ip, attack_type, confidence, details))
        conn.commit()
    finally:
        release_conn(conn)

def get_recent_alerts(limit=50):
    conn = get_conn()
    try:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT id, src_ip, attack_type, confidence, details, timestamp
                FROM alerts
                ORDER BY timestamp DESC
                LIMIT %s
            """, (limit,))
            cols = ["id", "src_ip", "attack_type", "confidence", "details", "timestamp"]
            return [dict(zip(cols, row)) for row in cur.fetchall()]
    finally:
        release_conn(conn)

def get_alert_type_counts():
    conn = get_conn()
    try:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT attack_type, COUNT(*) as count
                FROM alerts
                GROUP BY attack_type
            """)
            return [{"type": row[0], "count": row[1]} for row in cur.fetchall()]
    finally:
        release_conn(conn)

def get_total_alert_count():
    conn = get_conn()
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT COUNT(*) FROM alerts")
            return cur.fetchone()[0]
    finally:
        release_conn(conn)

# ─── Blocked IPs ─────────────────────────────────────────────

def block_ip(ip_address, reason="Manual block"):
    conn = get_conn()
    try:
        with conn.cursor() as cur:
            cur.execute("""
                INSERT INTO blocked_ips (ip_address, reason)
                VALUES (%s, %s)
                ON CONFLICT (ip_address) DO NOTHING
            """, (ip_address, reason))
        conn.commit()
    finally:
        release_conn(conn)

def get_blocked_ips():
    conn = get_conn()
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT ip_address, reason, blocked_at FROM blocked_ips ORDER BY blocked_at DESC")
            cols = ["ip", "reason", "blocked_at"]
            return [dict(zip(cols, row)) for row in cur.fetchall()]
    finally:
        release_conn(conn)

def get_blocked_ip_count():
    conn = get_conn()
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT COUNT(*) FROM blocked_ips")
            return cur.fetchone()[0]
    finally:
        release_conn(conn)

# ─── Traffic Stats ────────────────────────────────────────────

def insert_traffic_stat(packets_per_sec):
    conn = get_conn()
    try:
        with conn.cursor() as cur:
            cur.execute(
                "INSERT INTO traffic_stats (packets_per_sec) VALUES (%s)",
                (packets_per_sec,)
            )
        conn.commit()
    finally:
        release_conn(conn)

def get_recent_traffic(limit=30):
    conn = get_conn()
    try:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT packets_per_sec, recorded_at
                FROM traffic_stats
                ORDER BY recorded_at DESC
                LIMIT %s
            """, (limit,))
            return [
                {"pps": row[0], "time": row[1].strftime("%H:%M:%S")}
                for row in reversed(cur.fetchall())
            ]
    finally:
        release_conn(conn)