import db.services as db

from static_data import messages as static
from telegram.constants import ParseMode
from telegram.ext import ContextTypes, ConversationHandler
from telegram import Update, ReplyKeyboardRemove
from ..keyboards import room_menu_keyboard, main_menu_keyboard
from ..validators import room_context_validator
from loguru import logger

ADD_WISH, ENTER_THE_ROOM = 0, 0


@room_context_validator
async def add_wish_start_conversation(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> int:
    """Starts the conversation and asks the user about their gender."""
    logger.debug("start handler")
    wish_list = db.get_user_wishes(
        update.message.from_user.id, context.user_data["room_code"]
    )
    if wish_list is not None:
        context.user_data["wish_list"] = wish_list
        logger.debug(context.user_data["wish_list"])
        wish_list_2_str = ", ".join(context.user_data["wish_list"])
    else:
        wish_list_2_str = "..."
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=f"Write any wish you have\nYour current wishes:\n{wish_list_2_str}\nSend /submit to stop adding wishes.\n\n",
    )
    return ADD_WISH


@room_context_validator
async def add_wish(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Stores the photo and asks for a location."""
    user = update.message.from_user
    wish = update.message.text
    logger.debug(wish)
    wish_list = context.user_data["wish_list"]
    if wish not in wish_list:
        wish_list.append(wish)
        await update.message.reply_text(
            "Wish was added\n\nAre there any wishes?\nSend /submit to stop adding wishes."
        )
    else:
        await update.message.reply_text(
            "This wish is already in your list\n\nAre there any wishes?\nSend /submit to stop adding wishes."
        )

    return ADD_WISH


@room_context_validator
async def submit_wishes(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Cancels and ends the conversation."""
    user_id = update.message.from_user.id
    await update.message.reply_text(
        "Thanks for adding your wishes",
        reply_markup=room_menu_keyboard(user_is_admin=db.user_is_admin(user_id)),
    )
    wish_list = context.user_data["wish_list"]
    room_code = context.user_data["room_code"]
    logger.debug("|".join(wish_list))
    db.add_wish_list(user_id, room_code, wish_list)
    return ConversationHandler.END


# ---------------------


async def enter_the_room_start_conversation(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> int:
    """Starts the conversation and asks the user about their gender."""

    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=f"Type room code\nSend /cancel to get back to main menu\n\n",
        reply_markup=ReplyKeyboardRemove(),
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
                reply_markup=room_menu_keyboard(),
            )
            return ConversationHandler.END
        else:
            await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text="You are already in this room\nSend /cancel to get back to main menu",
            )
    else:
        await update.message.reply_text(
            "Room code is not valid\nSend /cancel to get back to main menu"
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
        chat_id=update.effective_chat.id,
        text="Back to menu",
        reply_markup=main_menu_keyboard(),
    )
    return ConversationHandler.END
