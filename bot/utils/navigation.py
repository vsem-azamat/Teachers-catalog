from aiogram import types
from typing import List, Optional
from bot.utils.callback_factory import *


EMOJI_NUMBERS = {
        "0": "0️⃣", "1": "1️⃣", "2": "2️⃣", "3": "3️⃣", "4": "4️⃣", 
        "5": "5️⃣", "6": "6️⃣", "7": "7️⃣", "8": "8️⃣", "9": "9️⃣"
        }


async def int_to_emoji(number: int) -> str:
    """
    Convert number to emoji

    Args:
        number (int): Number to convert

    Returns:
        str: Emoji number
    """
    return ''.join([EMOJI_NUMBERS.get(i, '?') for i in str(number)])


def detect_bad_symbols(text: str) -> bool:
    """
    Detect special symbols in text which don't allowed in bot

    Args:
        text (str): Text to check

    Returns:
        bool: True if bad symbols detected
    """
    bad_symbols = ['`', '[', ']', '~', '#', '+', '=', '|', '{', '}', '<', '>', ':']
    return any(char in text for char in bad_symbols)


async def truncate_text(text: str, max_length: int = 225, max_lines: int = 4) -> str:
    """
    Truncate text to max_length and max_lines

    Args:
        text (str): Text to truncate
        max_length (int, optional): Max length of text. Defaults to 225.
        max_lines (int, optional): Max lines of text. Defaults to 4.

    Returns:
        str: Truncated text
    """
    lines = text.split('\n')
    if len(lines) > max_lines:
        text = '\n'.join(lines[:max_lines]) + '.....'
        lines = text.split('\n')
    for i, line in enumerate(lines):
        if len(line) > max_length:
            lines[i] = line[:max_length-3] + '.....'
    return '\n'.join(lines)


# TODO: Re-write this function
async def determine_navigation(
    total_rows: int = 1, current_page: int = 1, rows_per_page: int = 1,
    back_callback: Optional[str] = None, next_callback: Optional[str] = None, return_callback: Optional[str] = None
    ) -> List[types.InlineKeyboardButton]:
    """
    Build navigation buttons for catalog. Determine if is back or next buttons needed with current_page and total_rows

    Args:
        total_rows (int, optional): Total rows in query. Defaults to 1.
        current_page (int, optional): Current page. Defaults to 1.
        rows_per_page (int, optional): Rows per page. Defaults to 1.

        back_button (Optional[str], optional): Callback data for back button. Defaults to None.
        next_button (Optional[str], optional): Callback data for next button. Defaults to None.
        return_button (Optional[str], optional): Callback data for return button. Defaults to None.
    
    Returns:
        List[types.InlineKeyboardButton]: List of navigation buttons
    """
    total_pages = total_rows // rows_per_page + (1 if total_rows % rows_per_page != 0 else 0)
    back = f"◀️{current_page-1}" if current_page > 1 else False
    next = f"{current_page+1}▶️" if current_page < total_pages else False 
    buttons = []
    if back and back_callback:
        buttons.append(
            types.InlineKeyboardButton(
                text=back,
                callback_data=back_callback
            )
        )
    if return_callback:
        buttons.append(
            types.InlineKeyboardButton(
                text="↩️",
                callback_data=return_callback
            )
        )
    if next and next_callback:
        buttons.append(
            types.InlineKeyboardButton(
                text=next,
                callback_data=next_callback
            )
        )
    return buttons
