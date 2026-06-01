from app.intent.intent_router import IntentRouter
from app.intent.intent_types import IntentType


router = IntentRouter()

test_inputs = [
    "hello",
    "remember that I like spicy food",
    "what do you remember about me?",
    "system status",
    "what can you do?",
    "random sentence here",
]

for text in test_inputs:
    result = router.route(text)

    print(f"Input: {text}")
    print(f"Intent: {result['intent'].value}")
    print(f"Confidence: {result['confidence']}")
    print("-" * 30)