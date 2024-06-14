import datetime

from DataBase.database import db


async def user_registrate(chat_id: int, user_id: int) -> None:
    await db.execute(
        f'INSERT INTO {db.users_by_step} (chat_id, user_id, create_at, status_create_at, time_sending_step) '
        f'VALUES ($1, $2, $3, $3, $3)',
        chat_id, user_id, datetime.datetime.now(),
        execute=True
    )
