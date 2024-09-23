from sqlalchemy.orm import Session
from sqlalchemy import or_
from typing import List
from src.database import models
from src.schemas import ContactCreate, ContactUpdate, ContactResponse
from datetime import datetime, timedelta
from src.database.models import User
from fastapi import HTTPException, status


def create_contact(db: Session, contact: ContactCreate, user: User) -> ContactResponse:
    """
    Creates a new contact and adds it to the database.

    Args:
        db (Session): Database session.
        contact (ContactCreate): Schema for creating a new contact.
        user (User): User to whom the contact belongs.

    Returns:
        ContactResponse: The created contact.

    Raises:
        HTTPException: If a contact with the same email already exists.
    """
    existing_contact = db.query(models.Contact).filter(
        models.Contact.email == contact.email).first()
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


def get_contacts(db: Session, user: User, skip: int = 0, limit: int = 10) -> List[ContactResponse]:
    """
    Retrieves a list of a user's contacts with pagination.

    Args:
        db (Session): Database session.
        user (User): User whose contacts need to be retrieved.
        skip (int): Number of records to skip (for pagination).
        limit (int): Number of records to return.

    Returns:
        List[ContactResponse]: List of contacts.
    """
    return (
        db.query(models.Contact)
        .filter(models.Contact.owner_id == user.id)
        .offset(skip)
        .limit(limit)
        .all()
    )


def get_contact(db: Session, contact_id: int, user: User) -> ContactResponse:
    """
    Retrieves a contact by ID if it belongs to the user.

    Args:
        db (Session): Database session.
        contact_id (int): Contact ID.
        user (User): User whose contacts need to be checked.

    Returns:
        ContactResponse: The found contact.

    Raises:
        HTTPException: If the contact is not found.
    """
    contact = (
        db.query(models.Contact)
        .filter(models.Contact.id == contact_id, models.Contact.owner_id == user.id)
        .first()
    )
    if not contact:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Contact not found.",
        )
    return contact


def update_contact(
    db: Session, contact_id: int, contact: ContactUpdate, user: User
) -> ContactResponse:
    """
    Updates a contact by ID if it belongs to the user.

    Args:
        db (Session): Database session.
        contact_id (int): Contact ID.
        contact (ContactUpdate): Schema with updated contact data.
        user (User): User to whom the contact belongs.

    Returns:
        ContactResponse: The updated contact.

    Raises:
        HTTPException: If the contact is not found.
    """
    db_contact = (
        db.query(models.Contact)
        .filter(models.Contact.id == contact_id, models.Contact.owner_id == user.id)
        .first()
    )
    if not db_contact:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Contact not found.",
        )
    for var, value in vars(contact).items():
        setattr(db_contact, var, value) if value else None
    db.add(db_contact)
    db.commit()
    db.refresh(db_contact)
    return db_contact


def delete_contact(db: Session, contact_id: int, user: User) -> None:
    """
    Deletes a contact by ID if it belongs to the user.

    Args:
        db (Session): Database session.
        contact_id (int): Contact ID.
        user (User): User whose contact needs to be deleted.

    Raises:
        HTTPException: If the contact is not found.
    """
    db_contact = (
        db.query(models.Contact)
        .filter(models.Contact.id == contact_id, models.Contact.owner_id == user.id)
        .first()
    )
    if not db_contact:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Contact not found.",
        )
    db.delete(db_contact)
    db.commit()


def search_contacts(db: Session, query: str, user: User) -> List[ContactResponse]:
    """
    Searches for a user's contacts based on a query.

    Args:
        db (Session): Database session.
        query (str): Search query.
        user (User): User whose contacts need to be searched.

    Returns:
        List[ContactResponse]: List of found contacts.
    """
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


def get_contacts_with_upcoming_birthdays(db: Session, user: User) -> List[ContactResponse]:
    """
    Retrieves contacts with upcoming birthdays in the current month.

    Args:
        db (Session): Database session.
        user (User): User whose contacts need to be checked.

    Returns:
        List[ContactResponse]: List of contacts with upcoming birthdays.
    """
    today = datetime.utcnow().date()
    next_month = today.replace(day=1) + timedelta(days=31)
    next_month = next_month.replace(day=1)
    return (
        db.query(models.Contact)
        .filter(
            models.Contact.owner_id == user.id,
            models.Contact.birthday.between(
                today.replace(year=today.year),
                next_month.replace(year=today.year)
            ),
        )
        .all()
    )
