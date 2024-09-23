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
    "/",
    response_model=ContactResponse,
    status_code=status.HTTP_201_CREATED,
    description="No more than 10 requests per minute",
    dependencies=[Depends(RateLimiter(times=10, seconds=60))],
)
def create_contact(
    contact: ContactCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(auth_service.get_current_user),
):
    """
    Creates a new contact.

    Adds a new contact to the database for the currently authenticated user.

    Args:
        contact (ContactCreate): Data for creating a new contact.
        db (Session): Database session.
        current_user (User): The currently authenticated user.

    Returns:
        ContactResponse: The created contact.

    Raises:
        HTTPException: If the contact creation fails.
    """
    return contacts.create_contact(db=db, contact=contact, user=current_user)


@router.get(
    "/",
    response_model=List[ContactResponse],
    description="No more than 10 requests per minute",
    dependencies=[Depends(RateLimiter(times=10, seconds=60))],
)
def read_contacts(
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db),
    current_user: User = Depends(auth_service.get_current_user),
):
    """
    Retrieves contacts for the currently authenticated user.

    Args:
        skip (int): Number of contacts to skip for pagination.
        limit (int): Number of contacts to return.
        db (Session): Database session.
        current_user (User): The currently authenticated user.

    Returns:
        List[ContactResponse]: List of contacts.

    Raises:
        HTTPException: If there is an issue retrieving the contacts.
    """
    return contacts.get_contacts(db=db, skip=skip, limit=limit, user=current_user)


@router.get(
    "/{contact_id}",
    response_model=ContactResponse,
    description="No more than 10 requests per minute",
    dependencies=[Depends(RateLimiter(times=10, seconds=60))],
)
def read_contact(
    contact_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(auth_service.get_current_user),
):
    """
    Retrieves a specific contact by ID.

    Args:
        contact_id (int): ID of the contact to retrieve.
        db (Session): Database session.
        current_user (User): The currently authenticated user.

    Returns:
        ContactResponse: The requested contact.

    Raises:
        HTTPException: If the contact is not found or access is forbidden.
    """
    db_contact = contacts.get_contact(
        db=db, contact_id=contact_id, user=current_user)
    if db_contact is None:
        raise HTTPException(status_code=404, detail="Contact not found")
    return db_contact


@router.put(
    "/{contact_id}",
    response_model=ContactResponse,
    status_code=status.HTTP_200_OK,
)
def update_contact(
    contact_id: int,
    contact: ContactUpdate,
    db: Session = Depends(get_db),
    user: User = Depends(auth_service.get_current_user),
):
    """
    Updates an existing contact.

    Args:
        contact_id (int): ID of the contact to update.
        contact (ContactUpdate): Data to update the contact.
        db (Session): Database session.
        user (User): The currently authenticated user.

    Returns:
        ContactResponse: The updated contact.

    Raises:
        HTTPException: If the contact is not found, no changes are detected, or the user does not have permission to update the contact.
    """
    db_contact = db.query(Contact).filter(Contact.id == contact_id).first()
    if not db_contact:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found")

    if db_contact.owner_id != user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="You do not have permission to update this contact")

    # Обновление данных
    for attr, value in contact.dict(exclude_unset=True).items():
        setattr(db_contact, attr, value)

    try:
        db.commit()
        db.refresh(db_contact)
    except IntegrityError as e:
        db.rollback()
        if "ix_contacts_email" in str(e.orig):
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                                detail="A contact with this email already exists.")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail="An error occurred while updating the contact")

    return db_contact


@router.delete("/{contact_id}")
def delete_contact(
    contact_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(auth_service.get_current_user),
):
    """
    Deletes a contact.

    Args:
        contact_id (int): ID of the contact to delete.
        db (Session): Database session.
        current_user (User): The currently authenticated user.

    Returns:
        dict: Message indicating the contact has been deleted.

    Raises:
        HTTPException: If the contact deletion fails.
    """
    contacts.delete_contact(db=db, contact_id=contact_id, user=current_user)
    return {"detail": "Contact deleted"}


@router.get("/search/", response_model=List[ContactResponse])
def search_contacts_api(
    query: str = Query(...,
                       description="Search query for first name, last name, or email"),
    db: Session = Depends(get_db),
    current_user: User = Depends(auth_service.get_current_user),
):
    """
    Searches for contacts based on a query.

    Args:
        query (str): Search query for first name, last name, or email.
        db (Session): Database session.
        current_user (User): The currently authenticated user.

    Returns:
        List[ContactResponse]: List of contacts matching the search query.

    Raises:
        HTTPException: If there is an issue performing the search.
    """
    return contacts.search_contacts(db=db, query=query, user=current_user)


@router.get("/birthdays/", response_model=List[ContactResponse])
def get_contacts_with_upcoming_birthdays(
    db: Session = Depends(get_db),
    current_user: User = Depends(auth_service.get_current_user),
):
    """
    Retrieves contacts with upcoming birthdays.

    Args:
        db (Session): Database session.
        current_user (User): The currently authenticated user.

    Returns:
        List[ContactResponse]: List of contacts with upcoming birthdays.

    Raises:
        HTTPException: If there is an issue retrieving contacts with upcoming birthdays.
    """
    return contacts.get_contacts_with_upcoming_birthdays(db=db, user=current_user)
