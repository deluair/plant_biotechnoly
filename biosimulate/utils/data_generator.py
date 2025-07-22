#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Data generation utilities for the BIOSIMULATE project.

This module provides functions for generating synthetic data for the simulation.
"""

import logging
import numpy as np
from typing import Dict, List, Tuple, Union, Any, Optional

logger = logging.getLogger(__name__)


def generate_normal(mean: float, std: float, size: int = 1, 
                   min_val: Optional[float] = None, 
                   max_val: Optional[float] = None) -> Union[float, np.ndarray]:
    """Generate values from a normal distribution with optional truncation.
    
    Args:
        mean: Mean of the distribution
        std: Standard deviation of the distribution
        size: Number of samples to generate
        min_val: Minimum allowed value (default: None)
        max_val: Maximum allowed value (default: None)
        
    Returns:
        Single value or array of generated values
    """
    values = np.random.normal(mean, std, size)
    
    if min_val is not None:
        values = np.maximum(values, min_val)
    
    if max_val is not None:
        values = np.minimum(values, max_val)
    
    if size == 1:
        return float(values[0])
    return values


def generate_normal_distribution(mean: float, std: float, size: int = 1, 
                                min_val: Optional[float] = None, 
                                max_val: Optional[float] = None) -> np.ndarray:
    """Generate values from a normal distribution with optional truncation.
    
    Args:
        mean: Mean of the distribution
        std: Standard deviation of the distribution
        size: Number of samples to generate
        min_val: Minimum allowed value (default: None)
        max_val: Maximum allowed value (default: None)
        
    Returns:
        Array of generated values
    """
    values = np.random.normal(mean, std, size)
    
    if min_val is not None:
        values = np.maximum(values, min_val)
    
    if max_val is not None:
        values = np.minimum(values, max_val)
    
    return values


def generate_triangular(low: float, mode: float, high: float, size: int = 1) -> Union[float, np.ndarray]:
    """Generate values from a triangular distribution.
    
    Args:
        low: Lower bound of the distribution
        mode: Mode of the distribution
        high: Upper bound of the distribution
        size: Number of samples to generate
        
    Returns:
        Single value or array of generated values
    """
    values = np.random.triangular(low, mode, high, size)
    
    if size == 1:
        return float(values[0])
    return values


def generate_beta(alpha: float, beta: float, size: int = 1, 
                 min_val: Optional[float] = 0.0, 
                 max_val: Optional[float] = 1.0) -> Union[float, np.ndarray]:
    """Generate values from a beta distribution with optional scaling.
    
    Args:
        alpha: Alpha parameter of the beta distribution
        beta: Beta parameter of the beta distribution
        size: Number of samples to generate
        min_val: Minimum value for scaling (default: 0.0)
        max_val: Maximum value for scaling (default: 1.0)
        
    Returns:
        Single value or array of generated values
    """
    values = np.random.beta(alpha, beta, size)
    
    # Scale from [0, 1] to [min_val, max_val] if needed
    if min_val != 0.0 or max_val != 1.0:
        values = min_val + (max_val - min_val) * values
    
    if size == 1:
        return float(values[0])
    return values


def generate_uniform_distribution(low: float, high: float, size: int = 1) -> np.ndarray:
    """Generate values from a uniform distribution.
    
    Args:
        low: Lower bound of the distribution
        high: Upper bound of the distribution
        size: Number of samples to generate
        
    Returns:
        Array of generated values
    """
    return np.random.uniform(low, high, size)


def generate_triangular_distribution(left: float, mode: float, right: float, size: int = 1) -> np.ndarray:
    """Generate values from a triangular distribution.
    
    Args:
        left: Lower bound of the distribution
        mode: Mode of the distribution
        right: Upper bound of the distribution
        size: Number of samples to generate
        
    Returns:
        Array of generated values
    """
    return np.random.triangular(left, mode, right, size)


def generate_beta_distribution(alpha: float, beta: float, size: int = 1, 
                              scale: float = 1.0, shift: float = 0.0) -> np.ndarray:
    """Generate values from a beta distribution with optional scaling and shifting.
    
    Args:
        alpha: Alpha parameter of the beta distribution
        beta: Beta parameter of the beta distribution
        size: Number of samples to generate
        scale: Scale factor to apply to the generated values
        shift: Shift to apply to the generated values
        
    Returns:
        Array of generated values
    """
    values = np.random.beta(alpha, beta, size)
    return values * scale + shift


def generate_poisson_distribution(lam: float, size: int = 1) -> np.ndarray:
    """Generate values from a Poisson distribution.
    
    Args:
        lam: Rate parameter of the Poisson distribution
        size: Number of samples to generate
        
    Returns:
        Array of generated values
    """
    return np.random.poisson(lam, size)


def generate_exponential_distribution(scale: float, size: int = 1) -> np.ndarray:
    """Generate values from an exponential distribution.
    
    Args:
        scale: Scale parameter of the exponential distribution
        size: Number of samples to generate
        
    Returns:
        Array of generated values
    """
    return np.random.exponential(scale, size)


def generate_growth_curve(initial_value: float, growth_rate: float, years: int, 
                         noise_level: float = 0.0, saturation_level: Optional[float] = None) -> np.ndarray:
    """Generate a growth curve with optional noise and saturation.
    
    Args:
        initial_value: Starting value
        growth_rate: Annual growth rate (as a decimal, e.g., 0.05 for 5%)
        years: Number of years to generate
        noise_level: Standard deviation of noise to add (default: 0.0)
        saturation_level: Maximum value for saturation (default: None)
        
    Returns:
        Array of values representing the growth curve
    """
    values = np.zeros(years)
    values[0] = initial_value
    
    for i in range(1, years):
        # Calculate growth with compound interest formula
        values[i] = values[i-1] * (1 + growth_rate)
        
        # Add noise if specified
        if noise_level > 0:
            values[i] += np.random.normal(0, noise_level * values[i])
        
        # Apply saturation if specified
        if saturation_level is not None and values[i] > saturation_level:
            values[i] = saturation_level
    
    return values


def generate_s_curve(initial_value: float, max_value: float, midpoint: float, 
                    steepness: float, years: int, noise_level: float = 0.0) -> np.ndarray:
    """Generate an S-curve (logistic growth) with optional noise.
    
    Args:
        initial_value: Starting value
        max_value: Maximum value (asymptote)
        midpoint: Year at which the curve reaches 50% of max_value
        steepness: Steepness of the curve
        years: Number of years to generate
        noise_level: Standard deviation of noise to add (default: 0.0)
        
    Returns:
        Array of values representing the S-curve
    """
    x = np.arange(years)
    values = initial_value + (max_value - initial_value) / (1 + np.exp(-steepness * (x - midpoint)))
    
    # Add noise if specified
    if noise_level > 0:
        values += np.random.normal(0, noise_level * max_value, years)
        # Ensure values stay within bounds
        values = np.maximum(values, initial_value)
        values = np.minimum(values, max_value)
    
    return values


def generate_cyclic_trend(base_value: float, amplitude: float, period: float, 
                         years: int, growth_rate: float = 0.0, 
                         noise_level: float = 0.0) -> np.ndarray:
    """Generate a cyclic trend with optional growth and noise.
    
    Args:
        base_value: Base value around which the cycle oscillates
        amplitude: Amplitude of the cycle
        period: Period of the cycle in years
        years: Number of years to generate
        growth_rate: Annual growth rate of the base value (default: 0.0)
        noise_level: Standard deviation of noise to add (default: 0.0)
        
    Returns:
        Array of values representing the cyclic trend
    """
    x = np.arange(years)
    
    # Calculate base values with growth
    if growth_rate == 0:
        base_values = np.ones(years) * base_value
    else:
        base_values = base_value * np.power(1 + growth_rate, x)
    
    # Add cyclic component
    values = base_values + amplitude * np.sin(2 * np.pi * x / period)
    
    # Add noise if specified
    if noise_level > 0:
        values += np.random.normal(0, noise_level * base_value, years)
    
    return values


def generate_market_adoption_curve(max_adoption: float, start_year: int, 
                                 adoption_rate: float, years: int, 
                                 noise_level: float = 0.0) -> np.ndarray:
    """Generate a market adoption curve using a modified Bass diffusion model.
    
    Args:
        max_adoption: Maximum adoption level (market saturation)
        start_year: Year when the technology is introduced (0-indexed)
        adoption_rate: Rate of adoption
        years: Number of years to generate
        noise_level: Standard deviation of noise to add (default: 0.0)
        
    Returns:
        Array of values representing the adoption curve
    """
    values = np.zeros(years)
    
    # No adoption before start_year
    for i in range(start_year, years):
        t = i - start_year + 1  # Time since introduction
        # Modified Bass diffusion model
        values[i] = max_adoption * (1 - np.exp(-adoption_rate * t)) / (1 + np.exp(-adoption_rate * (t - 5)))
        
        # Add noise if specified
        if noise_level > 0:
            values[i] += np.random.normal(0, noise_level * max_adoption)
            values[i] = max(0, values[i])  # Ensure non-negative
            values[i] = min(max_adoption, values[i])  # Ensure below max
    
    return values


def generate_regional_variation(base_values: np.ndarray, 
                               region_factors: Dict[str, float]) -> Dict[str, np.ndarray]:
    """Generate regional variations based on base values and region-specific factors.
    
    Args:
        base_values: Base values to apply regional factors to
        region_factors: Dictionary mapping region names to multiplier factors
        
    Returns:
        Dictionary mapping region names to arrays of values
    """
    regional_values = {}
    
    for region, factor in region_factors.items():
        regional_values[region] = base_values * factor
    
    return regional_values


def generate_technology_success_rates(base_rate: float, 
                                    technology_factors: Dict[str, float]) -> Dict[str, float]:
    """Generate technology-specific success rates.
    
    Args:
        base_rate: Base success rate
        technology_factors: Dictionary mapping technology names to relative factors
        
    Returns:
        Dictionary mapping technology names to success rates
    """
    success_rates = {}
    
    for tech, factor in technology_factors.items():
        # Apply factor and ensure rate is between 0 and 1
        rate = base_rate * factor
        success_rates[tech] = max(0, min(1, rate))
    
    return success_rates


def generate_correlated_time_series(base_series: np.ndarray, 
                                  correlation: float, 
                                  noise_level: float) -> np.ndarray:
    """Generate a time series correlated with a base series.
    
    Args:
        base_series: Base time series to correlate with
        correlation: Correlation coefficient (-1 to 1)
        noise_level: Standard deviation of noise to add
        
    Returns:
        Array of values representing the correlated time series
    """
    # Generate random noise
    noise = np.random.normal(0, noise_level, len(base_series))
    
    # Normalize base series
    base_norm = (base_series - np.mean(base_series)) / np.std(base_series)
    
    # Create correlated series
    correlated = correlation * base_norm + np.sqrt(1 - correlation**2) * noise
    
    # Scale back to original scale
    result = correlated * np.std(base_series) + np.mean(base_series)
    
    return result