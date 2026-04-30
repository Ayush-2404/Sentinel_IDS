from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from threading import Thread

from api.routes_alerts import router as alerts_router
from api.routes_stats   import router as stats_router
from api.routes_ips     import router as ips_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Start sniffer in background (requires root/admin on most systems)
    try:
        from capture.sniffer import start_sniffing
        t = Thread(target=start_sniffing, daemon=True)
        t.start()
        print("[Main] Sniffer thread started.")
    except Exception as e:
        print(f"[Main] Sniffer failed to start (run as admin): {e}")
    yield


app = FastAPI(
    title="Hybrid IDS API",
    description="Real-time Intrusion Detection System",
    version="1.0.0",
    lifespan=lifespan,
)

# Allow React dev server (port 5173) to talk to this API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(alerts_router)
app.include_router(stats_router)
app.include_router(ips_router)

@app.get("/")
def health():
    return {"status": "IDS running"}