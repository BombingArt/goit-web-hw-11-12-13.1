import unittest
from unittest.mock import AsyncMock, patch
from src.repository.users import get_user_by_email, create_user, confirmed_email, update_avatar
from src.schemas import UserModel


class TestUserRepository(unittest.TestCase):

    def setUp(self):
        self.db = AsyncMock()
        self.mock_user = UserModel(
            username='testuser',
            email='test@example.com',
            password='password',
            avatar='http://example.com/avatar.jpg'
        )

    @patch('repository.users.db')
    async def test_get_user_by_email(self):
        self.db.query.return_value.filter.return_value.first.return_value = self.mock_user

        result = await get_user_by_email(self.mock_user.email, self.db)
        self.assertEqual(result.email, self.mock_user.email)

    @patch('repository.users.db')
    async def test_create_user(self):
        self.db.add = AsyncMock()
        self.db.commit = AsyncMock()
        self.db.refresh = AsyncMock()

        result = await create_user(self.mock_user, self.db)
        self.assertEqual(result.email, self.mock_user.email)

    @patch('repository.users.get_user_by_email')
    @patch('repository.users.db')
    async def test_confirmed_email(self, mock_db, mock_get_user):
        mock_get_user.return_value = self.mock_user
        self.mock_user.confirmed = False

        await confirmed_email(self.mock_user.email, mock_db)
        self.assertTrue(self.mock_user.confirmed)

    @patch('repository.users.get_user_by_email')
    @patch('repository.users.db')
    async def test_update_avatar(self, mock_db, mock_get_user):
        mock_get_user.return_value = self.mock_user
        new_avatar_url = 'http://example.com/new_avatar.jpg'

        result = await update_avatar(self.mock_user.email, new_avatar_url, mock_db)
        self.assertEqual(result.avatar, new_avatar_url)


if __name__ == '__main__':
    unittest.main()
