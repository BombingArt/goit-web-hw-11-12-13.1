from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from typing import List

from src.database import db
from src.database.db import get_db
from src.repository import contacts
from src.schemas import ContactCreate, ContactUpdate, ContactResponse
from src.database.models import User, Contact
from src.services.auth import auth_service

from fastapi_limiter.depends import RateLimiter

router = APIRouter(prefix="/contacts", tags=["contacts"])


@router.post(
    "/contacts/",
    response_model=ContactResponse,
    status_code=status.HTTP_201_CREATED,
    description="No more than 10 requests per minute",
    dependencies=[Depends(RateLimiter(times=10, seconds=60))],
)
def create_contact(
    contact: ContactCreate,
    db: Session = Depends(db.get_db),
    current_user: User = Depends(auth_service.get_current_user),
):
    return contacts.create_contact(db=db, contact=contact, user=current_user)


@router.get(
    "/contacts/",
    response_model=List[ContactResponse],
    description="No more than 10 requests per minute",
    dependencies=[Depends(RateLimiter(times=10, seconds=60))],
)
def read_contacts(
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(db.get_db),
    current_user: User = Depends(auth_service.get_current_user),
):
    return contacts.get_contacts(db=db, skip=skip, limit=limit, user=current_user)


@router.get(
    "/contacts/{contact_id}",
    response_model=ContactResponse,
    description="No more than 10 requests per minute",
    dependencies=[Depends(RateLimiter(times=10, seconds=60))],
)
def read_contact(
    contact_id: int,
    db: Session = Depends(db.get_db),
    current_user: User = Depends(auth_service.get_current_user),
):
    db_contact = contacts.get_contact(db=db, contact_id=contact_id, user=current_user)
    if db_contact is None:
        raise HTTPException(status_code=404, detail="Contact not found")
    return db_contact


@router.put(
    "/contacts/{contact_id}",
    response_model=ContactResponse,
    status_code=status.HTTP_200_OK,
)
def update_contact(
    contact_id: int,
    contact: ContactUpdate,
    db: Session = Depends(get_db),
    user: User = Depends(auth_service.get_current_user),
):
    db_contact = db.query(Contact).filter(Contact.id == contact_id).first()
    if not db_contact:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found"
        )

    if db_contact.owner_id != user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to update this contact",
        )

    if (
        contact.first_name == db_contact.first_name
        and contact.last_name == db_contact.last_name
        and contact.email == db_contact.email
        and contact.phone_number == db_contact.phone_number
        and contact.birthday == db_contact.birthday
        and contact.additional_info == db_contact.additional_info
    ):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No changes detected for the contact",
        )

    if contact.first_name is not None:
        db_contact.first_name = contact.first_name
    if contact.last_name is not None:
        db_contact.last_name = contact.last_name
    if contact.email is not None:
        db_contact.email = contact.email
    if contact.phone_number is not None:
        db_contact.phone_number = contact.phone_number
    if contact.birthday is not None:
        db_contact.birthday = contact.birthday
    if contact.additional_info is not None:
        db_contact.additional_info = contact.additional_info

    try:
        db.commit()
        db.refresh(db_contact)
    except IntegrityError as e:
        db.rollback()
        if "ix_contacts_email" in str(e.orig):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="A contact with this email already exists.",
            )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while updating the contact",
        )
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while updating the contact",
        )

    return db_contact


@router.delete("/contacts/{contact_id}")
def delete_contact(
    contact_id: int,
    db: Session = Depends(db.get_db),
    current_user: User = Depends(auth_service.get_current_user),
):
    contacts.delete_contact(db=db, contact_id=contact_id, user=current_user)
    return {"detail": "Contact deleted"}


@router.get(
    "/contacts/search/",
    response_model=List[ContactResponse],
    description="No more than 10 requests per minute",
    dependencies=[Depends(RateLimiter(times=10, seconds=60))],
)
def search_contacts_api(
    query: str = Query(
        ..., description="Search query for first name, last name, or email"
    ),
    db: Session = Depends(db.get_db),
    current_user: User = Depends(auth_service.get_current_user),
):
    return contacts.search_contacts(db=db, query=query, user=current_user)


@router.get("/contacts/birthdays/", response_model=List[ContactResponse])
def get_contacts_with_upcoming_birthdays(
    db: Session = Depends(db.get_db),
    current_user: User = Depends(auth_service.get_current_user),
):
    return contacts.get_contacts_with_upcoming_birthdays(db=db, user=current_user)
