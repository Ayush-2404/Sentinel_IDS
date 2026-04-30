from fastapi import APIRouter
from pydantic import BaseModel
from db.queries import get_top_source_ips, get_blocked_ips, block_ip

router = APIRouter(prefix="/api/ips", tags=["ips"])

class BlockRequest(BaseModel):
    ip: str
    reason: str = "Manual block"

@router.get("/top")
def top_ips(limit: int = 10):
    return get_top_source_ips(limit=limit)

@router.get("/blocked")
def blocked_ips():
    ips = get_blocked_ips()
    for entry in ips:
        entry["blocked_at"] = str(entry["blocked_at"])
    return ips

@router.post("/block")
def block(req: BlockRequest):
    block_ip(req.ip, req.reason)
    return {"status": "blocked", "ip": req.ip}