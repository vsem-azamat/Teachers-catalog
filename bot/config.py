from decouple import config


class Settings:
    BOT_TOKEN = config('BOT_TOKEN', cast=str)

    try:
        __ADMINS = config('ADMINS', cast=str).split(',')
        ADMINS = [int(admin) for admin in __ADMINS if admin.isdigit()]
    except:
        ADMINS = []

class SettingsDB:
    USERNAME = config('DB_USERNAME')
    PASSWORD = config('DB_PASSWORD')
    HOST = config('DB_HOST')
    DATABASE = config('DB_DATABASE')
    PORT = config('DB_PORT', cast=int, default=5432)


settings = Settings()
settingsDB = SettingsDB()