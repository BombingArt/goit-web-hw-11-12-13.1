from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List

from src.database import db
from src.repository import contacts
from src.schemas import ContactCreate, ContactUpdate, ContactResponse



router = APIRouter()

@router.post("/contacts/", response_model=ContactResponse)
def create_contact(contact: ContactCreate, db: Session = Depends(db.get_db)):
    return contacts.create_contact(db=db, contact=contact)

@router.get("/contacts/", response_model=List[ContactResponse])
def read_contacts(skip: int = 0, limit: int = 10, db: Session = Depends(db.get_db)):
    return contacts.get_contacts(db=db, skip=skip, limit=limit)

@router.get("/contacts/{contact_id}", response_model=ContactResponse)
def read_contact(contact_id: int, db: Session = Depends(db.get_db)):
    db_contact = contacts.get_contact(db=db, contact_id=contact_id)
    if db_contact is None:
        raise HTTPException(status_code=404, detail="Contact not found")
    return db_contact

@router.put("/contacts/{contact_id}", response_model=ContactResponse)
def update_contact(contact_id: int, contact: ContactUpdate, db: Session = Depends(db.get_db)):
    return contacts.update_contact(db=db, contact_id=contact_id, contact=contact)

@router.delete("/contacts/{contact_id}")
def delete_contact(contact_id: int, db: Session = Depends(db.get_db)):
    contacts.delete_contact(db=db, contact_id=contact_id)
    return {"detail": "Contact deleted"}

@router.get("/contacts/search/", response_model=List[ContactResponse])
def search_contacts_api(
    query: str = Query(..., description="Search query for first name, last name, or email"),
    db: Session = Depends(db.get_db)
):
    return contacts.search_contacts(db=db, query=query)


@router.get("/contacts/birthdays/", response_model=List[ContactResponse])
def get_contacts_with_upcoming_birthdays(db: Session = Depends(db.get_db)):
    return contacts.get_contacts_with_upcoming_birthdays(db=db)



