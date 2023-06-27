import os
from dotenv import load_dotenv


class ParseEnv:

    USER_MQ = None
    PASSWD_MQ = None
    JWT_REFRESH_KEY = None
    REFRESH_TIME = None
    ACCESS_TIME = None
    ALGORITHM = None
    JWT_SECRET_KEY = None

    @property
    def db_name(self):
        if not self._db:
            raise ValueError("DB ERROR")
        return self._db

    @db_name.setter
    def db_name(self, name):
        self._db = name

    @property
    def host_value(self):
        if not self._host:
            raise ValueError("HOST ERROR")
        return self._host

    @property
    def user_name(self):
        if not self._user:
            raise ValueError("USER ERROR")
        return self._user

    @property
    def passwd(self):
        if not self._passwd:
            raise ValueError("PASSWORD ERROR")
        return self._passwd

    def __init__(self):
        load_dotenv()
        self._db = os.getenv("DB_PG")
        self._host = os.getenv("HOST_PG")
        self._user = os.getenv("USER_PG")
        self._passwd = os.getenv("PASSWD_PG")
        ParseEnv.JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
        ParseEnv.ALGORITHM = os.getenv("ALGORITHM")
        ParseEnv.ACCESS_TIME = os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES")
        ParseEnv.REFRESH_TIME = os.getenv("REFRESH_TOKEN_EXPIRE_MINUTES")
        ParseEnv.JWT_REFRESH_KEY = os.getenv("JWT_REFRESH_SECRET_KEY")
        ParseEnv.USER_MQ = os.getenv("USER_MQ")
        ParseEnv.PASSWD_MQ = os.getenv("PASSWD_MQ")
        