from abc import abstractmethod, ABCMeta

from asyncpg import Record


class UserDbInterface(metaclass=ABCMeta):

    @staticmethod
    @abstractmethod
    async def get_user_from_db(username) -> Record:
        ...

    @staticmethod
    @abstractmethod
    async def add_user_to_db(username) -> bool | None:
        ...

