from models.user_model.user_model import UserRegistration
from repository.core.core import DbConnection, fetch_row_transaction, insert_row_transaction
from dataclasses import dataclass
from repository.user_db_manager.user_db_interface import UserDbInterface
from asyncpg import Record


@dataclass
class UserDbManager(UserDbInterface):

    @staticmethod
    async def get_user_from_db(*, username) -> Record:
        _user_info = await fetch_row_transaction("""select * from users where u_username = $1""", username)
        return _user_info

    @staticmethod
    async def add_user_to_db(add_user_data: UserRegistration) -> bool | None:
        _user_add_state = await insert_row_transaction(
            """
            INSERT INTO users (u_username, u_phone) VALUES($1, $2)
            """,
            add_user_data.user_name,
            add_user_data.user_phone
        )
        return _user_add_state
