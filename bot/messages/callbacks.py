from telegram import Update, CallbackQuery
from telegram.ext import ContextTypes
from telegram.ext import CallbackContext
from loguru import logger

from .services import (
    send_invalid_message,
    start,
    create_room,
    my_rooms,
    room_choice,
    assign_roles,
    delete_room,
    people_list,
    return_to_menu,
    leave_room,
    create_user
)
from ..validators import room_context_validator


async def invalid_message_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await send_invalid_message(update.effective_chat.id, context)


async def start_callback(update: Update, context: CallbackContext):
    
    context.user_data["username_enter_expected"] = True 

    await start(update.effective_chat.id, update.effective_chat.username, context)


async def username_enter_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if context.user_data["username_enter_expected"]:

        username = update.effective_chat.username 
        if username is None:
            if update.effective_chat.first_name is not None:
                username = update.effective_chat.first_name + " " + update.effective_chat.last_name
            else:
                username = update.effective_chat.effective_name

        if update.message.text != "-":
            username = update.message.text
            
        await create_user(update.effective_chat.id, username, context)
            
            


async def create_room_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await create_room(update.effective_chat.id, context)



async def my_rooms_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await my_rooms(update.effective_chat.id, context)


async def room_choice_callback( update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query: CallbackQuery = update.callback_query  
    await query.answer()
    room_code = query.data.split("_")[1]
    context.user_data["room_code"] = room_code
    await query.delete_message()
    await room_choice(update.effective_chat.id, context)


@room_context_validator
async def assign_roles_callback(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> None:
    await assign_roles(update.effective_chat.id, context)


@room_context_validator
async def people_list_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await people_list(update.effective_chat.id, context)


@room_context_validator
async def delete_room_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await delete_room(update.effective_chat.id, context)


async def return_to_menu_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await return_to_menu(update.effective_chat.id, context)

@room_context_validator
async def leave_room_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await leave_room(update.effective_chat.id, context)
