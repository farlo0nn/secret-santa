from telegram.ext.filters import MessageFilter
from static_data import messages as static
from loguru import logger 


class AddWishFilter(MessageFilter):
    def filter(self, message):
        return message.text == static.add_wish_option


class EnterTheRoomFilter(MessageFilter):
    def filter(self, message):
        return message.text == static.enter_the_room_option
