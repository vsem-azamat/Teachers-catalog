from decouple import config


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


class CatalogConfig:
    ROWS_PER_PAGE_catalog_universities: int = 8
    COLUMNS_PER_ROW_catalog_lessons: int = 2


catalog_config = CatalogConfig()
settings = Settings()
settingsDB = SettingsDB()