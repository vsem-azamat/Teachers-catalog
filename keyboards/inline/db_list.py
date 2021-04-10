from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

next = InlineKeyboardMarkup(row_width=1,
                            inline_keyboard=[
                                [
                                    InlineKeyboardButton(
                                        text='вперед',
                                        callback_data='next'
                                    )
                                ]
                            ])

back = InlineKeyboardMarkup(row_width=1,
                            inline_keyboard=[
                                [
                                    InlineKeyboardButton(
                                        text='назад',
                                        callback_data='back'
                                    )
                                ]
                            ])

next_back = InlineKeyboardMarkup(row_width=2,
                            inline_keyboard=[
                                [
                                    InlineKeyboardButton(
                                        text='назад',
                                        callback_data='back'
                                    )
                                ],
                                [
                                    InlineKeyboardButton(
                                        text='вперед',
                                        callback_data='next'
                                    )
                                ]
                            ])








