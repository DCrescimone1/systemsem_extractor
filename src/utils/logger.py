"""
Logging utilities
"""

import logging
import sys
from pathlib import Path
import config

def setup_logger(name: str) -> logging.Logger:
    """Setup logger with consistent formatting"""
    logger = logging.getLogger(name)
    
    # Avoid duplicate handlers
    if logger.handlers:
        return logger
    
    logger.setLevel(getattr(logging, config.LOGGING_CONFIG["level"]))
    
    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    
    # File handler
    config.OUTPUT_DIR.mkdir(exist_ok=True)
    file_handler = logging.FileHandler(config.LOGGING_CONFIG["file"])
    file_handler.setLevel(logging.DEBUG)
    
    # Formatter
    formatter = logging.Formatter(config.LOGGING_CONFIG["format"])
    console_handler.setFormatter(formatter)
    file_handler.setFormatter(formatter)
    
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)
    
    return logger