from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.database import db
from src.database.db import Base, engine
from src.routes import contacts, auth, users
from fastapi_limiter import FastAPILimiter
import redis.asyncio as redis
from src.conf.config import settings

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def create_tables():
    Base.metadata.create_all(bind=engine)


app.include_router(contacts.router, prefix="/api")
app.include_router(auth.router, prefix="/api")
app.include_router(users.router, prefix="/api")

create_tables()


@app.on_event("startup")
async def startup():
    r = redis.Redis(
        host=settings.redis_host,
        port=settings.redis_port,
        db=0,
        encoding="utf-8",
        decode_responses=True,
    )
    # Проверка подключения
    try:
        await r.ping()
        print("Connected to Redis")
    except Exception as e:
        print(f"Could not connect to Redis: {e}")
    await FastAPILimiter.init(r)
