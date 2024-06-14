import asyncio
import sys
import time
import nest_asyncio
from pyrogram import types, filters, idle
from DataBase.database import db
from DataBase.inserts import user_registrate
from DataBase.selects import user_exists, get_users_by_step
from Logger.logger import logger
from Session.app import app
from Worker.worker import Worker
from config import step, USERNAME


@app.on_message(filters.text & filters.user(USERNAME))
async def on_message(_, msg: types.Message) -> None:
    """

    :param _:
    :param msg:
    """

    if not await user_exists(msg.chat.id, msg.from_user.id):
        await user_registrate(msg.chat.id, msg.from_user.id)


async def steps():

    while app.is_connected is None:
        await asyncio.sleep(1)

    while True:
        for step_, values in step.items():
            users = await get_users_by_step(step_)
            workers = [Worker(user) for user in users]
            tasks = (asyncio.create_task(worker.run(step_, values)) for worker in workers)

            res = await asyncio.gather(*tasks)
            logger.info(f"\n{res}")
        await asyncio.sleep(3)


async def main():
    """

    :return:
    """
    await db.run()

    asyncio.create_task(steps())

    await app.start()
    await idle()
    await app.stop()


if __name__ == '__main__':
    try:
        nest_asyncio.apply()
        asyncio.run(main())
    except KeyboardInterrupt:
        input()
        sys.exit(0)
    except (ValueError, Exception, BaseException) as e:
        logger.info("Global exception: ", e)
        time.sleep(1)
