from app.core.orchestrator import Orchestrator


def main():
    mavis = Orchestrator()

    print("MAVIS online. Type 'exit' to shut down.")

    while True:
        user_input = input("You: ")

        if user_input.lower().strip() in ["exit", "quit"]:
            print("MAVIS shutting down.")
            break

        response = mavis.process(user_input)
        print(f"MAVIS: {response}")


if __name__ == "__main__":
    main()