from fastapi import APIRouter
from db.queries import (
    get_packet_count, get_total_alert_count,
    get_blocked_ip_count, get_recent_traffic
)

router = APIRouter(prefix="/api/stats", tags=["stats"])

@router.get("/summary")
def summary():
    return {
        "total_packets": get_packet_count(),
        "total_alerts":  get_total_alert_count(),
        "blocked_ips":   get_blocked_ip_count(),
    }

@router.get("/traffic")
def traffic(limit: int = 30):
    return get_recent_traffic(limit=limit)