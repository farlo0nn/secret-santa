from telegram.ext import CommandHandler
from telegram.ext import MessageHandler, CallbackQueryHandler


from .filters import (
    CreateRoomFilter,
    MyRoomsFilter,
    AssignRolesFilter,
    PeopleListMessageFilter,
    DeleteRoomMessageFilter,
    ReturnToMenuMessageFilter,
    LeaveRoomFilter
)

from .callbacks import (
    start_callback,
    invalid_message_callback,
    create_room_callback,
    my_rooms_callback,
    # add_to_room_callback,
    room_choice_callback,
    assign_roles_callback,
    people_list_callback,
    delete_room_callback,
    return_to_menu_callback,
    leave_room_callback
)


def get_start_handler():
    return CommandHandler(command="start", callback=start_callback)

def get_create_room_handler():
    return MessageHandler(CreateRoomFilter(), callback=create_room_callback)


def get_my_rooms_handler():
    return MessageHandler(MyRoomsFilter(), callback=my_rooms_callback)


def get_room_choice_handler():
    return CallbackQueryHandler(room_choice_callback, pattern='^rc_')


def get_assign_roles_handler():
    return MessageHandler(AssignRolesFilter(), callback=assign_roles_callback)


def get_people_list_handler():
    return MessageHandler(PeopleListMessageFilter(), callback=people_list_callback)


def get_delete_room_handler():
    return MessageHandler(DeleteRoomMessageFilter(), callback=delete_room_callback)


def get_return_to_menu_handler():
    return MessageHandler(ReturnToMenuMessageFilter(), callback=return_to_menu_callback)

def get_leave_room_handler():
    return MessageHandler(LeaveRoomFilter(), callback=leave_room_callback)
