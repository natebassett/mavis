from app.intent.intent_types import IntentType


class IntentRouter:
    def __init__(self):
        self.intent_keywords = {
            IntentType.RECALL: [
                "what do you remember",
                "what do you know about me",
                "recall",
                "what have you stored",
                "memory",
            ],
            IntentType.REMEMBER: [
                "remember that",
                "remember",
                "note that",
                "save this",
                "store this",
            ],
            IntentType.GREETING: [
                "hello",
                "hi",
                "hey",
                "good morning",
                "good afternoon",
                "good evening",
            ],
            IntentType.GOODBYE: [
                "bye",
                "goodbye",
                "exit",
                "quit",
                "see you",
            ],
            IntentType.HELP: [
                "help",
                "what can you do",
                "commands",
                "options",
            ],
            IntentType.STATUS: [
                "status",
                "system status",
                "are you online",
                "diagnostics",
            ],
        }

    def route(self, user_input: str):
        cleaned_input = user_input.lower().strip()

        for intent_type, keywords in self.intent_keywords.items():
            for keyword in keywords:
                if keyword in cleaned_input:
                    return {
                        "intent": intent_type,
                        "confidence": 1.0,
                        "original_input": user_input,
                    }

        return {
            "intent": IntentType.UNKNOWN,
            "confidence": 0.0,
            "original_input": user_input,
        }