from decouple import config


class ConfigBot:
    BOT_TOKEN = config('BOT_TOKEN', cast=str)

    try:
        __ADMINS = config('ADMINS', cast=str).split(',')
        ADMINS = [int(admin) for admin in __ADMINS if admin.isdigit()]
    except:
        ADMINS = []

class ConfigDB:
    USERNAME: str = config('POSTGRES_USER')
    PASSWORD: str = config('POSTGRES_PASSWORD')
    DATABASE: str = config('POSTGRES_DB')
    HOST: str =  config('POSTGRES_HOST', default='localhost')
    PORT: int = int(config('POSTGRES_PORT', cast=int, default=5432))

    assert USERNAME and PASSWORD and HOST and DATABASE and PORT, 'DB settings are not set'


class ConfigCatalog:
    ROWS_PER_PAGE_catalog_universities: int = 8
    COLUMNS_PER_ROW_catalog_lessons: int = 2


cnfg_bot = ConfigBot()
cnfg_db = ConfigDB()
cnfg_catalog = ConfigCatalog()
