from telegram import Update
from telegram.ext._callbackcontext import CallbackContext
from telegram.ext import ContextTypes
from loguru import logger


def room_context_validator(f):
    async def wrapper(*args, **kwargs):
        if any([isinstance(args[0], int), isinstance(args[0], Update)]) and isinstance(args[1], CallbackContext):
            update = args[0]
            context: ContextTypes.DEFAULT_TYPE = args[1]
            try:
                room_code = context.user_data["room_code"]
                return await f(*args, **kwargs)
            except KeyError:
                await context.bot.send_message(
                    update.effective_chat.id, text="Room is not selected"
                )

    return wrapper
