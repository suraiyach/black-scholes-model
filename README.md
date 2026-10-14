# NSE Options Analytics – Black–Scholes (India)

Full-stack app that fetches NSE option chain (index/equity), computes Black–Scholes prices + Greeks, and displays them in a Next.js dashboard.

## Quickstart (no Docker)
### Backend
```bash
cd backend
python -m venv .venv && source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```
API: http://localhost:8000/docs

### Frontend
```bash
cd frontend
npm i
cp .env.example .env.local  # ensure NEXT_PUBLIC_API_BASE points to backend
npm run dev
```
UI: http://localhost:3000

## Docker Compose
```bash
docker compose up --build
```
- Frontend: http://localhost:3000
- API: http://localhost:8000

## Notes
- NSE blocks aggressive scraping. Keep refresh ≥ 10s, use cache/Redis.
- Expiry format: `dd-MMM-YYYY` (e.g., `28-Aug-2025`). Assumes 15:30 IST expiry for T.
- Risk-free defaults to 6.5% (RBI repo). Override with `?r=` query or env.
