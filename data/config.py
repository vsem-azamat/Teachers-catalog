import os

from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = str(os.getenv('BOT_TOKEN'))
admins = [
    268388996
]

# ip = os.getenv('ip')
#
# aiogram_redits = {
#     'host': ip,
# }
#
# redis = {
#     'adress': (ip, 6379),
#     'encoding': 'utf8'
# }