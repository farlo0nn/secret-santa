from telegram import (
    KeyboardButton,
    ReplyKeyboardMarkup,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)

from static_data import messages as static


def main_menu_keyboard():
    keyboard = [
        [
            KeyboardButton(static.enter_the_room_option),
            KeyboardButton(static.create_new_room_option),
        ],
        [KeyboardButton(static.my_rooms_option)],
    ]
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)


def my_rooms_inline_keyboard(my_room_codes):

    keyboard = [
        [
            InlineKeyboardButton(
                static.room_info_option.format(room_code=room_code),
                callback_data='rc_'+room_code,
            )
        ]
        for room_code in my_room_codes
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


def submit_wishes_key():

    keyboard = [
        [
            InlineKeyboardButton(
                "Submit",
                callback_data="submit",
            )
        ]
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)

def cancel_entering_the_room_key():

    keyboard = [
        [
            InlineKeyboardButton(
                "Cancel",
                callback_data="cancel",
            )
        ]
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


def room_menu_keyboard(user_is_admin):

    if user_is_admin:
        keyboard = [
            [KeyboardButton(static.assign_roles_option), KeyboardButton(static.people_list_option),],
            [KeyboardButton(static.delete_room_option), KeyboardButton(static.add_wish_option)],
            [KeyboardButton(static.return_to_menu_option)],
        ]
    else:
        keyboard = [
            [KeyboardButton(static.people_list_option),KeyboardButton(static.add_wish_option)],
            [KeyboardButton(static.delete_room_option),KeyboardButton(static.return_to_menu_option)],
        ]

    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)
