from sqlalchemy import (
    Column,
    Integer,
    String,
    Date,
    DateTime,
    func,
    ForeignKey,
    Boolean,
)
from sqlalchemy.orm import relationship
from src.database.db import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=False)
    contacts = relationship("Contact", back_populates="owner")
    created_at = Column("crated_at", DateTime, default=func.now())
    refresh_token = Column(String(255), nullable=True)
    confirmed = Column(Boolean, default=False)


class Contact(Base):
    __tablename__ = "contacts"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(25), index=True, nullable=False)
    last_name = Column(String(25), index=True, nullable=False)
    email = Column(String, index=True, unique=True, nullable=False)
    phone_number = Column(String(13), nullable=False)
    birthday = Column(Date, nullable=False)
    additional_info = Column(String, nullable=True)
    owner_id = Column(Integer, ForeignKey("users.id"))
    owner = relationship("User", back_populates="contacts")
