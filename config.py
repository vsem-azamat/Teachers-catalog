import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    BOT_TOKEN: str = str(os.getenv('BOT_TOKEN'))
    ADMINS: list[int] = [int(id_admin) for id_admin in os.getenv('ADMINS').split(',')]
    mongodb_url: str = str(os.getenv('MONGODB_URL'))

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'


settings = Settings()
