#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Main simulation runner for the BIOSIMULATE project.

This module serves as the entry point for running the plant biotechnology
industry ecosystem simulation. It orchestrates the initialization of agents,
regulatory frameworks, technology pipelines, and economic models, then
executes the simulation over the specified time period (2025-2035).
"""

import argparse
import logging
import sys
import os
import pandas as pd
from datetime import datetime

from biosimulate.simulation.engine import SimulationEngine
from biosimulate.simulation.config import SimulationConfig
from biosimulate.utils.logging_config import setup_logging


def parse_arguments():
    """Parse command line arguments for the simulation."""
    parser = argparse.ArgumentParser(
        description='Run the BIOSIMULATE plant biotechnology industry simulation'
    )
    
    parser.add_argument(
        '--start-year', 
        type=int, 
        default=2025,
        help='Starting year for the simulation (default: 2025)'
    )
    
    parser.add_argument(
        '--end-year', 
        type=int, 
        default=2035,
        help='Ending year for the simulation (default: 2035)'
    )
    
    parser.add_argument(
        '--scenario', 
        type=str, 
        default='baseline',
        choices=['baseline', 'regulatory_harmonization', 'climate_crisis', 
                 'tech_breakthrough', 'market_disruption'],
        help='Scenario to simulate (default: baseline)'
    )
    
    parser.add_argument(
        '--output-dir', 
        type=str, 
        default='./results',
        help='Directory to save simulation results (default: ./results)'
    )
    
    parser.add_argument(
        '--seed', 
        type=int, 
        default=None,
        help='Random seed for reproducibility (default: None)'
    )
    
    parser.add_argument(
        '--verbose', 
        action='store_true',
        help='Enable verbose output'
    )
    
    return parser.parse_args()


def main():
    """Main entry point for the simulation."""
    args = parse_arguments()
    
    # Setup logging
    log_level = logging.DEBUG if args.verbose else logging.INFO
    setup_logging(log_level)
    logger = logging.getLogger(__name__)
    
    logger.info(f"Starting BIOSIMULATE simulation at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    logger.info(f"Scenario: {args.scenario}")
    logger.info(f"Time period: {args.start_year}-{args.end_year}")
    
    try:
        # Create output directory if it doesn't exist
        os.makedirs(args.output_dir, exist_ok=True)

        # Initialize simulation configuration
        config = SimulationConfig(
            start_year=args.start_year,
            end_year=args.end_year,
            scenario=args.scenario,
            output_dir=args.output_dir,
            seed=args.seed
        )
        
        # Create and run the simulation engine
        engine = SimulationEngine(config)
        results = engine.run()
        
        # Results are now processed and saved within the engine's run method
        if not results or results.get('dataframe', pd.DataFrame()).empty:
            logger.warning("Simulation completed but produced no result data.")
        
        logger.info(f"Simulation completed successfully at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        return 0
        
    except Exception as e:
        logger.exception(f"Simulation failed: {str(e)}")
        return 1


if __name__ == "__main__":
    sys.exit(main())