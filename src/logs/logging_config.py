import os
from loguru import logger
from datetime import datetime

ROOT_DIR = os.getcwd()

current_date = datetime.now().strftime("%Y-%m-%d")
log_filename = f"app-{current_date}.log"
logs_file_path = os.path.join(ROOT_DIR, "src", "logs", log_filename)

app_log_config = {
    "sink": logs_file_path,
    "format": "{time:YYYY-MM-DD HH:mm} UTC - {level} - {name}:{function}:{line} - {message}",
    "level": "DEBUG",
    "rotation": "100 MB",
    "enqueue": True,
    "catch": True,
}

server_log_config = {
    "sink": logs_file_path,
    "format": "{time:YYYY-MM-DD HH:mm} UTC - {level} - {name}:{function}:{line} - {message}",
    "level": "INFO",
    "rotation": "50 MB",
    "enqueue": True,
    "catch": True
}

logger = logger.bind()
logger.add(**app_log_config)

# Example usage of the logger
logger.debug("This is a debug message.")
logger.info("This is an info message.")
logger.error("This is an error message.")