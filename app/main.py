import uvicorn
from fastapi import FastAPI
from slowapi import Limiter
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware

from app.core.config import settings
from app.db.session import engine, Base, get_db
from app.db.init_db import seed_roles

from app.api.routes import auth, users, records, dashboard
from app.middlewares.logging import LoggingMiddleware


app = FastAPI(title=settings.PROJECT_NAME)


# Rate Limiter (GLOBAL)
limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, lambda r, e: None)
app.add_middleware(SlowAPIMiddleware)


# Logging Middleware
app.add_middleware(LoggingMiddleware)


# Startup Event
@app.on_event("startup")
async def on_startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async for db in get_db():
        await seed_roles(db)


# Routers
app.include_router(auth.router)
app.include_router(users.router)
app.include_router(records.router)
app.include_router(dashboard.router)


# Root Endpoint
@app.get("/")
async def root():
    return {"message": "FinGuard API is running 🚀"}


# Run Server
if __name__ == "__main__":
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000)