from dataclasses import dataclass, field
from typing import Any, List 


class DataTransfer:

    def __init__(self, data: Any = None, valid: bool = True) -> None:
        self.valid = valid
        self.data = data


@dataclass
class GiverReceiverIdsPair:
    giver_chat_id: int
    receiver_chat_id: int

    def __str__(self) -> str:
        return f"giver id: {self.giver_chat_id}, receiver id: {self.receiver_chat_id}"


@dataclass
class GiverReceiverPair:
    giver_username: str 
    giver_id: int 
    
    receiver_username: str
    receiver_id: int

    def __str__(self) -> str:
        return f"{self.giver_username} -> {self.receiver_username}" 
    
@dataclass
class DbStatus:
    connection: bool = False 
    models_synced: bool = False 
    missing_tables: List[str] = field(default_factory=list)
    error: str = None 

    def valid(self):
        if self.connection and len(self.missing_tables) == 0:
            return True 
        return False 

    def __str__(self):
        return f"Connection to db is {'valid' if self.valid() else 'invalid'}"
        
