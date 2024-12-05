from telegram.ext import filters

from telegram.ext import CommandHandler, CallbackQueryHandler
from telegram.ext import MessageHandler
from telegram.ext import ConversationHandler


from ..filters import AddWishFilter, EnterTheRoomFilter

from .services import (
    ADD_WISH,
    add_wish_start_conversation,
    add_wish,
    submit_wishes,
    ENTER_THE_ROOM,
    enter_the_room_start_conversation,
    enter_the_room,
    cancel_entering_the_room,
)

from .callbacks import (
    submit_wishes_callback,
    cancel_entering_the_room_callback
)


def get_add_wishes_conversation_handler():

    conv_handler = ConversationHandler(
        entry_points=[MessageHandler(AddWishFilter(), add_wish_start_conversation)],
        states={
            ADD_WISH: [
                # CallbackQueryHandler(submit_wishes_callback, pattern='^submit'),
                MessageHandler(filters.TEXT, add_wish),
            ],
        },
        fallbacks=[CallbackQueryHandler(submit_wishes_callback, pattern='^submit')]
    )
    return conv_handler


def get_enter_the_room_conversation_handler():

    conv_handler = ConversationHandler(
        entry_points=[
            MessageHandler(EnterTheRoomFilter(), enter_the_room_start_conversation)
        ],
        states={
            ENTER_THE_ROOM: [
                MessageHandler(filters.TEXT, enter_the_room),
            ],
        },
        fallbacks=[CallbackQueryHandler(cancel_entering_the_room_callback, pattern='^cancel')],
    )
    return conv_handler
