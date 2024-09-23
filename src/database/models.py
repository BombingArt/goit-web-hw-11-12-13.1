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
    """
    Represents a user in the system.

    Attributes:
        id (int): Unique identifier for the user.
        username (str): Unique username of the user.
        email (str): Unique email address of the user.
        password (str): Hashed password of the user.
        avatar (str): URL or path to the user's avatar image.
        contacts (relationship): List of contacts associated with the user.
        created_at (datetime): Timestamp when the user was created.
        refresh_token (str): Optional token for refreshing the user's sessions.
        confirmed (bool): Flag indicating whether the user's email is confirmed.
    """
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=False)
    avatar = Column(String, nullable=True)
    contacts = relationship("Contact", back_populates="owner")
    created_at = Column("crated_at", DateTime, default=func.now())
    refresh_token = Column(String(255), nullable=True)
    confirmed = Column(Boolean, default=False)


class Contact(Base):
    """
    Represents a contact associated with a user.

    Attributes:
        id (int): Unique identifier for the contact.
        first_name (str): First name of the contact.
        last_name (str): Last name of the contact.
        email (str): Unique email address of the contact.
        phone_number (str): Phone number of the contact.
        birthday (date): Birthdate of the contact.
        additional_info (str): Additional information about the contact.
        owner_id (int): Unique identifier of the user to whom the contact belongs.
        owner (relationship): User to whom this contact belongs.
    """
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
