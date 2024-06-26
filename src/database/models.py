from sqlalchemy import Column, Integer, String, Date
from src.database.db import Base

class Contact(Base):
    __tablename__ = "contacts"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(25), index=True)
    last_name = Column(String(25), index=True)
    email = Column(String, index=True, unique=True)
    phone_number = Column(String(13))
    birthday = Column(Date)
    additional_info = Column(String, nullable=True)
