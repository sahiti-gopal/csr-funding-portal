# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Overview

CSR Funding Portal — a corporate social responsibility project-tracking dashboard. Flask + MySQL REST API backend, React (Vite) SPA frontend. The two apps live in `backend/` and `frontend/` and run as separate dev servers.

## Commands

### Database (Docker)
MySQL 8.4 runs in Docker, exposed on host port **3307** (not 3306). The backend `.env` must use `DB_PORT=3307`.
```bash
docker compose up -d      # start MySQL (db: csr_funding_portal, user: csr_user)
```

### Backend (run from `backend/`)
```bash
python -m venv .venv && .venv/Scripts/activate   # Windows; use bin/activate on POSIX
pip install -r requirements.txt
flask db upgrade          # apply Alembic migrations (FLASK_APP=run.py from .env)
python seed.py            # wipe + reseed roles, project types, categories, sample projects
python run.py             # dev server on http://localhost:5000 (debug=True)

flask db migrate -m "msg" # generate a migration after changing a model
flask db upgrade          # apply it
black .                   # format
ruff check .              # lint
pytest                    # test runner is installed; backend/tests/ is currently empty
```

### Frontend (run from `frontend/`)
```bash
npm install
npm run dev               # Vite dev server on http://localhost:5173
npm run build
npm run lint              # ESLint
npm run preview
```

## Architecture

### Backend — Flask app-factory + blueprints
- `run.py` → `create_app()` in `app/__init__.py`. The factory loads `Config`, inits extensions (`db`, `migrate`, `cors`), and registers each route blueprint under the **`/api`** prefix. CORS is restricted to the Vite origin `http://localhost:5173`.
- **Extensions** (`app/extensions.py`) are singletons (`db`, `migrate`, `cors`) initialized in the factory — import from here, never construct new instances.
- **Config** (`app/config.py`) builds `SQLALCHEMY_DATABASE_URI` from `DB_*` env vars via `python-dotenv`. `.env` is required (see `.env.example`).
- **Models** (`app/models/`) all subclass `BaseModel` (`app/models/base.py`), which supplies `id`, `created_at`, `updated_at`. `app/models/__init__.py` re-exports every model; import order there matters because relationships resolve at import. Data model: master tables `Role`, `ProjectType`, `BeneficiaryCategory`, `User`; `Project` has FKs to `project_type_id` and `beneficiary_category_id` with backref `projects`.
- **Routes** (`app/routes/*_routes.py`): one blueprint per resource. Handlers hand-build JSON dicts (no marshalling layer) and commit directly via `db.session`. New resources need a new `*_routes.py` blueprint **and** a `register_blueprint(..., url_prefix="/api")` line in `create_app()`.
- **Migrations** (`backend/migrations/`) are Flask-Migrate/Alembic. Schema changes go through `flask db migrate`/`upgrade`, not manual DDL.

### Frontend — React 19 + Vite, layered API access
- Entry: `main.jsx` → `App.jsx` → `routes/AppRouter.jsx` (React Router v7 `BrowserRouter`). All pages render inside `layouts/MainLayout.jsx` (Sidebar + Header + `<Outlet>`).
- **API layering (keep this separation):** `api/axios.js` creates the shared axios instance (`baseURL` = `VITE_API_URL` or `http://localhost:5000/api`) → `services/*Service.js` wrap endpoint calls and return `response.data` → pages/components consume the services. Do not call axios directly from components.
- Data fetching uses **TanStack Query**; forms use **react-hook-form** + **zod**; charts use **recharts**; styling is **Tailwind CSS v4** plus per-page CSS in `src/styles/`.
- Components are grouped by feature area: `components/{dashboard,project,charts,alerts,forms,layout}/`.

## Conventions & gotchas
- Backend↔frontend contract lives in the route handler dicts and the matching `services/*.js` — update both sides together when changing a response shape.
- `AuthContext`/`authService`/`useAuth` exist but **auth is not wired into the router**; all routes are currently public.
- Dead/empty scaffolding to ignore (not part of the active app): `backend/app/config/config.py` (empty — real config is `app/config.py`), `backend/app/routes.py` (unregistered health blueprint), `backend/query`.
- Root-level `package.json`/`node_modules/` are incidental; the real frontend deps live in `frontend/`.
