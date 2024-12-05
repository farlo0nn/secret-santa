from sqlalchemy import Column, Table, ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.orm import DeclarativeBase
from .session import get_engine


class Base(DeclarativeBase): ...


class GiftAssignment(Base):
    __tablename__ = "GiftAssignment"

    pk: Mapped[int] = mapped_column(primary_key=True)

    giver_pk = Column(Integer, ForeignKey("User.pk"))
    receiver_pk = Column(Integer, ForeignKey("User.pk"))

    giver = relationship("User", foreign_keys=[giver_pk], back_populates="give_to")
    receiver = relationship(
        "User", foreign_keys=[receiver_pk], back_populates="receive_from"
    )

    room_pk = Column(Integer, ForeignKey("Room.pk"))


user_room = Table(
    "user_room",
    Base.metadata,
    Column("user_pk", Integer, ForeignKey("User.pk")),
    Column("room_pk", Integer, ForeignKey("Room.pk")),
)


class User(Base):
    __tablename__ = "User"

    pk: Mapped[int] = mapped_column(primary_key=True)
    id: Mapped[int] = mapped_column(unique=True)
    username: Mapped[str] = mapped_column(unique=True)

    created_rooms = relationship("Room", backref="admin")
    rooms = relationship("Room", secondary=user_room, back_populates="users")

    give_to = relationship(
        "GiftAssignment", foreign_keys="GiftAssignment.giver_pk", back_populates="giver"
    )
    receive_from = relationship(
        "GiftAssignment",
        foreign_keys="GiftAssignment.receiver_pk",
        back_populates="receiver",
    )

    wishes = relationship("Wish", backref="user")

    def __repr__(self) -> str:
        return f"<User:{self.id}>"


class Room(Base):
    __tablename__ = "Room"

    pk: Mapped[int] = mapped_column(primary_key=True)
    code: Mapped[str] = mapped_column(unique=True)
    admin_id = Column(Integer, ForeignKey("User.pk"))
    users = relationship("User", secondary=user_room, back_populates="rooms")
    assignments = relationship("GiftAssignment", backref="room", cascade="all,delete")
    wishes = relationship("Wish", backref="room")

    def __repr__(self) -> str:
        return f"<Room:{self.code}>"


class Wish(Base):
    __tablename__ = "Wish"

    pk: Mapped[int] = mapped_column(primary_key=True)
    content: Mapped[str] = mapped_column(unique=False)
    user_pk = Column(Integer, ForeignKey("User.pk"))
    room_pk = Column(Integer, ForeignKey("Room.pk"))


def update_models():
    engine = get_engine()
    Base.metadata.create_all(bind=engine)
