import asyncio
from sqlite3 import OperationalError
from typing import Union

from pyrogram import Client, types, filters, idle
from pyrogram.errors import UserDeactivated, UserDeactivatedBan, ActiveUserRequired, AuthKeyInvalid, AuthKeyPermEmpty, \
    AuthKeyUnregistered, AuthKeyDuplicated, SessionExpired, SessionPasswordNeeded, SessionRevoked, Flood
from aiohttp import ClientConnectorError

from Exception.exception import SessionException
from Logger.logger import logger
from config import API_ID, API_HASH


class App:
    def __init__(self):
        self.client: Union[Client, None] = None

    def app(self):
        text, check_session = '', True
        try:
            self.client = Client(
                name="my_bot",
                workdir='Session',
                api_id=API_ID,
                api_hash=API_HASH,
                sleep_threshold=0
            )
            return self.client
        except OperationalError:
            check_session = False
            text = f"База данных заблокирована у аккаунта!"
        except UserDeactivated:
            check_session = False
            text = f"Аккаунт деактивирован!"
        except UserDeactivatedBan:
            check_session = False
            text = f"Аккаунт деактивирован и заблокирован!️"
        except ClientConnectorError:
            text = f'Ошибка соединения с телеграммом'
        except ActiveUserRequired:
            check_session = False
            text = f'Пользователь не активированный!️'
        except AuthKeyInvalid:
            check_session = False
            text = f'Ключ недействителен!️'
        except AuthKeyPermEmpty:
            check_session = False
            text = f'Использовался временный ключ авторизации!'
        except AuthKeyUnregistered:
            check_session = False
            text = f'Пользователь не авторизовался!️'
        except AuthKeyDuplicated:
            check_session = False
            text = f'Дубликат сеанса!'
        except SessionExpired:
            check_session = False
            text = f'Истек срок действия авторизации!'
        except SessionPasswordNeeded:
            check_session = False
            text = f'Использовался временный ключ авторизации!'
        except SessionRevoked:
            check_session = False
            text = f'Авторизация была признана недействительной, так как пользователь завершил все сеансы!'
        except Flood as error:
            logger.info(f'Ошибка сессии users - Заработает через {error.value} секунд(у)')
        except TimeoutError:
            text = f'Вышел таймаут!'
        except Exception as error:
            text = error

        if text:
            text = "Ошибка сессии! " \
                    f"\nСообщение: {text}"
            logger.error(text)

        if not check_session:
            raise SessionException(text)


app = App().app()
