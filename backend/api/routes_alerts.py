from fastapi import APIRouter
from pydantic import BaseModel
from db.queries import (
    get_recent_alerts, get_alert_type_counts,
    get_total_alert_count, insert_alert, block_ip
)

router = APIRouter(prefix="/api/alerts", tags=["alerts"])

# --- existing routes stay exactly as they are ---

@router.get("/")
def list_alerts(limit: int = 50):
    alerts = get_recent_alerts(limit=limit)
    for a in alerts:
        a["timestamp"] = str(a["timestamp"])
    return alerts

@router.get("/types")
def alert_type_breakdown():
    return get_alert_type_counts()

@router.get("/count")
def alert_count():
    return {"count": get_total_alert_count()}


# --- ADD THIS NEW ROUTE at the bottom ---

class ManualAlertRequest(BaseModel):
    src_ip:      str
    attack_type: str
    confidence:  float = 1.0
    details:     str   = ""

@router.post("/manual")
def manual_alert(req: ManualAlertRequest):
    """
    Called directly by simulation scripts to guarantee
    the correct attack type appears in the dashboard.
    """
    insert_alert(req.src_ip, req.attack_type, req.confidence, req.details)
    block_ip(req.src_ip, reason=f"Simulation: {req.attack_type}")
    return {"status": "alert created", "attack_type": req.attack_type}