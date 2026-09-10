from app.core.orchestrator import Orchestrator
from app.utils.logger import setup_logger


class BackgroundService:
    """
    Core runtime loop for MAVIS.

    This service keeps MAVIS running continuously and passes user
    commands into the main orchestrator.
    """

    def __init__(self):
        """
        Initialises the background service and MAVIS orchestrator.
        """

        self.logger = setup_logger("MAVIS.BackgroundService")
        self.orchestrator = Orchestrator()
        self.running = False

    def start(self):
        """
        Starts the MAVIS runtime loop.
        """

        self.running = True

        self.logger.info("MAVIS background service started.")

        print("\nMAVIS online.")
        print("Type 'exit', 'quit', or 'shutdown' to stop MAVIS.\n")

        while self.running:
            try:
                # Wait for user input
                user_input = input("You: ").strip()

                if not user_input:
                    continue

                # Stop MAVIS safely
                if user_input.lower() in ["exit", "quit", "shutdown"]:
                    self.stop()
                    break

                response = self.orchestrator.process(user_input)

                print(f"MAVIS: {response}")

            except KeyboardInterrupt:
                # Handle CTRL+C safely
                self.logger.info("Keyboard interrupt received.")
                self.stop()
                break

            except Exception as error:
                self.logger.error(f"Runtime error: {error}")
                print(f"MAVIS Error: {error}")

    def stop(self):
        """
        Stops the MAVIS runtime loop.
        """

        self.running = False

        self.logger.info("MAVIS background service stopped.")

        print("\nMAVIS shutting down.")