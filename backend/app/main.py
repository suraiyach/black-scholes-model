from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional
from datetime import datetime
import pytz

from .settings import settings
from .cache import Cache
from .nse_client import NSEClient
from .greeks import compute_row

app = FastAPI(title="NSE Options BS API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

cache = Cache(settings.REDIS_URL, settings.CACHE_TTL_SECONDS)
client = NSEClient(cache)

@app.get("/health")
async def health():
    return {"ok": True}

@app.get("/api/chain")
async def chain(
    symbol: str = Query(..., description="e.g., NIFTY, BANKNIFTY, RELIANCE"),
    instrument: str = Query("INDEX", regex="^(INDEX|EQUITY)$"),
    expiry: Optional[str] = None,
    optionType: str = Query("ALL", regex="^(ALL|CE|PE)$"),
    r: float = Query(settings.RISK_FREE, description="Annualized risk-free rate"),
    maxRows: int = Query(2000, ge=10, le=5000),
):
    oc = client.option_chain(symbol, instrument)
    spot, chosen_expiry, rows = client.extract_rows(oc, expiry, optionType)

    # Compute T (years) from expiry – assume 15:30 IST expiry
    ist = pytz.timezone("Asia/Kolkata")
    now = datetime.now(ist)
    try:
        exp = ist.localize(datetime.strptime(chosen_expiry, "%d-%b-%Y")).replace(hour=15, minute=30, second=0)
    except Exception:
        exp = now
    T_years = max((exp - now).total_seconds(), 60) / (365 * 24 * 3600)

    out = [compute_row(row, S=spot, r=r, T=T_years) for row in rows[:maxRows]]

    return {
        "symbol": symbol.upper(),
        "instrument": instrument,
        "spot": spot,
        "riskFree": r,
        "expiry": chosen_expiry,
        "rows": out,
    }
