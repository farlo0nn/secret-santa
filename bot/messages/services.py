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
    giver_chat_id, context: ContextTypes.DEFAULT_TYPE
) -> None:
    await people_list(giver_chat_id, context)


async def send_invalid_message(user_id, context: ContextTypes.DEFAULT_TYPE) -> None:
    await _send_message(static.invalid_message, user_id, context)


async def start(user_id, username, context: ContextTypes.DEFAULT_TYPE):
    
    await _send_message(
        static.start_message.format(username=username), user_id, context
    )


async def create_user(user_id, username, context: ContextTypes.DEFAULT_TYPE):
    db.create_user(user_id, username)
    await _send_message(
        "Вы завершили регистрацию\nЮзернейм - {username}".format(username=username),
        user_id,
        context,
        reply_markup=main_menu_keyboard()
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
        reply_markup=room_menu_keyboard(user_is_admin=user_is_admin, roles_assigned=db.roles_assigned(room_code)),
    )


async def assign_roles(user_id, context: ContextTypes.DEFAULT_TYPE):
    response = db.assign_roles(context.user_data["room_code"])

    if response.valid:
        for giver_receiver_pair in response.data:
            await send_roles(
                giver_chat_id=giver_receiver_pair.giver_chat_id,
                context=context,
            )
    else:
        await _send_message(static.roles_already_assigned, user_id, context)


async def people_list(user_id, context: ContextTypes.DEFAULT_TYPE):

    room_code = context.user_data["room_code"]

    await _send_message(
        get_room_info(user_id, context)
        ,
        user_id,
        context,
        reply_markup=room_menu_keyboard(db.user_is_admin(user_id,room_code),roles_assigned=db.roles_assigned(room_code))
    )

def get_room_info(user_id, context):

    room_code = context.user_data["room_code"]
    usernames = db.get_room_people_list(room_code)
    admin_username = db.get_room_admin(room_code)
    gift_assignment = db.get_gift_assignment(user_id, room_code)
    info_message = static.people_list_message.format(
            room_code=room_code,
            admin_username=admin_username,
            usernames_string="\n➖".join(usernames),
        )
    if gift_assignment.valid:
        info_message += static.assignment_message.format(receiver=gift_assignment.data.receiver_username)
        wish_list = db.get_user_wish_list(gift_assignment.data.receiver_id, room_code)  
        if wish_list != None:
            logger.debug(wish_list)
            info_message += static.users_wishes_message.format(wish_list=", ".join(wish_list))
    else:
        info_message += static.roles_are_not_assigned
    return info_message
    


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

async def leave_room(user_id, context: ContextTypes.DEFAULT_TYPE):
    room_code = context.user_data["room_code"]
    if db.user_is_admin(user_id, room_code):
        return static.leave_only_for_admin_message
    db.delete_user_from_room(user_id, room_code)
    await _send_message(
        static.successful_leave,
        user_id,
        context,
        reply_markup=main_menu_keyboard()
    )