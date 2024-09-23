import unittest
from unittest.mock import MagicMock
from fastapi import HTTPException
from sqlalchemy.orm import Session
from src.schemas import ContactCreate, ContactUpdate, ContactResponse
from src.repository.contacts import create_contact, get_contacts, get_contact, update_contact, delete_contact


class TestContactRepository(unittest.TestCase):

    def setUp(self):
        self.db = MagicMock(spec=Session)
        self.user = MagicMock(id=1)

    def test_create_contact_success(self):
        contact_data = ContactCreate(
            first_name="John",
            last_name="Doe",
            email="john@example.com",
            phone_number="1234567890",
            birthday="1990-01-01",
        )
        self.db.query().filter().first.return_value = None
        created_contact = create_contact(self.db, contact_data, self.user)

        self.assertEqual(created_contact.first_name, contact_data.first_name)
        self.assertEqual(created_contact.email, contact_data.email)

    def test_create_contact_conflict(self):
        contact_data = ContactCreate(
            first_name="Jane",
            last_name="Doe",
            email="jane@example.com",
            phone_number="0987654321",
            birthday="1995-01-01",
        )
        # Имитация существующего контакта
        self.db.query().filter().first.return_value = MagicMock()

        with self.assertRaises(HTTPException) as context:
            create_contact(self.db, contact_data, self.user)

        self.assertEqual(context.exception.status_code, 409)

    def test_get_contacts(self):
        self.db.query().filter().offset().limit().all.return_value = [
            MagicMock()]  # Имитация списка контактов
        contacts = get_contacts(self.db, self.user)
        self.assertIsInstance(contacts, list)

    def test_get_contact_success(self):
        contact_id = 1
        # Имитация найденного контакта
        self.db.query().filter().first.return_value = MagicMock()
        contact = get_contact(self.db, contact_id, self.user)
        self.assertIsNotNone(contact)

    def test_get_contact_not_found(self):
        contact_id = 999
        self.db.query().filter().first.return_value = None

        with self.assertRaises(HTTPException) as context:
            get_contact(self.db, contact_id, self.user)

        self.assertEqual(context.exception.status_code, 404)

    def test_update_contact_success(self):
        contact_id = 1
        existing_contact = MagicMock()
        self.db.query().filter().first.return_value = existing_contact

        update_data = ContactUpdate(
            first_name="Updated Name",
            last_name=None,  # Не обновляем фамилию
            email=None,  # Не обновляем email
            phone_number="1111111111",
            birthday=None,
            additional_info=None,
        )

        updated_contact = update_contact(
            self.db, contact_id, update_data, self.user)
        self.assertEqual(updated_contact.first_name, "Updated Name")
        self.db.commit.assert_called_once()

    def test_update_contact_not_found(self):
        contact_id = 999
        self.db.query().filter().first.return_value = None

        update_data = ContactUpdate(
            first_name="Updated Name",
            last_name="Doe",
            email="updated@example.com",
            phone_number="2222222222",
            birthday="1992-02-02",
        )

        with self.assertRaises(HTTPException) as context:
            update_contact(self.db, contact_id, update_data, self.user)

        self.assertEqual(context.exception.status_code, 404)

    def test_delete_contact_success(self):
        contact_id = 1
        existing_contact = MagicMock()
        self.db.query().filter().first.return_value = existing_contact

        delete_contact(self.db, contact_id, self.user)
        self.db.delete.assert_called_once_with(existing_contact)
        self.db.commit.assert_called_once()

    def test_delete_contact_not_found(self):
        contact_id = 999
        self.db.query().filter().first.return_value = None

        with self.assertRaises(HTTPException) as context:
            delete_contact(self.db, contact_id, self.user)

        self.assertEqual(context.exception.status_code, 404)


if __name__ == "__main__":
    unittest.main()
