import logging
from logging.handlers import RotatingFileHandler
import os

def setup_logging(log_file='app.log'):
    # Ensure log directory exists
    LOG_DIR = "logs"
    os.makedirs(LOG_DIR, exist_ok=True)

    # Configure loggers
    formatter = logging.Formatter(
        "%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )

    # Console logger (StreamHandler logs to stdout for Docker)
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    # Rotating file logger
    file_handler = RotatingFileHandler(
        os.path.join(LOG_DIR, log_file), maxBytes=1_000_000, backupCount=5
    )
    file_handler.setFormatter(formatter)
    
    # Assign handlers to Flask's logger
    logger = logging.getLogger()
    #logger.setLevel(logging.INFO)

    #log level config
    log_level = os.getenv("LOG_LEVEL", "INFO").upper()
    logger.setLevel(getattr(logging, log_level, logging.INFO))
    
    if not logger.handlers:
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)