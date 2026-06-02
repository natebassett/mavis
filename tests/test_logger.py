from app.utils.logger import setup_logger

logger = setup_logger("MAVIS.Test")

logger.info("MAVIS logger test")
logger.warning("MAVIS warning test")
logger.error("MAVIS error test")

print("Logging test complete.")