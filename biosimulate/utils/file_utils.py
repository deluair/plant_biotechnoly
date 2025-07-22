#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""File utility functions for the BIOSIMULATE project.

This module provides functions for file operations used throughout the simulation.
"""

import os
import json
import csv
import logging
import pandas as pd
from typing import Dict, List, Any, Optional, Union

logger = logging.getLogger(__name__)


def ensure_directory_exists(directory_path: str) -> None:
    """Ensure that a directory exists, creating it if necessary.
    
    Args:
        directory_path: Path to the directory
    """
    if not os.path.exists(directory_path):
        os.makedirs(directory_path)
        logger.info(f"Created directory: {directory_path}")


def save_json(data: Dict[str, Any], file_path: str, pretty: bool = True) -> None:
    """Save data to a JSON file.
    
    Args:
        data: Data to save
        file_path: Path to the output file
        pretty: Whether to format the JSON with indentation (default: True)
    """
    # Ensure the directory exists
    directory = os.path.dirname(file_path)
    if directory:
        ensure_directory_exists(directory)
    
    # Save the data
    with open(file_path, 'w') as f:
        if pretty:
            json.dump(data, f, indent=2)
        else:
            json.dump(data, f)
    
    logger.debug(f"Saved JSON data to {file_path}")


def load_json(file_path: str) -> Dict[str, Any]:
    """Load data from a JSON file.
    
    Args:
        file_path: Path to the input file
        
    Returns:
        Loaded data
        
    Raises:
        FileNotFoundError: If the file does not exist
        json.JSONDecodeError: If the file is not valid JSON
    """
    with open(file_path, 'r') as f:
        data = json.load(f)
    
    logger.debug(f"Loaded JSON data from {file_path}")
    return data


def save_csv(data: List[Dict[str, Any]], file_path: str, fieldnames: Optional[List[str]] = None) -> None:
    """Save data to a CSV file.
    
    Args:
        data: List of dictionaries to save
        file_path: Path to the output file
        fieldnames: List of field names (default: None, uses keys from first dictionary)
    """
    # Ensure the directory exists
    directory = os.path.dirname(file_path)
    if directory:
        ensure_directory_exists(directory)
    
    # Determine fieldnames if not provided
    if fieldnames is None and data:
        fieldnames = list(data[0].keys())
    
    # Save the data
    with open(file_path, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)
    
    logger.debug(f"Saved CSV data to {file_path}")


def load_csv(file_path: str) -> List[Dict[str, Any]]:
    """Load data from a CSV file.
    
    Args:
        file_path: Path to the input file
        
    Returns:
        List of dictionaries with the loaded data
        
    Raises:
        FileNotFoundError: If the file does not exist
    """
    with open(file_path, 'r', newline='') as f:
        reader = csv.DictReader(f)
        data = list(reader)
    
    logger.debug(f"Loaded CSV data from {file_path}")
    return data


def save_dataframe(df: pd.DataFrame, file_path: str, format: str = 'csv') -> None:
    """Save a pandas DataFrame to a file.
    
    Args:
        df: DataFrame to save
        file_path: Path to the output file
        format: File format ('csv', 'excel', 'parquet', 'pickle')
    """
    # Ensure the directory exists
    directory = os.path.dirname(file_path)
    if directory:
        ensure_directory_exists(directory)
    
    # Save the DataFrame in the specified format
    if format.lower() == 'csv':
        df.to_csv(file_path, index=False)
    elif format.lower() == 'excel':
        df.to_excel(file_path, index=False)
    elif format.lower() == 'parquet':
        df.to_parquet(file_path, index=False)
    elif format.lower() == 'pickle':
        df.to_pickle(file_path)
    else:
        raise ValueError(f"Unsupported format: {format}")
    
    logger.debug(f"Saved DataFrame to {file_path} in {format} format")


def load_dataframe(file_path: str, format: Optional[str] = None) -> pd.DataFrame:
    """Load a pandas DataFrame from a file.
    
    Args:
        file_path: Path to the input file
        format: File format (default: None, inferred from file extension)
        
    Returns:
        Loaded DataFrame
        
    Raises:
        FileNotFoundError: If the file does not exist
    """
    # Infer format from file extension if not provided
    if format is None:
        _, ext = os.path.splitext(file_path)
        ext = ext.lower()[1:]  # Remove the dot and convert to lowercase
        if ext == 'xlsx' or ext == 'xls':
            format = 'excel'
        elif ext == 'parquet':
            format = 'parquet'
        elif ext == 'pkl' or ext == 'pickle':
            format = 'pickle'
        else:
            format = 'csv'
    
    # Load the DataFrame from the specified format
    if format.lower() == 'csv':
        df = pd.read_csv(file_path)
    elif format.lower() == 'excel':
        df = pd.read_excel(file_path)
    elif format.lower() == 'parquet':
        df = pd.read_parquet(file_path)
    elif format.lower() == 'pickle':
        df = pd.read_pickle(file_path)
    else:
        raise ValueError(f"Unsupported format: {format}")
    
    logger.debug(f"Loaded DataFrame from {file_path} in {format} format")
    return df


def get_output_path(base_dir: str, scenario: str, filename: str) -> str:
    """Get the full path for an output file.
    
    Args:
        base_dir: Base output directory
        scenario: Simulation scenario
        filename: Name of the output file
        
    Returns:
        Full path to the output file
    """
    # Create scenario-specific directory
    scenario_dir = os.path.join(base_dir, scenario)
    ensure_directory_exists(scenario_dir)
    
    # Return full path
    return os.path.join(scenario_dir, filename)