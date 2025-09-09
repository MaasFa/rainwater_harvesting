# Smart India Hackathon 2025 – Rooftop Rainwater Harvesting (RWH) MVP

This bundle contains:
- `backend/` FastAPI service (Postgres-ready, SQLite fallback)
- `flutter_app/` minimal Flutter client
- `docs/flowchart.png` architecture flowchart

## Quick Start

### Backend (API)
1. Install Python 3.11+
2. Create virtual env and install deps:
   ```bash
   cd backend
   python -m venv .venv
   source .venv/bin/activate    # Windows: .venv\Scripts\activate
   pip install -r requirements.txt
   cp .env.example .env         # set SECRET_KEY and DATABASE_URL if using Postgres
   uvicorn app.main:app --reload --port 8000
   ```
3. Open docs: http://localhost:8000/docs

### Flutter App
1. Install Flutter (3.x). In Android emulator, the backend URL `http://10.0.2.2:8000` points to your host.
2. Run app:
   ```bash
   cd flutter_app
   flutter pub get
   flutter run
   ```

### Docker (optional, Postgres included)
```bash
cd backend
docker compose up --build
```

## Formula
Harvest Potential (L/year) = Roof Area (sqm) × Avg Rainfall (mm/yr) × Runoff Coefficient

Defaults:
- Concrete 0.85, Tile 0.75, Metal 0.90, Green roof 0.50 (MVP values; tune with field data).

## Next Steps
- Replace demo auth with production-grade (refresh tokens, password reset).
- Add PDF report endpoint.
- Add PostGIS and map visualization.
- Integrate IMD rainfall API and soil datasets.
