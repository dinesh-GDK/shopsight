"""Logging configuration for ShopSight."""

import logging
import sys
from app.config import settings


def setup_logger(name: str = "shopsight") -> logging.Logger:
    """
    Configure and return a logger instance.

    Args:
        name: Logger name

    Returns:
        Configured logger instance
    """
    logger = logging.getLogger(name)
    logger.setLevel(getattr(logging, settings.LOG_LEVEL.upper()))

    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(getattr(logging, settings.LOG_LEVEL.upper()))

    # Formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    console_handler.setFormatter(formatter)

    # Add handler if not already added
    if not logger.handlers:
        logger.addHandler(console_handler)

    return logger


# Global logger instance
logger = setup_logger()
