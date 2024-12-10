from telegram import Message
from telegram.ext._utils.types import FilterDataDict
from telegram.ext.filters import MessageFilter
from db.services import is_valid_room_code
from static_data import messages as static

from loguru import logger


class CreateRoomFilter(MessageFilter):
    def filter(self, message):
        return message.text == static.create_new_room_option


class MyRoomsFilter(MessageFilter):
    def filter(self, message):
        return message.text == static.my_rooms_option


class ValidRoomCodeFilter(MessageFilter):
    def filter(self, message):
        return is_valid_room_code(message.text)


class AssignRolesFilter(MessageFilter):
    def filter(self, message):
        return message.text == static.assign_roles_option


class PeopleListMessageFilter(MessageFilter):
    def filter(self, message):
        return message.text == static.people_list_option


class DeleteRoomMessageFilter(MessageFilter):
    def filter(self, message):
        return message.text == static.delete_room_option


class ReturnToMenuMessageFilter(MessageFilter):
    def filter(self, message):
        return message.text == static.return_to_menu_option

class LeaveRoomFilter(MessageFilter):
    def filter(self, message):
        return message.text == static.leave_room_option


class EditUsernameRequestFilter(MessageFilter):
    def filter(self, message): 
        return message.text == static.edit_username_option