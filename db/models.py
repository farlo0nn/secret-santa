from sqlalchemy import Column, Table, ForeignKey, Integer, String, BigInteger
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.orm import DeclarativeBase
from .session import get_engine


class Base(DeclarativeBase): ...

user_room = Table(
    "user_room",
    Base.metadata,
    Column("user_id", BigInteger, ForeignKey("User.id")),
    Column("room_code", String(8), ForeignKey("Room.code")),
)

class User(Base):
    __tablename__ = "User"

    pk: Mapped[int] = mapped_column(primary_key=True)
    id = Column(BigInteger, unique=True)
    
    username = Column(String(255), unique=False, nullable=True)

    created_rooms = relationship("Room", backref="admin", cascade="all,delete")
    rooms = relationship("Room", secondary=user_room, back_populates="users")

    give_to = relationship(
        "GiftAssignment", 
        foreign_keys="GiftAssignment.giver_id", 
        back_populates="giver"
    )
    receive_from = relationship(
        "GiftAssignment",
        foreign_keys="GiftAssignment.receiver_id",
        back_populates="receiver",
    )

    wishes = relationship("Wish", backref="user")

    def __repr__(self) -> str:
        return f"<User:{self.id}>"


class Room(Base):
    __tablename__ = "Room"

    pk: Mapped[int] = mapped_column(primary_key=True)
    code = Column(String(8), unique=True)
    admin_id = Column(BigInteger, ForeignKey("User.id"))
    users = relationship("User", secondary=user_room, back_populates="rooms")
    assignments = relationship("GiftAssignment", backref="room", cascade="all,delete")
    wishes = relationship("Wish", backref="room", cascade="all,delete")

    def __repr__(self) -> str:
        return f"<Room:{self.code}>"
    

class GiftAssignment(Base):
    __tablename__ = "GiftAssignment"

    pk: Mapped[int] = mapped_column(primary_key=True)

    giver_id = Column(BigInteger, ForeignKey("User.id"))
    receiver_id = Column(BigInteger, ForeignKey("User.id"))

    giver = relationship("User", foreign_keys=[giver_id], back_populates="give_to")
    receiver = relationship(
        "User", foreign_keys=[receiver_id], back_populates="receive_from"
    )

    room_code = Column(String(8), ForeignKey("Room.code"))


class Wish(Base):
    __tablename__ = "Wish"

    pk: Mapped[int] = mapped_column(primary_key=True)
    content = Column(String(255), unique=False)
    user_id = Column(BigInteger, ForeignKey("User.id"))
    room_code = Column(String(8), ForeignKey("Room.code"))


def update_models():
    engine = get_engine()
    Base.metadata.create_all(bind=engine)
