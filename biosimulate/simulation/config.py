#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Simulation configuration for the BIOSIMULATE project.

This module defines the configuration parameters for the simulation,
including time periods, scenarios, and output settings.
"""

import os
import json
import random
import numpy as np
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any


@dataclass
class SimulationConfig:
    """Configuration for the BIOSIMULATE simulation.
    
    Attributes:
        start_year: Starting year for the simulation
        end_year: Ending year for the simulation
        scenario: Scenario to simulate
        output_dir: Directory to save simulation results
        seed: Random seed for reproducibility
        params: Additional simulation parameters
    """
    
    start_year: int = 2025
    end_year: int = 2035
    scenario: str = 'baseline'
    output_dir: str = './results'
    seed: Optional[int] = None
    params: Dict[str, Any] = field(default_factory=dict)
    
    def __post_init__(self):
        """Initialize the configuration after creation."""
        # Set random seed if provided
        if self.seed is not None:
            random.seed(self.seed)
            np.random.seed(self.seed)
        
        # Create output directory if it doesn't exist
        os.makedirs(self.output_dir, exist_ok=True)
        
        # Load scenario-specific parameters
        self._load_scenario_params()
    
    def _load_scenario_params(self):
        """Load parameters specific to the selected scenario."""
        # Define baseline parameters
        self.params.update({
            # Market growth parameters
            'market_growth_rate': 0.082,  # 8.2% CAGR
            'market_size_2025': 51.73,  # $51.73 billion
            'market_size_2030': 76.79,  # $76.79 billion

            # Market segments
            'market': {
                'segments': ['grain_crops', 'oilseed_crops', 'specialty_crops', 'fiber_crops'],
                'segment_shares': [0.4, 0.3, 0.2, 0.1],
                'adoption_rate_initial': 0.05,
                'adoption_rate_peak': 0.8
            },
            
            # Technology parameters
            'technology': {
                'crispr_success_rate': 0.25,
                'crispr_precision': 0.90,
                'breeding_cycle_reduction': 0.40
            },
            
            # Regulatory parameters
            'regulatory': {
                'us_approval_time': 4,
                'eu_approval_time': 8.5,
                'emerging_markets_approval_time': 5
            },
            
            # Economic parameters
            'economic': {
                'rd_investment_annual': 13.5,
                'trait_development_cost': 200,
                'regulatory_compliance_cost_ratio': 0.275,
                'market_launch_cost': 100
            },
            
            # Adoption parameters
            'adoption': {
                'farmer_roi_threshold': 0.20,
                'seed_premium': 0.275,
                'licensing_royalty_rate': 0.10
            }
        })
        
        # Apply scenario-specific parameter adjustments
        if self.scenario == 'regulatory_harmonization':
            self.params.update({
                'eu_approval_time': 6.0,  # Reduced from 8.5 years
                'regulatory_compliance_cost_ratio': 0.20,  # Reduced from 27.5%
                'farmer_roi_threshold': 0.18,  # Reduced from 20%
            })
        
        elif self.scenario == 'climate_crisis':
            self.params.update({
                'market_growth_rate': 0.095,  # Increased from 8.2%
                'farmer_roi_threshold': 0.15,  # Reduced from 20%
                'seed_premium': 0.35,  # Increased from 27.5%
            })
        
        elif self.scenario == 'tech_breakthrough':
            self.params.update({
                'crispr_success_rate': 0.40,  # Increased from 25%
                'crispr_precision': 0.98,  # Increased from 90%
                'breeding_cycle_reduction': 0.60,  # Increased from 40%
                'trait_development_cost': 150,  # Reduced from $200 million
            })
        
        elif self.scenario == 'market_disruption':
            self.params.update({
                'market_growth_rate': 0.065,  # Reduced from 8.2%
                'rd_investment_annual': 16.0,  # Increased from $13.5 billion
                'seed_premium': 0.20,  # Reduced from 27.5%
                'licensing_royalty_rate': 0.08,  # Reduced from 10%
            })
    
    def save(self, filepath: Optional[str] = None) -> None:
        """Save the configuration to a JSON file.
        
        Args:
            filepath: Path to save the configuration file. If None, uses
                a default path in the output directory.
        """
        if filepath is None:
            filepath = os.path.join(
                self.output_dir, 
                f"config_{self.scenario}_{self.start_year}_{self.end_year}.json"
            )
        
        # Create a dictionary representation of the configuration
        config_dict = {
            'start_year': self.start_year,
            'end_year': self.end_year,
            'scenario': self.scenario,
            'seed': self.seed,
            'params': self.params
        }
        
        # Save to file
        with open(filepath, 'w') as f:
            json.dump(config_dict, f, indent=2)
    
    @classmethod
    def load(cls, filepath: str) -> 'SimulationConfig':
        """Load a configuration from a JSON file.
        
        Args:
            filepath: Path to the configuration file.
            
        Returns:
            A SimulationConfig instance.
        """
        with open(filepath, 'r') as f:
            config_dict = json.load(f)
        
        # Create a new instance with the loaded parameters
        config = cls(
            start_year=config_dict['start_year'],
            end_year=config_dict['end_year'],
            scenario=config_dict['scenario'],
            seed=config_dict['seed']
        )
        
        # Update parameters
        config.params.update(config_dict['params'])
        
        return config