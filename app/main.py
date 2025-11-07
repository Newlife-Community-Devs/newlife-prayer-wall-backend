from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
from sqlalchemy import text
from .database import engine, Base
from .routes import router as api_router

app = FastAPI(title="PrayerWall Backend")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def on_startup():
    # create tables if they don't exist
    Base.metadata.create_all(bind=engine)


app.include_router(api_router)


@app.get("/")
def root():
    return {"message": "PrayerWall backend is running"}


@app.get("/health")
async def health_check():
    try:
        # Try to connect and run a simple query
        with engine.connect() as conn:
            result = conn.execute(text("SELECT 1")).scalar()
            return {
                "status": "healthy",
                "database": "connected",
                "timestamp": datetime.utcnow().isoformat()
            }
    except Exception as e:
        return {"status": "unhealthy", "database": str(e)}
