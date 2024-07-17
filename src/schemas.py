from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import date, datetime


class UserModel(BaseModel):
    username: str
    email: EmailStr
    password: str = Field(min_length=6, max_length=10)
    avatar: str


class UserDb(BaseModel):
    id: int
    username: str
    email: str
    avatar: str
    created_at: datetime

    class Config:
        from_attributes = True


class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    user: UserDb
    detail: str = "User successfully created"

    class Config:
        from_attributes = True


class TokenModel(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    email: str


class ContactBase(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    phone_number: str
    birthday: date
    additional_info: Optional[str] = None


class ContactCreate(ContactBase):
    pass


class ContactUpdate(ContactBase):
    first_name: Optional[str]
    last_name: Optional[str]
    email: Optional[EmailStr]
    phone_number: Optional[str]
    birthday: Optional[date]
    additional_info: Optional[str]


class ContactInDB(ContactBase):
    id: int

    class Config:
        from_attributes = True


class ContactResponse(ContactBase):
    id: int

    class Config:
        from_attributes = True


class RequestEmail(BaseModel):
    email: EmailStr
