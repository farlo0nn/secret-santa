import uuid
import random

from .session import db_session
from .models import User, Room, GiftAssignment, Wish
from utils.models import DataTransfer, GiverReceiverPair
from loguru import logger


def create_user(user_id, username):
    with db_session() as db:
        user = db.query(User).filter_by(id=user_id).first()
        if user is None:
            user = User(id=user_id, username=username)
            db.add(user)


def create_room(admin_id):
    with db_session() as db:
        user = db.query(User).filter_by(id=admin_id).first()
        room = Room(code=generate_room_code(), admin_id=user.pk)
        room.users.append(user)
        db.add(room)


def generate_room_code():
    room_code = uuid.uuid4().hex[:8]
    return room_code


def add_to_room(user_id, code):
    with db_session() as db:
        user = db.query(User).filter_by(id=user_id).first()
        room = db.query(Room).filter_by(code=code).first()
        if room not in user.rooms:
            user.rooms.append(room)
        logger.debug(user.rooms)
        return user.username


def get_my_room_codes(id):
    with db_session() as db:
        user = db.query(User).filter_by(id=id).first()
        return [room.code for room in user.rooms]


def is_valid_room_code(string):
    with db_session() as db:
        room = db.query(Room).filter_by(code=string).first()
        if room is None:
            return False
        return True


def get_room_people_list(room_code):
    with db_session() as db:
        if not is_valid_room_code(room_code):
            return None
        room = db.query(Room).filter_by(code=room_code).first()
        return [user.username for user in room.users]


def get_room_admin(room_code):
    with db_session() as db:
        if not is_valid_room_code(room_code):
            return None
        room = db.query(Room).filter_by(code=room_code).first()
        return room.admin.username


def assign_roles(room_code):
    with db_session() as db:
        room = db.query(Room).filter_by(code=room_code).first()

        assignment_for_room_exists = bool(
            db.query(GiftAssignment).filter_by(room_pk=room.pk).count()
        )
        if assignment_for_room_exists:
            return DataTransfer(valid=False)

        participants: list[User] = room.users

        givers = participants[:]

        random.shuffle(givers)
        receivers = givers[1:] + givers[:1]

        assignments = []

        for giver, receiver in zip(givers, receivers):
            assignment = GiftAssignment(
                giver_pk=giver.pk, receiver_pk=receiver.pk, room_pk=room.pk
            )
            assignments.append(assignment)

        db.add_all(assignments)
        # user = db.query(User).filter_by(pk=assignment.giver_pk).first()
        assignments = db.query(GiftAssignment).filter_by(room_pk=room.pk).all()
        giver_receiver_pairs = [
            GiverReceiverPair(assignment.giver.id, assignment.receiver.id)
            for assignment in assignments
        ]
        return DataTransfer(giver_receiver_pairs, True)


def get_user_username(user_id):
    with db_session() as db:
        user = db.query(User).filter_by(id=user_id).first()
        if user is not None:
            return user.username
        return None


def delete_room(room_code):
    with db_session() as db:
        room = db.query(Room).filter_by(code=room_code).first()
        db.delete(room)


def room_exists(room_code):
    with db_session() as db:
        room = db.query(Room).filter_by(code=room_code).first()
        return True if room else False


def add_wish_list(user_id, room_code, wish_list):
    with db_session() as db:
        user = db.query(User).filter_by(id=user_id).first()
        room = db.query(Room).filter_by(code=room_code).first()
        wish_object_list = [
            Wish(content=wish, user_pk=user.pk, room_pk=room.pk) for wish in wish_list
        ]
        db.add_all(wish_object_list)


def get_user_wishes(user_id, room_code):
    with db_session() as db:
        user: User = db.query(User).filter_by(id=user_id).first()
        room: Room = db.query(Room).filter_by(code=room_code).first()
        wish: Wish = 0
        wish_list = [
            wish.content
            for wish in list(filter(lambda wish: wish.room_pk == room.pk, user.wishes))
        ]
        return wish_list or None


def room_exists(room_code):
    with db_session() as db:
        room: Room = db.query(Room).filter_by(code=room_code).first()
        return True if room else False


def room_members_id(room_code):
    with db_session() as db:
        room: Room = db.query(Room).filter_by(code=room_code).first()
        return [user.id for user in room.users]


def user_is_admin(user_id, room_code):
    with db_session() as db:
        user: User = db.query(User).filter_by(id=user_id).first()
        return room_code in [room.code for room in user.created_rooms]
