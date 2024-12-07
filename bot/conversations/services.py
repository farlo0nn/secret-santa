import db.services as db

from static_data import messages as static
from telegram.constants import ParseMode
from telegram.ext import ContextTypes, ConversationHandler
from telegram import Update, ReplyKeyboardRemove
from ..keyboards import room_menu_keyboard, main_menu_keyboard, submit_wishes_key, cancel_entering_the_room_key
from ..validators import room_context_validator
from loguru import logger

ADD_WISH, ENTER_THE_ROOM = 0, 0


@room_context_validator
async def add_wish_start_conversation(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> int:
    """Starts the conversation and asks the user about their gender."""
    
    wish_list = db.get_user_wish_list(
        update.message.from_user.id, context.user_data["room_code"]
    )
    if wish_list is not None:
        context.user_data["wish_list"] = wish_list
        context.user_data["wish_list_to_add"] = []
        wish_list_2_str = ", ".join(context.user_data["wish_list"])
    else:
        context.user_data["wish_list"] = []
        context.user_data["wish_list_to_add"] = []
        wish_list_2_str = "..."

    # logger.debug("|".join(context.user_data["wish_list"]))

    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Write any wish you have",
        reply_markup=ReplyKeyboardRemove()
    )
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=f"Your current wishes:\n{wish_list_2_str}",
        reply_markup=submit_wishes_key()
    )
    return ADD_WISH


@room_context_validator
async def add_wish(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Stores the photo and asks for a location."""
    user = update.message.from_user
    wish = update.message.text
    wish_list = context.user_data["wish_list"]
    wish_list_to_add = context.user_data["wish_list_to_add"]
    if wish not in wish_list and wish not in wish_list_to_add:
        wish_list_to_add.append(wish)
        await update.message.reply_text(
            "Wish was added\n\nAre there any wishes?",
            reply_markup=submit_wishes_key()
        )
    else:
        await update.message.reply_text(
            "This wish is already in your list\n\nAre there any wishes?",
            reply_markup=submit_wishes_key()
        )

    return ADD_WISH


@room_context_validator
async def submit_wishes(update: Update, context: ContextTypes.DEFAULT_TYPE, query) -> int:
    """Cancels and ends the conversation."""
    await query.answer()
    if query.data == "submit":
        
        wish_list_to_add = context.user_data["wish_list_to_add"]
        wish_list = context.user_data["wish_list"] + wish_list_to_add
        room_code = context.user_data["room_code"]
        user_id = update.effective_chat.id
        await query.delete_message()
        await context.bot.send_message(chat_id=user_id, text=f"Your wishes in this room:\n{", ".join(wish_list)}", reply_markup=room_menu_keyboard(user_is_admin=db.user_is_admin(user_id,room_code)))        
        
        # logger.debug("|".join(wish_list))
        db.add_wish_list(user_id, room_code, wish_list_to_add)

        context.user_data["wish_list"] = []
        context.user_data["wish_list_to_add"] = []
        return ConversationHandler.END


# ---------------------


async def enter_the_room_start_conversation(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> int:
    """Starts the conversation and asks the user about their gender."""
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=f"Type room code",
        reply_markup=cancel_entering_the_room_key()
    )

    
    return ENTER_THE_ROOM

async def enter_the_room(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user_id = update.effective_chat.id
    room_code = update.message.text
    if is_valid_room_code(room_code):
        if user_id not in db.room_members_id(room_code):
            add_to_room(user_id, room_code, context)
            context.user_data["room_code"] = room_code
            await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text="You are successfully added to the room",
                reply_markup=room_menu_keyboard(user_is_admin=db.user_is_admin(user_id,room_code)),
            )
            return ConversationHandler.END
        else:
            await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text="You are already in this room",
                reply_markup=cancel_entering_the_room_key()
            )
    else:
        await update.message.reply_text(
            "Room code is not valid",
            reply_markup=cancel_entering_the_room_key()
        )
        return ENTER_THE_ROOM


def is_valid_room_code(room_code: str):
    if all([isinstance(room_code, str), len(room_code) == 8]):
        if db.room_exists(room_code):
            return True

    return False


def add_to_room(user_id, room_code, context: ContextTypes.DEFAULT_TYPE):
    username = db.add_to_room(user_id=user_id, code=room_code)


async def cancel_entering_the_room(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> int:
    """Cancels and ends the conversation."""
    logger.debug("cancel called")
    await context.bot.send_message(
        chat_id=update,
        text="Back to menu",
        reply_markup=main_menu_keyboard(),
    )
    return ConversationHandler.END
