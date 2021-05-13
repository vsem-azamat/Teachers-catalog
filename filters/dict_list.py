from aiogram import types
from aiogram.dispatcher.filters import BoundFilter

dict_univ = {'list_cvut': 'cvut', 'list_uk': 'uk', 'list_vse': 'vse',
             'list_czu': 'czu', 'list_vut': 'vut', 'list_masaryk': 'masaryk'}
dict_less = {'list_math': 'math', 'list_nostr': 'nostr', 'list_boil': 'biol', 'list_chem': 'chem',
             'list_czech': 'czech', 'list_engl': 'engl'}


class DictList(BoundFilter):  # filter for dict of teachers
    async def check(self, callback_query: types.CallbackQuery) -> bool:
        return callback_query.data in dict_univ or callback_query.data in dict_less
