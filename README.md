# PrayerWall backend (FastAPI)

This backend provides a minimal FastAPI + PostgreSQL service for managing users and prayer requests.

Features

- User registration and login (JWT)
- Create and list personal prayer requests
- Admin endpoints to list, mark answered, and delete prayer requests

Quick start

1. Create a Python virtualenv and install dependencies:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

2. Copy `.env.example` to `.env` and set `DATABASE_URL` and `SECRET_KEY`.

3. Create the PostgreSQL database (example):

```powershell
# run in psql or use your DB admin tool
createdb prayerdb
```

4. Run the app:

```powershell
uvicorn app.main:app --reload --port 8000
```

Notes

- This scaffold uses SQLAlchemy create_all to build tables. For production use Alembic migrations.
- You should set a strong SECRET_KEY in `.env` and secure the database credentials.
