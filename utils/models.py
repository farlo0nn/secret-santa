from dataclasses import dataclass
from typing import Any


class DataTransfer:

    def __init__(self, data: Any = None, valid: bool = True) -> None:
        self.valid = valid
        self.data = data


@dataclass
class GiverReceiverIdsPair:
    giver_chat_id: int
    receiver_chat_id: int

    def __repr__(self) -> str:
        return f"giver id: {self.giver_chat_id}, receiver id: {self.receiver_chat_id}"


@dataclass
class GiverReceiverPair:
    giver_username: str 
    giver_id: int 
    
    receiver_username: str
    receiver_id: int

    def __repr__(self) -> str:
        return f"{self.giver_username} -> {self.receiver_username}" 