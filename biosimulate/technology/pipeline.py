#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Technology Pipeline module for the BIOSIMULATE project.

This module implements the technology pipeline that tracks the development
and maturation of various technologies and traits in the plant biotechnology
industry simulation.
"""

import logging
from typing import Dict, List, Any, Optional

from biosimulate.simulation.config import SimulationConfig


class TechnologyPipeline:
    """Technology pipeline for tracking technology and trait development.
    
    This class manages the pipeline of technologies and traits being developed
    in the simulation, including their discovery, development, and commercialization.
    
    Attributes:
        config: Simulation configuration
        technologies: Dictionary of technology instances by ID
        traits: Dictionary of trait instances by ID
    """
    
    def __init__(self, config: SimulationConfig):
        """Initialize the technology pipeline.
        
        Args:
            config: Simulation configuration
        """
        self.config = config
        self.logger = logging.getLogger(__name__)
        
        # Initialize technology and trait dictionaries
        self.technologies = {}
        self.traits = {}
    
    def register_technology(self, technology: Dict[str, Any]) -> str:
        """Register a new technology in the pipeline.
        
        Args:
            technology: Dictionary containing technology attributes
        
        Returns:
            ID of the registered technology
        """
        technology_id = technology.get('id')
        if not technology_id:
            raise ValueError("Technology must have an ID")
        
        self.technologies[technology_id] = technology
        self.logger.info(f"Registered technology: {technology['name']} (ID: {technology_id})")
        
        return technology_id
    
    def register_trait(self, trait: Dict[str, Any]) -> str:
        """Register a new trait in the pipeline.
        
        Args:
            trait: Dictionary containing trait attributes
        
        Returns:
            ID of the registered trait
        """
        trait_id = trait.get('id')
        if not trait_id:
            raise ValueError("Trait must have an ID")
        
        self.traits[trait_id] = trait
        self.logger.info(f"Registered trait: {trait['name']} (ID: {trait_id})")
        
        return trait_id
    
    def get_technology(self, technology_id: str) -> Optional[Dict[str, Any]]:
        """Get a technology by ID.
        
        Args:
            technology_id: ID of the technology to retrieve
        
        Returns:
            Technology dictionary or None if not found
        """
        return self.technologies.get(technology_id)
    
    def get_trait(self, trait_id: str) -> Optional[Dict[str, Any]]:
        """Get a trait by ID.
        
        Args:
            trait_id: ID of the trait to retrieve
        
        Returns:
            Trait dictionary or None if not found
        """
        return self.traits.get(trait_id)
    
    def advance_year(self, current_year: int, agents: Dict[str, Any]) -> Dict[str, Any]:
        """Update the technology pipeline for a year.
        
        This method advances the development of technologies and traits,
        updates their maturity and status, and potentially creates new
        technologies and traits based on innovation dynamics.
        
        Args:
            current_year: Current simulation year
            agents: Dictionary of agent instances by ID
        
        Returns:
            Dictionary containing update results
        """
        # Initialize results
        results = {
            "technologies_updated": [],
            "traits_updated": [],
            "new_technologies": [],
            "new_traits": []
        }
        
        # Update existing technologies
        for tech_id, technology in self.technologies.items():
            # Update technology maturity and status
            # This is a simplified implementation
            if technology.get('maturity', 0) < 1.0:
                technology['maturity'] = min(technology.get('maturity', 0) + 0.1, 1.0)
                results["technologies_updated"].append(tech_id)
        
        # Update existing traits
        for trait_id, trait in self.traits.items():
            # Update trait development stage
            # This is a simplified implementation
            if trait.get('development_stage') == 'research':
                # Chance to advance to development stage
                trait['development_stage'] = 'development'
                results["traits_updated"].append(trait_id)
            elif trait.get('development_stage') == 'development':
                # Chance to advance to regulatory stage
                trait['development_stage'] = 'regulatory'
                results["traits_updated"].append(trait_id)
            elif trait.get('development_stage') == 'regulatory':
                # Chance to advance to commercial stage
                trait['development_stage'] = 'commercial'
                results["traits_updated"].append(trait_id)
        
        # Return update results
        return results