import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    BOT_TOKEN: str = str(os.getenv('BOT_TOKEN'))
    ADMINS: list[int] = [int(id_admin) for id_admin in os.getenv('ADMINS').split(',')]

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'

class SettingsDB:
    USERNAME: str = str(os.getenv('USERNAME'))
    PASSWORD: str = str(os.getenv('PASSWORD'))
    HOST: str = str(os.getenv('HOST'))
    DATABASE: str = str(os.getenv('DATABASE'))

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'


settings = Settings()
settingsDB = SettingsDB()