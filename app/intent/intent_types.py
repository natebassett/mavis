from enum import Enum


class IntentType(Enum):
    GREETING = "greeting"
    GOODBYE = "goodbye"
    HELP = "help"
    REMEMBER = "remember"
    RECALL = "recall"
    STATUS = "status"
    UNKNOWN = "unknown"