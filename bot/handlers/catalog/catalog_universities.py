from aiogram import Router, types, F, Bot
from aiogram.utils.keyboard import InlineKeyboardBuilder

from bot.config import catalog_config
from bot.databases.db_postgresql import db
from bot.text_assets import TextMenu as tm
from bot.utils.callback_factory import CatalogUniversity


router = Router()


@router.callback_query(F.data == 'universities')
async def handler_catalog_universitites(callback: types.CallbackQuery, bot: Bot):
    """
    Show list of Universities.

    🏠 Main menu of catalog
    ├── 🏫 List of Universities (THIS HANDLER)
    │   └── 📚 Lessons of selected University
    │       └── 👩‍🏫 Teachers of selected Lesson
    │           └── 👤 Teacher profile
    ...
    """
    # Text
    user_language = await db.get_user_language(callback.from_user.id)
    text_head = tm.TeachersCategory.text_select_head.get(user_language, 'ru')
    text = tm.TeachersCategory.text_select_university.get(user_language, 'ru')
    
    # Make buttons with universities
    universities = await db.get_universities(exclude_null_teachers=True)
    builder = InlineKeyboardBuilder()
    for university in universities:
        builder.button(
            text = university.name, # type: ignore
            callback_data=CatalogUniversity(
                university_id=university.id, # type: ignore
            )
        )
    columns_per_row = catalog_config.ROWS_PER_PAGE_catalog_universities
    builder.adjust(columns_per_row)
    builder.row(types.InlineKeyboardButton(text='↩️', callback_data='back_menu'))
    # Send message
    await bot.edit_message_text(
        chat_id=callback.from_user.id,
        message_id=callback.message.message_id, 
        text=text_head + text, 
        reply_markup=builder.as_markup()
        )
    await callback.answer()