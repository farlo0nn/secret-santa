from telegram import Update, CallbackQuery
from telegram.ext import ContextTypes
from .services import submit_wishes, cancel_entering_the_room

from loguru import logger 

async def submit_wishes_callback(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> None:
    
    query: CallbackQuery = update.callback_query 

    await query.answer()
    logger.debug(query.data)
    if query.data == "submit":
        wish_list = context.user_data["wish_list"]
        await query.edit_message_text(f"Your wishes in this room:\n{", ".join(wish_list)}")
        
        return await submit_wishes(update.effective_chat.id, context) 


async def cancel_entering_the_room_callback(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> None:
    
    query: CallbackQuery = update.callback_query 

    await query.answer()
    
    if query.data == "cancel":
        
        await query.delete_message()
        
        return await cancel_entering_the_room(update.effective_chat.id, context)