# RWH Assessment Backend (FastAPI)

## Features (MVP)
- JWT-based auth (demo-grade)
- Users, Sites, Assessments
- Compute harvest potential and recharge feasibility
- Postgres via SQLAlchemy (falls back to SQLite if DATABASE_URL not set)
- CORS enabled for Flutter app

## Quickstart (Local)

### 1) Python env
```bash
cd backend
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### 2) Database
- Default is SQLite for local dev.
- For Postgres, set DATABASE_URL in `.env` e.g.
  `DATABASE_URL=postgresql+psycopg2://postgres:postgres@localhost:5432/rwhdb`

### 3) Run server
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

API docs at: `http://localhost:8000/docs`

### Docker (optional)
```bash
docker compose up --build
```
