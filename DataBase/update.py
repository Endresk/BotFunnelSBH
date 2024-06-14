import datetime
from DataBase.database import db


async def user_update_step(
        chat_id: int, user_id: int, step: int, create_at: datetime, time_sending_step: datetime) -> None:
    await db.execute(
        f'UPDATE {db.users_by_step} '
        f'SET step = $3, time_sending_step = $4 '
        f'WHERE chat_id = $1 and user_id = $2 and create_at = $5;',
        chat_id, user_id, step, time_sending_step, create_at,
        execute=True
    )


async def user_update_step_trigger(
        chat_id: int, user_id: int, step: int, create_at: datetime, trigger: str, time_sending_step: datetime) -> None:
    await db.execute(
        f'UPDATE {db.users_by_step} '
        f'SET step = $3, time_sending_step = $4, trigger = $6 '
        f'WHERE chat_id = $1 and user_id = $2 and create_at = $5;',
        chat_id, user_id, step, time_sending_step, create_at, trigger,
        execute=True
    )


async def user_update_finished_trigger(
        chat_id: int, user_id: int, status: str, create_at: datetime, trigger: str,
        time_sending_step: datetime) -> None:
    await db.execute(
        f'UPDATE {db.users_by_step} '
        f'SET status = $3, time_sending_step = $4, trigger = $6 '
        f'WHERE chat_id = $1 and user_id = $2 and create_at = $5;',
        chat_id, user_id, status, time_sending_step, create_at, trigger,
        execute=True
    )


async def user_update_status(
        chat_id: int, user_id: int, status: str, create_at: datetime, status_create_at: datetime) -> None:
    await db.execute(
        f'UPDATE {db.users_by_step} '
        f'SET status = $3, status_create_at = $4 '
        f'WHERE chat_id = $1 and user_id = $2 and create_at = $5;',
        chat_id, user_id, status, status_create_at, create_at,
        execute=True
    )


async def user_update_finished(
        chat_id: int, user_id: int, status: str, create_at: datetime, status_create_at: datetime) -> None:
    await db.execute(
        f'UPDATE {db.users_by_step} '
        f'SET status = $3, status_create_at = $4, time_sending_step = $4 '
        f'WHERE chat_id = $1 and user_id = $2 and create_at = $5;',
        chat_id, user_id, status, status_create_at, create_at,
        execute=True
    )
