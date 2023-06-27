from abc import abstractmethod, ABCMeta
from typing import Union
from models.user_model.user_model import UserInfo, UserRegistration


class UserServiceInterface(metaclass=ABCMeta):

    @staticmethod
    @abstractmethod
    async def get_user_from_db(*, username) -> Union[UserInfo, None]:
        ...

    @staticmethod
    @abstractmethod
    async def add_user_to_db(add_user_data: UserRegistration) -> Union[bool, None]:
        ...
