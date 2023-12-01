from aiogram import Router, types, F, Bot
from aiogram.fsm.context import FSMContext
from aiogram.utils.keyboard import InlineKeyboardBuilder

from typing import Optional, Union

from bot.databases.db_postgresql import db
from bot.text_assets import TextMenu as tm
from bot.utils.states import TeacherRegistration
from bot.utils.navigation import *
from bot.utils.filters import TeacherSettingsFilter
from bot.utils.callback_factory import \
    TeacherSettingsMenu, TypeTeacherSettingsMenu, \
    TeacherSettingsEdit, TypeTeacherSettingsEdit

router = Router()


async def teacher_profile_menu(teacher: Teachers, message_or_query: Union[types.Message, types.CallbackQuery], callback_data: Optional[TeacherSettingsMenu] = None) -> Tuple[str, InlineKeyboardBuilder]:
    """
    This function is used when teacher exists.
    Return text and keyboard for teacher profile menu.

    Args:
        teacher (Teachers): Teacher object
        message_or_query (Union[types.Message, types.CallbackQuery]): Message or CallbackQuery
        callback_data (Optional[TeacherSettingsMenu], optional): Callback data. Defaults to None.

    Returns:
        text_menu, builder: Text and InlineKeyboardBuilder
    """
    
    user_language = await db.get_user_language(message_or_query.from_user.id)
    teacher_state = bool(teacher.state)
    text_menu = tm.MyTeachersProfile.text_your_profile.get(user_language, '<b>Menu:</b>')

    builder = tm.MyTeachersProfile.kb_profile_menu(user_language)

    # Teacher has not USERNAME -> show profile and settings
    if not message_or_query.from_user.username:
        # Set teacher.state=False
        await db.teacher_state_update(teacher_id_tg=message_or_query.from_user.id, state=False)
        # Text with request to set USERNAME
        text_login_error = tm.MyTeachersProfile.text_login_error.get(user_language, '')
        # Add text with request to set USERNAME
        text_menu += "\n\n" + text_login_error # type: ignore


    elif isinstance(message_or_query, types.CallbackQuery) and callback_data:
        # Event: profile_activate -> update teacher.state
        if callback_data.menu_type == TypeTeacherSettingsMenu.profile_activate:
            teacher_state = bool(callback_data.state)
            print(message_or_query.from_user.id, teacher_state)
            teacher = await db.teacher_state_update(teacher_id_tg=message_or_query.from_user.id, state=teacher_state)            

    # Build button with teacher.state
    button_state_text = tm.MyTeachersProfile.text_teacher_state.get(teacher_state).get(user_language, 'ru')
    builder.row(
        types.InlineKeyboardButton(
            text=button_state_text,
            callback_data=TeacherSettingsMenu(
                menu_type=TypeTeacherSettingsMenu.profile_activate,
                state=not teacher_state
            ).pack()
        )
    )

    return text_menu, builder


@router.message(TeacherSettingsFilter())
@router.callback_query(TeacherSettingsMenu.filter(F.menu_type == TypeTeacherSettingsMenu.profile))
@router.callback_query(TeacherSettingsMenu.filter(F.menu_type == TypeTeacherSettingsMenu.profile_activate))
async def handler_teachers_profile_menu(message_or_query: Union[types.Message, types.CallbackQuery], state: FSMContext, callback_data: Optional[TeacherSettingsMenu] = None):
    """
    Show teacher profile and settings or offer to create new profile.

    If Teacher profile exists:

    ⚙️ Main menu of teacher profile (THIS HANDLER)
    ├── 📝 Edit profile
    │   ├── 🪧 Edit full profile
    │   ├── 📨 Edit description
    │   └── ↩️ Back to main menu
    │
    ├── 🛒 Add/Remove lessons
    │   ├── 🔠 Languages
    │   ├── 🏫 Universities
    │   │   └── 📚 Lessons of university          
    │   │
    │   ├── 📚 All lessons
    │   └── ↩️ Back to main menu
    │
    └── ✅ Activate/Deactivate profile

    If Teacher profile does not exist:

    Message with offer to create new profile.
    Keyboard:
        - ✅
        - ❌
    """
    user_language = await db.get_user_language(message_or_query.from_user.id)
    teacher = await db.get_teacher(teacher_id_tg=message_or_query.from_user.id)

    # If teacher does not exist -> Send message and return to main menu
    if not teacher:
        text = tm.MyTeachersProfile.text_create_new_profile.get(user_language, 'ru')
        builder_reply = tm.MyTeachersProfile.kb_profile_settings()
        keyboard = builder_reply.as_markup(resize_keyboard=True)
        await message_or_query.answer(text=text, reply_markup=keyboard)
        await state.set_state(TeacherRegistration.start_registration)
        if isinstance(message_or_query, types.CallbackQuery):
            await message_or_query.message.delete()
        return

    # If teacher exists -> Show profile and settings
    text_menu, builder = await teacher_profile_menu(teacher=teacher, message_or_query=message_or_query, callback_data=callback_data)
    builder.adjust(1)
    keyboard = builder.as_markup()

    # Send teacher profile and menu of settings
    if isinstance(message_or_query, types.Message):
        text_profile = await teacher_profile_text(teacher=teacher)
        await message_or_query.answer(text=text_profile)
        await message_or_query.answer(text=text_menu, reply_markup=keyboard)
    
    # Edit message of settings
    elif isinstance(message_or_query, types.CallbackQuery):
        try:
            await message_or_query.message.edit_text(text=text_menu, reply_markup=keyboard)
        finally:
            await message_or_query.answer()


@router.callback_query(TeacherSettingsMenu.filter(F.menu_type == TypeTeacherSettingsMenu.profile_edit))
async def handler_profile_edit(query: types.CallbackQuery, bot: Bot):
    """
    Show menu for edit teacher profile.

    ⚙️ Main menu of teacher profile
    ├── 📝 Edit profile (THIS HANDLER)
    │   ├── 🪧 Edit full profile
    │   ├── 📨 Edit description
    │   └── ↩️ Back to main menu
    │
    ...
    """
    user_language = await db.get_user_language(query.from_user.id)

    # Text
    text_head = tm.MyTeachersProfile.text_profile_lessons_head.get(user_language, 'ru')
    text = tm.MyTeachersProfile.text_profile_select_edit.get(user_language, 'ru')
    
    # Build buttons
    builder = InlineKeyboardBuilder()
    builder.add(
        types.InlineKeyboardButton(
            text=tm.MyTeachersProfile.ti_profile_edit_all.get(user_language, 'ru'),
            callback_data=TeacherSettingsEdit(edit_type=TypeTeacherSettingsEdit.profile_edit_full).pack()
        ),
        types.InlineKeyboardButton(
            text=tm.MyTeachersProfile.ti_profile_edit_description.get(user_language, 'ru'),
            callback_data=TeacherSettingsEdit(edit_type=TypeTeacherSettingsEdit.profile_edit_description).pack()
        ),
        types.InlineKeyboardButton(
            text="↩️",
            callback_data=TeacherSettingsMenu(menu_type=TypeTeacherSettingsMenu.profile).pack()
        ),
    )
    builder.adjust(1)

    # Send message
    await bot.edit_message_text(
        text=text_head + text, 
        chat_id=query.from_user.id, 
        message_id=query.message.message_id,
        reply_markup=builder.as_markup()
        )
