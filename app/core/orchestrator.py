from app.utils.logger import setup_logger


class Orchestrator:
    def __init__(self):
        self.logger = setup_logger("MAVIS.Orchestrator")

    def process(self, user_input: str) -> str:
        cleaned_input = user_input.strip()

        self.logger.info(f"Received input: {cleaned_input}")

        if not cleaned_input:
            return "I didn't catch that."

        return f"You said: {cleaned_input}"