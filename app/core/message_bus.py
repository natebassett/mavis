from app.core.agent_message import AgentMessage
from app.utils.logger import setup_logger


class MessageBus:
    def __init__(self):
        self.logger = setup_logger("MAVIS.MessageBus")
        self.messages = []

    def send(self, message: AgentMessage):
        self.messages.append(message)

        self.logger.info(
            f"Message sent from {message.sender} to {message.receiver} "
            f"with type {message.message_type}"
        )

        return message

    def get_messages(self):
        return self.messages

    def get_messages_for(self, receiver: str):
        return [
            message for message in self.messages
            if message.receiver == receiver
        ]