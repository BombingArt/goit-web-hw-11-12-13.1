from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import date, datetime


class UserModel(BaseModel):
    """
    Data model for user registration.

    Attributes:
        username (str): The username of the user.
        email (EmailStr): The email address of the user.
        password (str): The password of the user. Must be between 6 and 10 characters.
        avatar (str): URL of the user's avatar.
    """
    username: str
    email: EmailStr
    password: str = Field(min_length=6, max_length=10)
    avatar: str


class UserDb(BaseModel):
    """
    Data model for the user as stored in the database.

    Attributes:
        id (int): The unique identifier of the user.
        username (str): The username of the user.
        email (str): The email address of the user.
        avatar (str): URL of the user's avatar.
        created_at (datetime): The timestamp when the user was created.
    """
    id: int
    username: str
    email: str
    avatar: str
    created_at: datetime

    class Config:
        from_attributes = True


class UserCreate(BaseModel):
    """
    Data model for user creation.

    Attributes:
        username (str): The username of the user.
        email (EmailStr): The email address of the user.
        password (str): The password of the user.
    """
    username: str
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    """
    Response model for user creation.

    Attributes:
        user (UserDb): The created user.
        detail (str): A message indicating successful creation.
    """
    user: UserDb
    detail: str = "User successfully created"

    class Config:
        from_attributes = True


class TokenModel(BaseModel):
    """
    Data model for authentication tokens.

    Attributes:
        access_token (str): The access token.
        refresh_token (str): The refresh token.
        token_type (str): The type of the token, typically 'bearer'.
    """
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    """
    Data model for token data.

    Attributes:
        email (str): The email address associated with the token.
    """
    email: str


class ContactBase(BaseModel):
    """
    Base data model for a contact.

    Attributes:
        first_name (str): The first name of the contact.
        last_name (str): The last name of the contact.
        email (EmailStr): The email address of the contact.
        phone_number (str): The phone number of the contact.
        birthday (date): The birthday of the contact.
        additional_info (Optional[str]): Any additional information about the contact.
    """
    first_name: str
    last_name: str
    email: EmailStr
    phone_number: str
    birthday: date
    additional_info: Optional[str] = None


class ContactCreate(ContactBase):
    """
    Data model for creating a new contact.

    Inherits all attributes from ContactBase.
    """
    pass


class ContactUpdate(ContactBase):
    """
    Data model for updating an existing contact.

    Attributes:
        first_name (Optional[str]): The new first name of the contact (if updating).
        last_name (Optional[str]): The new last name of the contact (if updating).
        email (Optional[EmailStr]): The new email address of the contact (if updating).
        phone_number (Optional[str]): The new phone number of the contact (if updating).
        birthday (Optional[date]): The new birthday of the contact (if updating).
        additional_info (Optional[str]): Any new additional information about the contact (if updating).
    """
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[EmailStr] = None
    phone_number: Optional[str] = None
    birthday: Optional[date] = None
    additional_info: Optional[str] = None


class ContactInDB(ContactBase):
    """
    Data model for a contact as stored in the database.

    Attributes:
        id (int): The unique identifier of the contact.
    """
    id: int

    class Config:
        from_attributes = True


class ContactResponse(ContactBase):
    """
    Response model for a contact.

    Attributes:
        id (int): The unique identifier of the contact.
    """
    id: int

    class Config:
        from_attributes = True


class RequestEmail(BaseModel):
    """
    Data model for requesting an email.

    Attributes:
        email (EmailStr): The email address for which the request is made.
    """
    email: EmailStr
