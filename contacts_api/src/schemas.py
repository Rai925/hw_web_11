from typing import List, Optional
from pydantic import BaseModel, EmailStr

class ContactCreate(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    phone_number: str
    birthday: Optional[str] = None  # Змінено на рядок
    additional_info: Optional[str] = None

class ContactUpdate(ContactCreate):
    pass

class ContactResponse(ContactCreate):
    id: int
