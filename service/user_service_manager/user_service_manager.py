from repository.user_db_manager.user_db_manager import UserDbManager
from models.user_model.user_model import UserInfo, UserRegistration
from typing import Union
from service.user_service_manager.user_service_interface import UserServiceInterface


class UserServiceManager(UserServiceInterface):

    @staticmethod
    async def get_user_from_db(*, username) -> Union[UserInfo, None]:
        try:
            user_info = await UserDbManager.get_user_from_db(username=username)
            if user_info:
                return UserInfo(**user_info)
            return
        except Exception as e:
            raise e

    @staticmethod
    async def add_user_to_db(add_user_data: UserRegistration) -> Union[bool, None]:
        try:
            user_info = await UserDbManager.get_user_from_db(username=add_user_data.user_name)
            if not user_info:
                _user_add_state = await UserDbManager.add_user_to_db(add_user_data)
                return _user_add_state
            return
        except Exception as e:
            raise e
