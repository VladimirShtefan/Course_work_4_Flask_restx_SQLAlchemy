import logging

from app.constants import DEBUG_LOG_PATH, ERROR_LOG_PATH


def create_logger(name: str) -> logging.Logger:
    file_formatter = logging.Formatter('%(asctime)s - %(name)s [%(levelname)s] %(message)s')

    file_debug_handler = logging.FileHandler(DEBUG_LOG_PATH)
    file_error_handler = logging.FileHandler(ERROR_LOG_PATH)

    file_debug_handler.setLevel(logging.DEBUG)
    file_error_handler.setLevel(logging.ERROR)

    file_debug_handler.setFormatter(file_formatter)
    file_error_handler.setFormatter(file_formatter)

    logger = logging.getLogger(name)

    logger.addHandler(file_debug_handler)
    logger.addHandler(file_error_handler)
    logger.setLevel(logging.DEBUG)

    return logger
