from decouple import config


class Settings:
    BOT_TOKEN = config('BOT_TOKEN', cast=str)

    try:
        __ADMINS = config('ADMINS', cast=str).split(',')
        ADMINS = [int(admin) for admin in __ADMINS if admin.isdigit()]
    except:
        ADMINS = []

class SettingsDB:
    USERNAME = config('USERNAME')
    PASSWORD = config('PASSWORD')
    HOST = config('HOST')
    DATABASE = config('DATABASE')


settings = Settings()
settingsDB = SettingsDB()