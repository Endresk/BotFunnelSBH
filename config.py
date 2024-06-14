from environs import Env

env = Env()
env.read_env()

API_ID = env.int("API_ID")
API_HASH = env.str("API_HASH")

DB_HOST = env.str("DB_HOST")
DB_PORT = env.str("DB_PORT")
DB_NAME = env.str("DB_NAME")
DB_USER = env.str("DB_USER")
DB_PASS = env.str("DB_PASS")

USERNAME = env.str("USERNAME")

step = {
    1: {
        'text': 'Текст1',
        'time': 1
    },
    2: {
        'text': 'Текст2',
        'time': 1
    },
    3: {
        'text': 'Текст3',
        'time': 1
    }
}  # time = минуты
