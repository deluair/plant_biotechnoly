#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Logging configuration for the BIOSIMULATE project.

This module provides functions for setting up logging for the simulation.
"""

import os
import logging
from datetime import datetime
from typing import Optional


def setup_logging(level: int = logging.INFO, log_file: Optional[str] = None) -> None:
    """Set up logging for the simulation.
    
    Args:
        level: Logging level (default: INFO)
        log_file: Path to log file (default: None, logs to console only)
    """
    # Create logs directory if it doesn't exist and log_file is specified
    if log_file is not None:
        log_dir = os.path.dirname(log_file)
        if log_dir and not os.path.exists(log_dir):
            os.makedirs(log_dir)
    else:
        # Default log file in logs directory with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        log_dir = "./logs"
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)
        log_file = os.path.join(log_dir, f"biosimulate_{timestamp}.log")
    
    # Configure root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(level)
    
    # Remove existing handlers
    for handler in root_logger.handlers[:]:  # Make a copy of the list
        root_logger.removeHandler(handler)
    
    # Create console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(level)
    console_format = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    console_handler.setFormatter(console_format)
    root_logger.addHandler(console_handler)
    
    # Create file handler
    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(level)
    file_format = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    file_handler.setFormatter(file_format)
    root_logger.addHandler(file_handler)
    
    # Log initial message
    root_logger.info(f"Logging initialized at level {logging.getLevelName(level)}")
    root_logger.info(f"Log file: {os.path.abspath(log_file)}")