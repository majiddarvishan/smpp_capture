import logging
import logging.handlers
import os

# Create logs directory if it doesn't exist
LOG_DIR = "logs"
if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)

# Log file path
LOG_FILE = os.path.join(LOG_DIR, "app.log")

# Define log format
LOG_FORMAT = "%(asctime)s - %(levelname)s - %(name)s - %(message)s"

# Create a logger
logger = logging.getLogger("SMPP_Analyzer")
logger.setLevel(logging.DEBUG)  # Change to INFO in production

# Console handler
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
console_handler.setFormatter(logging.Formatter(LOG_FORMAT))

# File handler (rotating logs)
file_handler = logging.handlers.RotatingFileHandler(
    LOG_FILE, maxBytes=10 * 1024 * 1024, backupCount=5, encoding="utf-8"
)
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(logging.Formatter(LOG_FORMAT))

# Add handlers to logger
logger.addHandler(console_handler)
logger.addHandler(file_handler)


def get_logger(name):
    """Returns a logger instance for a specific module."""
    return logging.getLogger(name)
