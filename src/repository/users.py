from sqlalchemy.orm import Session
from src.database.models import User
from src.schemas import UserModel


async def get_user_by_email(email: str, db: Session) -> User:
    """
    Retrieves a user by their email address.

    Args:
        email (str): Email address of the user.
        db (Session): Database session.

    Returns:
        User: The found user, if it exists.
    """
    return db.query(User).filter(User.email == email).first()


async def create_user(body: UserModel, db: Session) -> User:
    """
    Creates a new user and adds them to the database.

    Args:
        body (UserModel): Schema for creating a new user.
        db (Session): Database session.

    Returns:
        User: The created user.
    """
    new_user = User(**body.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


async def update_token(user: User, token: str | None, db: Session) -> None:
    """
    Updates the user's token.

    Args:
        user (User): The user whose token needs to be updated.
        token (str | None): The new token or None to remove the token.
        db (Session): Database session.
    """
    user.refresh_token = token
    db.commit()


async def confirmed_email(email: str, db: Session) -> None:
    """
    Confirms the user's email address.

    Args:
        email (str): Email address of the user.
        db (Session): Database session.
    """
    user = await get_user_by_email(email, db)
    user.confirmed = True
    db.commit()


async def update_avatar(email: str, url: str, db: Session) -> User:
    """
    Updates the user's avatar URL.

    Args:
        email (str): Email address of the user.
        url (str): New avatar URL.
        db (Session): Database session.

    Returns:
        User: The user with the updated avatar URL.
    """
    user = await get_user_by_email(email, db)
    user.avatar = url
    db.commit()
    return user
