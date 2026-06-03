from app.core.background_service import BackgroundService


def main():
    """
    Main entry point for MAVIS.
    """

    mavis = BackgroundService()
    mavis.start()


if __name__ == "__main__":
    main()