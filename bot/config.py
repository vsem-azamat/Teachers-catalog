from email.policy import default
from decouple import config
from typing import List, Optional


class Settings:
    BOT_TOKEN = config('BOT_TOKEN', cast=str)

    try:
        __ADMINS = config('ADMINS', cast=str).split(',')
        ADMINS = [int(admin) for admin in __ADMINS if admin.isdigit()]
    except:
        ADMINS = []

class SettingsDB:
    USERNAME: str = config('DB_USERNAME', default=None)
    PASSWORD: str = config('DB_PASSWORD', default=None)
    HOST: str =  config('DB_HOST', default=None)
    DATABASE: str = config('DB_DATABASE', default=None)
    PORT: int = int(config('DB_PORT', cast=int, default=5432))


    if not USERNAME or not PASSWORD or not HOST or not DATABASE or not PORT:
        raise Exception('DB settings are not set')


settings = Settings()
settingsDB = SettingsDB()