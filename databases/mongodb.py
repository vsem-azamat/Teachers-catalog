import datetime
import pymongo

from config import settings


class MongoDB:
    def __init__(self):
        self.__conn_str = settings.mongodb_url
        self.client = pymongo.MongoClient(self.__conn_str)
        self.database = self.client['teachers_bot']

        # Collections
        self.users = self.database['users']
        self.teachers = self.database['teachers']
        self.nostrification = self.database['nostrification']
        self.university = self.database['university']

    def new_user(self, id_tg: int, lang: str) -> bool:
        """
        Add a new user to database, if he doesn't exist.

        :returns bool:

        True:   Old user
        False:  New user
        """
        if lang not in ['ru']:
            lang = 'ru'

        key = {'id_tg': id_tg}
        value = {
            "$setOnInsert": {
                "id_tg": id_tg,
                "start_time": datetime.datetime.now(),
                "lang": lang
            }
        }
        result = self.users.update_one(key, value, upsert=True).raw_result
        return result.get('updatedExisting')

    def get_user_lang(self, id_tg: int) -> str | bool:
        key = {"id_tg": id_tg}
        value = {"lang": True}
        try:
            return self.users.find_one(key, value)['lang']
        except TypeError:
            return False

    def update_user_lang(self, id_tg: int, lang: str) -> None:
        key = {"id_tg": id_tg}
        value = {
            "$set": {
                "lang": lang
            }
        }
        self.users.update_one(key, value)

    def do_find(self):
        return self.teachers.find()

    def get_university(self):
        """
        Get list of university.
        """
        return self.university.find({}, { "_id": 0, "name": 1})


mongodb = MongoDB()
