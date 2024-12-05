from dataclasses import dataclass
from typing import Any


class DataTransfer:

    def __init__(self, data: Any = None, valid: bool = True) -> None:
        self.valid = valid
        self.data = data


@dataclass
class GiverReceiverPair:
    giver_chat_id: int
    receiver_chat_id: int
