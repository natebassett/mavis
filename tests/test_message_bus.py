from app.core.agent_message import AgentMessage
from app.core.message_bus import MessageBus


bus = MessageBus()

message = AgentMessage(
    sender="Orchestrator",
    receiver="IntentAgent",
    message_type="USER_INPUT",
    payload={
        "text": "hello mavis"
    }
)

bus.send(message)

print("All messages:")
print(bus.get_messages())

print("Messages for IntentAgent:")
print(bus.get_messages_for("IntentAgent"))