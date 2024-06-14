import datetime

from sqlite3 import OperationalError
from pyrogram.errors import UserDeactivated, UserDeactivatedBan, ActiveUserRequired, AuthKeyInvalid, AuthKeyPermEmpty, \
    AuthKeyUnregistered, AuthKeyDuplicated, SessionExpired, SessionPasswordNeeded, SessionRevoked, Flood
from aiohttp import ClientConnectorError
from DataBase.update import user_update_step, user_update_status, user_update_step_trigger, user_update_finished, \
    user_update_finished_trigger
from Logger.logger import logger
from Session.app import app


class Worker:
    def __init__(self, user: dict):
        self.actions_phrases = {
            'break':
                ['Прекрасно', 'Ожидать'],
            'skip':
                ['Триггер1']
        }
        self.user = user

    @staticmethod
    async def check_trigger(chat_id: int, user_id: int, actions_phrases: dict, create_at: datetime) -> str or None:
        async for msg in app.get_chat_history(chat_id, limit=50):

            if msg.date > create_at:
                for action, phrases in actions_phrases.items():
                    for phrase in phrases:
                        if msg.text and msg.outgoing \
                                and phrase.lower() in msg.text.lower() \
                                and msg.from_user.id == user_id:
                            return action
        return None

    async def user_trails(self, user: dict, step_: int, values: dict):

        if datetime.datetime.now() > user['time_sending_step'] + datetime.timedelta(minutes=values['time']):

            trigger = await self.check_trigger(
                user['chat_id'], user['user_id'],
                self.actions_phrases, user['create_at'])

            if trigger == 'break':
                await user_update_finished_trigger(
                    user['chat_id'], user['user_id'],
                    'finished', user['create_at'], 'break', datetime.datetime.now()
                )
                return f"create_at: {user['create_at']} | " \
                       f"chat: {user['chat_id']} | " \
                       f"user: {user['user_id']} | " \
                       f"status: 'finished' | " \
                       f"step: {step_} | " \
                       f"trigger: 'break' |"
            elif trigger == 'skip' and step_ == 2:
                await user_update_step_trigger(
                    user['chat_id'], user['user_id'], step_ + 1,
                    user['create_at'], 'skip', datetime.datetime.now()
                )
                return f"create_at: {user['create_at']} | " \
                       f"chat: {user['chat_id']} | " \
                       f"user: {user['user_id']} | " \
                       f"status: 'finished' | " \
                       f"step: {step_} | " \
                       f"trigger: 'skip' |"

            text, check_session = '', True
            try:
                await app.send_message(user['chat_id'], values['text'])
                if step_ == 3:
                    await user_update_finished(
                        user['chat_id'], user['user_id'],
                        'finished', user['create_at'], datetime.datetime.now()
                    )
                    return f"create_at: {user['create_at']} | " \
                           f"chat: {user['chat_id']} | " \
                           f"user: {user['user_id']} | " \
                           f"status: 'finished' | " \
                           f"step: {step_} | " \
                           f"trigger: {user['trigger']} |"
                else:
                    await user_update_step(
                        user['chat_id'], user['user_id'],
                        step_ + 1, user['create_at'], datetime.datetime.now()
                    )
            except OperationalError:
                check_session = False
                text = f"База данных заблокирована у аккаунта!"
            except ClientConnectorError:
                text = f'Ошибка соединения с телеграммом'
            except UserDeactivated:
                check_session = False
                text = f"Аккаунт деактивирован!"
            except UserDeactivatedBan:
                check_session = False
                text = f"Аккаунт деактивирован и заблокирован!️"
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
                await user_update_status(
                    user['chat_id'], user['user_id'],
                    'dead', user['create_at'], datetime.datetime.now()
                )
                return f"create_at: {user['create_at']} | " \
                       f"chat: {user['chat_id']} | " \
                       f"user: {user['user_id']} | " \
                       f"status: 'dead' | " \
                       f"step: {step_} | " \
                       f"trigger: {user['trigger']} |"

        return f"create_at: {user['create_at']} | " \
               f"chat: {user['chat_id']} | " \
               f"user: {user['user_id']} | " \
               f"status: 'alive' | " \
               f"step: {step_} | " \
               f"trigger: {user['trigger']} |"

    async def run(self, step_: int, values: dict):
        return await self.user_trails(self.user, step_, values)
