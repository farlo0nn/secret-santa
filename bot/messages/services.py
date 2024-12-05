import db.services as db


from static_data import messages as static
from telegram.constants import ParseMode
from telegram.ext import ContextTypes, ConversationHandler
from ..keyboards import main_menu_keyboard, my_rooms_inline_keyboard, room_menu_keyboard
from loguru import logger


async def _send_message(message, user_id, context, reply_markup=None):
    await context.bot.send_message(
        chat_id=user_id,
        text=message,
        reply_markup=reply_markup,
        parse_mode=ParseMode.HTML,
    )


async def send_invalid_room_context_message(
    user_id, context: ContextTypes.DEFAULT_TYPE
):
    await _send_message(
        static.invalid_room_context_message,
        user_id,
        context,
        reply_markup=main_menu_keyboard(),
    )


async def send_roles(
    giver_chat_id, receiver_chat_id, context: ContextTypes.DEFAULT_TYPE
) -> None:
    receiver_username = db.get_user_username(receiver_chat_id)
    if receiver_username is not None:
        await _send_message(
            static.give_to_message.format(receiver_username=receiver_username),
            giver_chat_id,
            context,
        )


async def send_invalid_message(user_id, context: ContextTypes.DEFAULT_TYPE) -> None:
    await _send_message(static.invalid_message, user_id, context)


async def start(admin_id, username, context: ContextTypes.DEFAULT_TYPE):
    db.create_user(admin_id, username)
    await _send_message(
        static.start_message, admin_id, context, reply_markup=main_menu_keyboard()
    )


async def create_room(user_id, context: ContextTypes.DEFAULT_TYPE) -> None:
    db.create_room(admin_id=user_id)
    await _send_message(static.new_room_message, user_id, context)


async def my_rooms(user_id, context: ContextTypes.DEFAULT_TYPE):
    room_codes = db.get_my_room_codes(user_id)
    if len(room_codes) == 0:
        return await _send_message(static.no_created_rooms_message, user_id, context)

    await _send_message(
        static.my_rooms_message,
        user_id,
        context,
        reply_markup=my_rooms_inline_keyboard(room_codes),
    )


async def room_choice(user_id, context: ContextTypes.DEFAULT_TYPE):

    room_code = context.user_data["room_code"]
    
    if room_code:
        if db.room_exists(room_code):
            pass
        else:
            return await _send_message(static.room_doesnt_exist_message.format(room_code), user_id, context)
    user_is_admin = db.user_is_admin(user_id, room_code)

    return await _send_message(
        static.room_selected_message.format(room_code=room_code),
        user_id,
        context,
        reply_markup=room_menu_keyboard(user_is_admin),
    )


async def assign_roles(user_id, context: ContextTypes.DEFAULT_TYPE):
    response = db.assign_roles(context.user_data["room_code"])

    if response.valid:
        for giver_receiver_pair in response.data:
            await send_roles(
                giver_chat_id=giver_receiver_pair.giver_chat_id,
                receiver_chat_id=giver_receiver_pair.receiver_chat_id,
                context=context,
            )
    else:
        await _send_message(static.roles_already_assigned, user_id, context)


async def people_list(user_id, context: ContextTypes.DEFAULT_TYPE):
    room_code = context.user_data["room_code"]
    usernames = db.get_room_people_list(room_code)
    admin_username = db.get_room_admin(room_code)
    await _send_message(
        static.people_list_message.format(
            room_code=room_code,
            admin_username=admin_username,
            usernames_string="\n".join(usernames),
        ),
        user_id,
        context,
    )


async def delete_room(user_id, context: ContextTypes.DEFAULT_TYPE):
    room_code = context.user_data["room_code"]

    db.delete_room(room_code)
    await _send_message(
        static.delete_room_message.format(room_code),
        user_id,
        context,
        reply_markup=main_menu_keyboard(),
    )


async def return_to_menu(user_id, context: ContextTypes.DEFAULT_TYPE):
    await _send_message(
        static.return_to_menu_message,
        user_id,
        context,
        reply_markup=main_menu_keyboard(),
    )
