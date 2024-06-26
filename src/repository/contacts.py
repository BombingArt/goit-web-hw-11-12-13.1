from sqlalchemy.orm import Session
from sqlalchemy import or_
from typing import List
from src.database import models
from src.schemas import ContactCreate, ContactUpdate, ContactResponse
from datetime import date, timedelta


def create_contact(db: Session, contact: ContactCreate) -> ContactResponse:
    db_contact = models.Contact(**contact.dict())
    db.add(db_contact)
    db.commit()
    db.refresh(db_contact)
    return db_contact

def get_contacts(db: Session, skip: int = 0, limit: int = 10) -> List[ContactResponse]:
    return db.query(models.Contact).offset(skip).limit(limit).all()

def get_contact(db: Session, contact_id: int) -> ContactResponse:
    return db.query(models.Contact).filter(models.Contact.id == contact_id).first()

def update_contact(db: Session, contact_id: int, contact: ContactUpdate) -> ContactResponse:
    db_contact = db.query(models.Contact).filter(models.Contact.id == contact_id).first()
    if db_contact:
        for field, value in contact.dict(exclude_unset=True).items():
            setattr(db_contact, field, value)
        db.commit()
        db.refresh(db_contact)
    return db_contact

def delete_contact(db: Session, contact_id: int) -> None:
    db.query(models.Contact).filter(models.Contact.id == contact_id).delete()
    db.commit()

def search_contacts(db: Session, query: str) -> List[ContactResponse]:
    return db.query(models.Contact).filter(
        or_(
            models.Contact.first_name.ilike(f"%{query}%"),
            models.Contact.last_name.ilike(f"%{query}%"),
            models.Contact.email.ilike(f"%{query}%"),
        )
    ).all()

def search_contacts(db: Session, query: str) -> List[ContactResponse]:
    search_filter = or_(
        models.Contact.first_name.ilike(f"%{query}%"),
        models.Contact.last_name.ilike(f"%{query}%"),
        models.Contact.email.ilike(f"%{query}%")
    )
    return db.query(models.Contact).filter(search_filter).all()



def get_contacts_with_upcoming_birthdays(db: Session) -> List[ContactResponse]:
    today = date.today()
    end_date = today + timedelta(days=7)
    
    return db.query(models.Contact).filter(
        (models.Contact.birthday >= today) & (models.Contact.birthday <= end_date)
    ).all()
