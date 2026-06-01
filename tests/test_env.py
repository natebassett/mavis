from app.config.config_manager import ConfigManager

print(
    ConfigManager.get(
        "WAKE_WORD"
    )
)