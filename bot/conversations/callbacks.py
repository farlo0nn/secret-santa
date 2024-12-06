from telegram import Update, CallbackQuery
from telegram.ext import ContextTypes
from .services import submit_wishes, cancel_entering_the_room

from loguru import logger 

async def submit_wishes_callback(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> None:
    
    query: CallbackQuery = update.callback_query 

    return await submit_wishes(update,context,query)


async def cancel_entering_the_room_callback(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> None:
    
    query: CallbackQuery = update.callback_query 

    await query.answer()
    
    if query.data == "cancel":
        
        await query.delete_message()
        
        return await cancel_entering_the_room(update.effective_chat.id, context)