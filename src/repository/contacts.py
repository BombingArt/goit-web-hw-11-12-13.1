from sqlalchemy.orm import Session
from sqlalchemy import or_
from typing import List
from src.database import models
from src.schemas import ContactCreate, ContactUpdate, ContactResponse
from datetime import datetime, timedelta
from src.database.models import User
from fastapi import HTTPException, status


def create_contact(db: Session, contact: ContactCreate, user: User) -> ContactResponse:
    existing_contact = (
        db.query(models.Contact).filter(models.Contact.email == contact.email).first()
    )
    if existing_contact:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="A contact with this email already exists.",
        )
    db_contact = models.Contact(**contact.dict(), owner_id=user.id)
    db.add(db_contact)
    db.commit()
    db.refresh(db_contact)
    return db_contact


def get_contacts(
    db: Session, user: User, skip: int = 0, limit: int = 10
) -> List[ContactResponse]:
    return (
        db.query(models.Contact)
        .filter(models.Contact.owner_id == user.id)
        .offset(skip)
        .limit(limit)
        .all()
    )


def get_contact(db: Session, contact_id: int, user: User) -> ContactResponse:
    return (
        db.query(models.Contact)
        .filter(models.Contact.id == contact_id, models.Contact.owner_id == user.id)
        .first()
    )


def update_contact(
    db: Session, contact_id: int, contact: ContactUpdate, user: User
) -> ContactResponse:
    db_contact = (
        db.query(models.Contact)
        .filter(models.Contact.id == contact_id, models.Contact.owner_id == user.id)
        .first()
    )
    if db_contact:
        for var, value in vars(contact).items():
            setattr(db_contact, var, value) if value else None
        db.add(db_contact)
        db.commit()
        db.refresh(db_contact)
    return db_contact


def delete_contact(db: Session, contact_id: int, user: User) -> None:
    db_contact = (
        db.query(models.Contact)
        .filter(models.Contact.id == contact_id, models.Contact.owner_id == user.id)
        .first()
    )
    if db_contact:
        db.delete(db_contact)
        db.commit()


def search_contacts(db: Session, query: str, user: User) -> List[ContactResponse]:
    return (
        db.query(models.Contact)
        .filter(
            models.Contact.owner_id == user.id,
            or_(
                models.Contact.first_name.ilike(f"%{query}%"),
                models.Contact.last_name.ilike(f"%{query}%"),
                models.Contact.email.ilike(f"%{query}%"),
            ),
        )
        .all()
    )


def get_contacts_with_upcoming_birthdays(
    db: Session, user: User
) -> List[ContactResponse]:
    today = datetime.utcnow().date()
    next_month = today.replace(day=1) + timedelta(days=31)
    next_month = next_month.replace(day=1)
    return (
        db.query(models.Contact)
        .filter(
            models.Contact.owner_id == user.id,
            models.Contact.birthday.between(
                today.replace(year=today.year), next_month.replace(year=today.year)
            ),
        )
        .all()
    )
