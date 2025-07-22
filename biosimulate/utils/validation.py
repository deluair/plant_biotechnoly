#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Data validation utilities for the BIOSIMULATE project.

This module provides functions for validating simulation data and parameters.
"""

import logging
from typing import Any, Dict, List, Optional, Union, Tuple
import numpy as np

logger = logging.getLogger(__name__)


def validate_year_range(start_year: int, end_year: int) -> Tuple[bool, str]:
    """Validate the simulation year range.
    
    Args:
        start_year: Starting year of the simulation
        end_year: Ending year of the simulation
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    if not isinstance(start_year, int) or not isinstance(end_year, int):
        return False, "Start and end years must be integers"
    
    if start_year < 2025:
        return False, f"Start year {start_year} is before 2025"
    
    if end_year > 2050:
        return False, f"End year {end_year} is after 2050"
    
    if start_year >= end_year:
        return False, f"Start year {start_year} must be before end year {end_year}"
    
    return True, ""


def validate_probability(value: float, name: str) -> Tuple[bool, str]:
    """Validate that a value is a valid probability (between 0 and 1).
    
    Args:
        value: The probability value to validate
        name: Name of the parameter (for error messages)
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    if not isinstance(value, (int, float)):
        return False, f"{name} must be a number"
    
    if value < 0 or value > 1:
        return False, f"{name} must be between 0 and 1"
    
    return True, ""


def validate_positive(value: Union[int, float], name: str) -> Tuple[bool, str]:
    """Validate that a value is positive.
    
    Args:
        value: The value to validate
        name: Name of the parameter (for error messages)
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    if not isinstance(value, (int, float)):
        return False, f"{name} must be a number"
    
    if value <= 0:
        return False, f"{name} must be positive"
    
    return True, ""


def validate_non_negative(value: Union[int, float], name: str) -> Tuple[bool, str]:
    """Validate that a value is non-negative.
    
    Args:
        value: The value to validate
        name: Name of the parameter (for error messages)
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    if not isinstance(value, (int, float)):
        return False, f"{name} must be a number"
    
    if value < 0:
        return False, f"{name} must be non-negative"
    
    return True, ""


def validate_in_range(value: Union[int, float], min_val: Union[int, float], 
                     max_val: Union[int, float], name: str) -> Tuple[bool, str]:
    """Validate that a value is within a specified range.
    
    Args:
        value: The value to validate
        min_val: Minimum allowed value
        max_val: Maximum allowed value
        name: Name of the parameter (for error messages)
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    if not isinstance(value, (int, float)):
        return False, f"{name} must be a number"
    
    if value < min_val or value > max_val:
        return False, f"{name} must be between {min_val} and {max_val}"
    
    return True, ""


def validate_scenario(scenario: str) -> Tuple[bool, str]:
    """Validate the simulation scenario.
    
    Args:
        scenario: The scenario name
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    valid_scenarios = [
        "baseline", 
        "regulatory_harmonization", 
        "climate_crisis",
        "tech_breakthrough", 
        "market_disruption"
    ]
    
    if scenario not in valid_scenarios:
        return False, f"Scenario '{scenario}' is not valid. Must be one of: {', '.join(valid_scenarios)}"
    
    return True, ""


def validate_distribution_params(dist_type: str, params: Dict[str, Any]) -> Tuple[bool, str]:
    """Validate parameters for a probability distribution.
    
    Args:
        dist_type: Type of distribution (normal, uniform, etc.)
        params: Distribution parameters
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    if dist_type == "normal":
        required_params = ["mean", "std"]
        for param in required_params:
            if param not in params:
                return False, f"Missing required parameter '{param}' for normal distribution"
        
        # Validate standard deviation is positive
        if params["std"] <= 0:
            return False, f"Standard deviation must be positive, got {params['std']}"
            
    elif dist_type == "uniform":
        required_params = ["low", "high"]
        for param in required_params:
            if param not in params:
                return False, f"Missing required parameter '{param}' for uniform distribution"
        
        # Validate low < high
        if params["low"] >= params["high"]:
            return False, f"Low value {params['low']} must be less than high value {params['high']}"
            
    elif dist_type == "triangular":
        required_params = ["left", "mode", "right"]
        for param in required_params:
            if param not in params:
                return False, f"Missing required parameter '{param}' for triangular distribution"
        
        # Validate left <= mode <= right
        if not (params["left"] <= params["mode"] <= params["right"]):
            return False, f"Must have left <= mode <= right for triangular distribution"
            
    elif dist_type == "beta":
        required_params = ["alpha", "beta"]
        for param in required_params:
            if param not in params:
                return False, f"Missing required parameter '{param}' for beta distribution"
        
        # Validate alpha and beta are positive
        if params["alpha"] <= 0 or params["beta"] <= 0:
            return False, f"Alpha and beta must be positive for beta distribution"
            
    else:
        return False, f"Unknown distribution type: {dist_type}"
    
    return True, ""