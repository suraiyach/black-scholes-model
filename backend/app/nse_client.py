from typing import Any, Dict, List, Tuple
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from .settings import settings
from .cache import Cache

BASE = "https://www.nseindia.com"
INDEX_API = "/api/option-chain-indices?symbol={symbol}"
EQUITY_API = "/api/option-chain-equities?symbol={symbol}"
QUOTES_API = "/api/quote-equity?symbol={symbol}"

class NSEClient:
    def __init__(self, cache: Cache):
        self.cache = cache
        self.s = requests.Session()
        self.s.headers.update({
            "User-Agent": settings.USER_AGENT,
            "Accept": "application/json, text/plain, */*",
            "Referer": BASE + "/option-chain",
            "Accept-Language": "en-IN,en;q=0.9",
            "Connection": "keep-alive",
        })
        retry = Retry(total=settings.RETRIES, backoff_factor=0.6, status_forcelist=[429, 500, 502, 503, 504])
        self.s.mount("https://", HTTPAdapter(max_retries=retry))
        self._warm()

    def _warm(self):
        try:
            self.s.get(BASE, timeout=settings.TIMEOUT)
        except Exception:
            pass

    def _get_json(self, url: str) -> Dict[str, Any]:
        r = self.s.get(url, timeout=settings.TIMEOUT)
        r.raise_for_status()
        return r.json()

    def option_chain(self, symbol: str, instrument: str = "INDEX") -> Dict[str, Any]:
        key = f"oc:{instrument}:{symbol}"
        cached = self.cache.get(key)
        if cached:
            return cached
        url = BASE + (INDEX_API if instrument == "INDEX" else EQUITY_API).format(symbol=symbol.upper())
        data = self._get_json(url)
        self.cache.set(key, data)
        return data

    def spot_price(self, symbol: str, instrument: str = "INDEX") -> float:
        if instrument == "INDEX":
            oc = self.option_chain(symbol, instrument)
            return float(oc.get("records", {}).get("underlyingValue"))
        else:
            data = self._get_json(BASE + QUOTES_API.format(symbol=symbol.upper()))
            return float(data.get("priceInfo", {}).get("lastPrice"))

    def extract_rows(self, oc: Dict[str, Any], expiry: str | None, optionType: str) -> Tuple[float, str, List[Dict[str, Any]]]:
        records = oc.get("records", {})
        spot = float(records.get("underlyingValue"))
        expiries: List[str] = records.get("expiryDates", [])
        chosen_expiry = expiry or (expiries[0] if expiries else "")
        data: List[Dict[str, Any]] = []

        for row in oc.get("records", {}).get("data", []):
            if row.get("expiryDate") != chosen_expiry:
                continue
            strike = float(row.get("strikePrice"))
            if optionType in ("ALL", "CE") and row.get("CE"):
                ce = row["CE"]
                data.append({
                    "strikePrice": strike,
                    "optionType": "CE",
                    "impliedVolatility": float(ce.get("impliedVolatility") or 0) / 100.0,
                    "lastPrice": float(ce.get("lastPrice") or 0),
                    "totalTradedVolume": float(ce.get("totalTradedVolume") or 0),
                })
            if optionType in ("ALL", "PE") and row.get("PE"):
                pe = row["PE"]
                data.append({
                    "strikePrice": strike,
                    "optionType": "PE",
                    "impliedVolatility": float(pe.get("impliedVolatility") or 0) / 100.0,
                    "lastPrice": float(pe.get("lastPrice") or 0),
                    "totalTradedVolume": float(pe.get("totalTradedVolume") or 0),
                })
        data.sort(key=lambda x: (x["strikePrice"], x["optionType"]))
        return spot, chosen_expiry, data
