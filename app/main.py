import uvicorn
from fastapi import FastAPI
from sqlalchemy.ext.asyncio import AsyncEngine

from app.core.config import settings
from app.db.session import engine, Base

from app.api.routes import auth, users, records, dashboard


app = FastAPI(title=settings.PROJECT_NAME)

# Create Tables on Startup
@app.on_event("startup")
async def on_startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

# Include Routers
app.include_router(auth.router)
app.include_router(users.router)
app.include_router(records.router)
app.include_router(dashboard.router)


# Root Endpoint
@app.get("/")
async def root():
    return {"message": "FinGuard API is running 🚀"}


if __name__ == "__main__":
    uvicorn.run("app.main:app", host = "localhost", port = 8000, reload = True)