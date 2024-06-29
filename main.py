from fastapi import FastAPI
from src.routes import contacts
from src.database import db
from src.database.db import Base, engine
from src.routes import contacts, auth

app = FastAPI()


def create_tables():
    Base.metadata.create_all(bind=engine)


app.include_router(contacts.router, prefix="/api")
app.include_router(auth.router, prefix="/api")

create_tables()
