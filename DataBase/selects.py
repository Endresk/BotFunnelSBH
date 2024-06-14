from DataBase.database import db


async def user_exists(chat_id: int, user_id: int) -> list:
    return await db.execute(
        f'SELECT * FROM {db.users_by_step} '
        f'WHERE chat_id = $1 and user_id = $2 and status = $3;',
        chat_id, user_id, 'alive',
        fetch=True
    )


async def get_users_by_step(step: int) -> list:
    return await db.execute(
        f'SELECT * FROM {db.users_by_step} '
        f'WHERE step = $1 and status = $2;',
        step, 'alive',
        fetch=True
    )
