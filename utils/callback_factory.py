from aiogram.filters.callback_data import CallbackData


class CategoryTeachersCallbackFactory(CallbackData, prefix='catteach'):
    category: str
