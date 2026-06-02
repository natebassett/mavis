from dataclasses import dataclass
from datetime import datetime
from typing import Any


@dataclass
class AgentMessage:
    sender: str
    receiver: str
    message_type: str
    payload: Any
    timestamp: datetime = datetime.now()