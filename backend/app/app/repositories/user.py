from core.repository import BaseRepository

from app.models import User


class UserRepository(BaseRepository[User]):
    """
    User repository provides all the database operations for the User model.
    """

    async def get_by_username(
        self, username: str, join_: set[str] | None = None
    ) -> User | None:
        """
        Get user by username.

        :param username: Username.
        :param join_: Join relations.
        :return: User.
        """
        query = await self._query(join_)
        query = query.filter(User.username == username)
        return await self._one_or_none(query)

    async def get_by_email(
        self, email: str, join_: set[str] | None = None
    ) -> User | None:
        """
        Get user by email.

        :param email: Email.
        :param join_: Join relations.
        :return: User.
        """
        query = await self._query(join_)
        query = query.filter(User.email == email)
        return await self._one_or_none(query)
