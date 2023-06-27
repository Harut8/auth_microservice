import asyncio
from typing import Callable
from repository.core.core_exceptions import CoreError
import asyncpg
from repository.core.core_interface import DbConnectionInterface
from asyncpg import Pool
from service.parser import ParseEnv


def transaction(func: Callable):
    try:
        async def wrapper(*args, **kwargs):
            async with DbConnection() as connection:
                async with connection.acquire() as db:
                    async with db.transaction():
                        return await func(*args, db)
        return wrapper
    except Exception as e:
        raise Exception(e)


@transaction
async def fetch_row_transaction(query, db=None, *args):
    info = None
    if args:
        info = await db.fetchrow(query, *args)
    else:
        info = await db.fetchrow(query)
    return info


@transaction
async def insert_row_transaction(query, db=None, *args):
    if args:
        await db.execute(query, *args)
        return 1
    else:
        await db.execute(query)
        return 1


class DbConnection(DbConnectionInterface):

    @staticmethod
    async def create_connection():
        print("ENV PARSED")
        await DbConnection()._set_connection()

    @staticmethod
    async def abort_connection():
        await DbConnection().abort()

    async def _set_connection(self):
        try:
            __db: str = self._parser.db_name
            __host: str = self._parser.host_value
            __username: str = self._parser.user_name
            __passwd: str = self._parser.passwd
            __dsn = "postgres://"+__username+":"+__passwd+"@"+__host+":5432"+"/"+__db
            self.connection = await asyncpg.pool.create_pool(
                dsn=__dsn
            )
            print("CONNECTION CREATED")
        except Exception as e:
            raise CoreError(e, 'Connection Error, Check: DB, HOST, PASSWORD, USERNAME')

    @property
    def connection(self):
        if not self._connection:
            raise CoreError("No Connection")
        return self._connection

    @connection.setter
    def connection(self, value: Pool):
        self._connection: Pool = value

    def __new__(cls, *args, **kwargs):
        try:
            if not hasattr(cls, 'single'):
                cls.single = super(DbConnection, cls).__new__(cls, *args, **kwargs)
                cls.single._parser = ParseEnv()
            return cls.single
        except Exception as e:
            raise CoreError(e, 'Parse Error')

    def __init__(self):
        if not self.single:
            self._connection: Pool | None = None

    async def __aenter__(self) -> Pool:
        return self.connection

    async def __aexit__(self, *arg):
        # await self.abort()
        ...

    async def abort(self):
        try:
            if self.connection is not None:
                await self.connection.close()
                print("CONNECTION CLOSED")
        except Exception as e:
            raise CoreError(e, 'Connection Closing Failed')

