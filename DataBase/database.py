from typing import Union, Any

import asyncpg
from asyncpg.pool import Pool

from Exception.exception import DataBaseException
from Logger.logger import logger
from config import DB_NAME, DB_USER, DB_PASS, DB_HOST, DB_PORT


class DataBase:
    def __init__(self):
        self.pool: Union[Pool, None] = None

        """ Таблицы базы данных """
        self.users_by_step = "users_by_step"

    async def run(self):

        await self.connect()

        if self.pool is None:
            logger.info("База данных не существует. Создание базы данных...")
            await self.create_db()

            if self.pool is None:
                raise DataBaseException("Возникла ошибка при создании бд!")
            await self.create_table()
        else:
            await self.check_table()

    async def connect(self):
        try:
            self.pool = await asyncpg.create_pool(
                database=DB_NAME,
                user=DB_USER,
                password=DB_PASS,
                host=DB_HOST,
                port=DB_PORT
            )
        except Exception as error:
            logger.error(f"ERROR connection: {error}")
            self.pool = None

    async def create_db(self):
        try:
            self.pool = await asyncpg.create_pool(
                user=DB_USER,
                password=DB_PASS,
                host=DB_HOST,
                port=DB_PORT
            )

            await self.pool.execute(
                f'CREATE DATABASE {DB_NAME} OWNER {DB_USER}'
            )

            await self.create_table()

        except Exception as error:
            logger.error(f"ERROR connection and create db: {error}")
            self.pool = None

    async def check_table(self):
        tables = [
            table[0] for table in await self.execute(
                sql="""
                        SELECT table_name 
                        FROM information_schema.tables 
                        WHERE table_schema = 'public' AND table_type = 'BASE TABLE'
                    """,
                fetch=True
            )
        ]
        await self.create_table(tables)

    async def create_table(self, tables: list = None) -> None:
        if self.users_by_step not in tables or tables is None:
            await self.create_table_get_users_by_step()

    async def execute(
            self,
            sql: str,
            *args,
            fetch: bool = False,
            fetchval: bool = False,
            fetchrow: bool = False,
            execute: bool = False
    ) -> None or Any:
        async with self.pool.acquire() as connection:
            if execute:
                await connection.execute(sql, *args)
            elif fetch:
                return await connection.fetch(sql, *args)
            elif fetchval:
                return await connection.fetchval(sql, *args)
            elif fetchrow:
                return await connection.fetchrow(sql, *args)

    async def create_table_get_users_by_step(self):
        await self.execute(
            sql=f"""
                        CREATE TABLE IF NOT EXISTS {self.users_by_step} (
                                id SERIAL PRIMARY KEY,
                                chat_id bigint NOT NULL,
                                user_id int NOT NULL,
                                step int DEFAULT 1,
                                create_at timestamp NOT NULL,
                                status varchar(10) DEFAULT 'alive',
                                trigger varchar(15) DEFAULT 'No',
                                status_create_at timestamp NOT NULL,
                                time_sending_step timestamp NOT NULL                
                        )
                """,
            execute=True
        )
        logger.info(f"Created table {self.users_by_step}")


db = DataBase()
