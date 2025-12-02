# Aiswathi Adaptive Prep

Prototype for an IIT JEE-style adaptive practice platform with FastAPI backend and Next.js frontend.

## Backend
- FastAPI service with endpoints for auth, content CRUD, attempts logging, adaptive question selection, analytics, and study plans.
- In-memory store for rapid prototyping plus Postgres schema under `db/migrations` for production.
- Spaced repetition and Elo-style updates implemented in `backend/app/services/adaptive.py`.
- Seed script at `backend/scripts/seed_data.py`.

Run locally:
```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload
```

## Frontend
- Next.js UI with flows for login, practice, analytics dashboard, and study plan editor.
- Located under `frontend/` with simple layout and controls to interact with the backend.

Run locally:
```bash
cd frontend
npm install
npm run dev
```

## DevOps
- `infra/docker-compose.yml` for backend, frontend, Postgres, and Redis.
- GitHub Actions workflow at `.github/workflows/ci.yml` to lint/compile.
