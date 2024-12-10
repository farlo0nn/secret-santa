import config

from telegram.ext import ApplicationBuilder, CallbackQueryHandler
from telegram.ext import Application
from loguru import logger

from .messages.handlers import (
    get_start_handler,
    # get_invalid_messages_handler,
    get_create_room_handler,
    get_my_rooms_handler,
    # get_add_to_room_handler,
    get_room_choice_handler,
    get_assign_roles_handler,
    get_delete_room_handler,
    get_people_list_handler,
    get_return_to_menu_handler,
    get_leave_room_handler,
    get_edit_username_handler,
    get_edit_username_request_handler
)

from .conversations.handlers import (
    get_add_wishes_conversation_handler,
    get_enter_the_room_conversation_handler,
)


def config_application(application: Application) -> None:

    application.add_handler(get_start_handler())
    application.add_handler(get_create_room_handler())
    application.add_handler(get_my_rooms_handler())
    # application.add_handler(get_add_to_room_handler())
    application.add_handler(get_room_choice_handler())
    application.add_handler(get_assign_roles_handler())
    application.add_handler(get_people_list_handler())
    application.add_handler(get_delete_room_handler())
    application.add_handler(get_leave_room_handler())
    application.add_handler(get_return_to_menu_handler())
    # application.add_handler(get_invalid_messages_handler())
    application.add_handler(get_add_wishes_conversation_handler())
    application.add_handler(get_enter_the_room_conversation_handler())
    application.add_handler(get_edit_username_request_handler())


    application.add_handler(get_edit_username_handler())


def run_application() -> None:
    if isinstance(config.TG_TOKEN, str):

        application = ApplicationBuilder().token(config.TG_TOKEN).read_timeout(15).write_timeout(15).build()
        config_application(application)

        application.run_polling()
    else:
        logger.error("Please enter valid Telegram Token in .env file")
