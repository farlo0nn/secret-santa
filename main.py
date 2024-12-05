from bot.application import run_application
from db.models import update_models
from loguru import logger

if __name__ == "__main__":
    # update_models()
    logger.add("log.log", format="{level}|{message}")
    run_application()


# if __name__ == "__main__":
#!/usr/bin/env python
# pylint: disable=unused-argument
# This program is dedicated to the public domain under the CC0 license.


# from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update
# from telegram.ext import (
#     Application,
#     CommandHandler,
#     ContextTypes,
#     ConversationHandler,
#     MessageHandler,
#     filters,
# )
# import config

# # Enable logging

# ADD_WISH = 0
# wish_storage = []

# async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
#     """Starts the conversation and asks the user about their gender."""
#     logger.debug("start handler")
#     await context.bot.send_message(
#         chat_id=update.effective_chat.id,
#         text="Write any wish you have\nSend /submit to stop adding wishes.\n\n"
#     )
#     return ADD_WISH


# async def add_wish(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
#     """Stores the photo and asks for a location."""
#     user = update.message.from_user
#     wish = update.message.text
#     logger.debug(wish)

#     if wish not in wish_storage:
#         wish_storage.append(wish)
#         await update.message.reply_text(
#             "Wish was added\n\nAre there any wishes?\nSend /submit to stop adding wishes.\n\n"
#         )
#     else:
#         await update.message.reply_text(
#             "This wish is already in your list\n\nAre there any wishes?\nSend /submit to stop adding wishes.\n\n"
#         )

#     return ADD_WISH


# async def submit(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
#     """Cancels and ends the conversation."""
#     user = update.message.from_user
#     await update.message.reply_text(
#         "Thanks for adding your wishes", reply_markup=ReplyKeyboardRemove()
#     )
#     logger.debug("|".join(wish_storage))
#     return ConversationHandler.END


# def main() -> None:
#     """Run the bot."""
#     # Create the Application and pass it your bot's token.
#     application = Application.builder().token(config.TG_TOKEN).build()

#     # Add conversation handler with the states GENDER, PHOTO, LOCATION and BIO
#     conv_handler = ConversationHandler(
#         entry_points=[CommandHandler("start", start)],
#         states={
#             ADD_WISH: [CommandHandler("submit", submit), MessageHandler(filters.TEXT, add_wish)],
#             },
#         fallbacks=[CommandHandler("submit", submit)],
#     )

#     application.add_handler(conv_handler)

#     # Run the bot until the user presses Ctrl-C
#     application.run_polling(allowed_updates=Update.ALL_TYPES)


# if __name__ == "__main__":
#     main()
