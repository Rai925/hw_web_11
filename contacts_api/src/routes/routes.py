from typing import List, Optional
from fastapi import APIRouter, HTTPException, Depends, Query
from sqlalchemy.orm import Session
from ..database.db import get_db
from ..database.models import Contact
from ..repository.repository import create_contact, get_contacts, get_contact, update_contact, delete_contact, \
    search_contacts, get_contacts_birthday_soon
from pydantic import BaseModel, EmailStr

router = APIRouter()


class ContactCreate(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    phone_number: str
    birthday: Optional[str] = None
    additional_info: Optional[str] = None


class ContactUpdate(ContactCreate):
    pass


class ContactResponse(ContactCreate):
    id: int


@router.post("/contacts/", response_model=ContactResponse)
def create_new_contact(contact: ContactCreate, db: Session = Depends(get_db)):
    try:
        db_contact = create_contact(db, contact.dict())
        return db_contact
    except Exception as e:
        print(f"Error in create_new_contact: {e}")  # or use logging
        raise HTTPException(status_code=500, detail="Internal Server Error")


@router.get("/contacts/", response_model=List[ContactResponse])
def read_contacts(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    contacts = get_contacts(db, skip=skip, limit=limit)
    return contacts


@router.get("/contacts/search/", response_model=List[ContactResponse])
def search_contacts_route(name: Optional[str] = None, email: Optional[str] = None, db: Session = Depends(get_db)):
    return search_contacts(db, name, email)


@router.get("/contacts/birthday/", response_model=List[ContactResponse])
def contacts_birthday_soon(days: int = 7, db: Session = Depends(get_db)):
    return get_contacts_birthday_soon(db, days)


@router.get("/contacts/{contact_id}", response_model=ContactResponse)
def read_contact(contact_id: int, db: Session = Depends(get_db)):
    db_contact = get_contact(db, contact_id)
    if db_contact is None:
        raise HTTPException(status_code=404, detail="Contact not found")
    return db_contact


@router.put("/contacts/{contact_id}", response_model=ContactResponse)
def update_contact(contact_id: int, contact: ContactUpdate, db: Session = Depends(get_db)):
    db_contact = update_contact(db, contact_id, contact.dict())
    if db_contact is None:
        raise HTTPException(status_code=404, detail="Contact not found")
    return db_contact


@router.delete("/contacts/{contact_id}", response_model=ContactResponse)
def delete_contact(contact_id: int, db: Session = Depends(get_db)):
    db_contact = delete_contact(db, contact_id)
    if db_contact is None:
        raise HTTPException(status_code=404, detail="Contact not found")
    return db_contact



