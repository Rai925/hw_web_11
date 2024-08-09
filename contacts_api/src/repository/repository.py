from typing import List, Optional
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from ..database.models import Contact


def create_contact(db: Session, contact: dict) -> Contact:
    existing_contact = db.query(Contact).filter(Contact.email == contact.get('email')).first()
    if existing_contact:
        raise ValueError(f"Contact with email {contact['email']} already exists.")

    if 'birthday' in contact and contact['birthday']:
        contact['birthday'] = datetime.strptime(contact['birthday'], '%Y-%m-%d').date()

    db_contact = Contact(**contact)
    db.add(db_contact)
    db.commit()
    db.refresh(db_contact)
    if db_contact.birthday:
        db_contact.birthday = db_contact.birthday.strftime('%Y-%m-%d')
    return db_contact


def get_contacts(db: Session, skip: int = 0, limit: int = 100) -> List[Contact]:
    contacts = db.query(Contact).offset(skip).limit(limit).all()
    for contact in contacts:
        if contact.birthday:
            contact.birthday = contact.birthday.strftime('%Y-%m-%d')
    return contacts


def get_contact(db: Session, contact_id: int) -> Optional[Contact]:
    db_contact = db.query(Contact).filter(Contact.id == contact_id).first()
    if db_contact and db_contact.birthday:
        db_contact.birthday = db_contact.birthday.strftime('%Y-%m-%d')
    return db_contact


def update_contact(db: Session, contact_id: int, contact: dict) -> Optional[Contact]:
    db_contact = db.query(Contact).filter(Contact.id == contact_id).first()
    if db_contact:
        for key, value in contact.items():
            if key == 'birthday' and value:
                value = datetime.strptime(value, '%Y-%m-%d').date()
            setattr(db_contact, key, value)
        db.commit()
        db.refresh(db_contact)
        if db_contact.birthday:
            db_contact.birthday = db_contact.birthday.strftime('%Y-%m-%d')
        return db_contact
    return None


def delete_contact(db: Session, contact_id: int) -> Optional[Contact]:
    db_contact = db.query(Contact).filter(Contact.id == contact_id).first()
    if db_contact:
        db.delete(db_contact)
        db.commit()
        return db_contact
    return None


def search_contacts(
    db: Session, name: Optional[str] = None, email: Optional[str] = None
) -> List[Contact]:
    query = db.query(Contact)
    if name:
        query = query.filter(
            (Contact.first_name.ilike(f"%{name}%"))
            | (Contact.last_name.ilike(f"%{name}%"))
        )
    if email:
        query = query.filter(Contact.email.ilike(f"%{email}%"))
    contacts = query.all()
    for contact in contacts:
        if contact.birthday:
            contact.birthday = contact.birthday.strftime('%Y-%m-%d')
    return contacts


def get_contacts_birthday_soon(db: Session, days: int = 7) -> List[Contact]:
    today = datetime.today().date()
    end_date = today + timedelta(days=days)
    contacts = (
        db.query(Contact)
        .filter(Contact.birthday >= today, Contact.birthday <= end_date)
        .all()
    )
    for contact in contacts:
        if contact.birthday:
            contact.birthday = contact.birthday.strftime('%Y-%m-%d')
    return contacts
