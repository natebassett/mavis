import logging
import os

from app.config.config_manager import ConfigManager


def setup_logger(name: str = "MAVIS"):
    os.makedirs("logs", exist_ok=True)

    logger = logging.getLogger(name)

    if logger.handlers:
        return logger

    log_level = ConfigManager.get("LOG_LEVEL", "INFO").upper()
    logger.setLevel(getattr(logging, log_level, logging.INFO))

    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
    )

    file_handler = logging.FileHandler("logs/mavis.log")
    file_handler.setFormatter(formatter)

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger