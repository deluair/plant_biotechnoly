#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Innovation Model module for the BIOSIMULATE project.

This module implements the innovation model that simulates the discovery
and development of new technologies and traits in the plant biotechnology
industry simulation.
"""

import logging
import random
import uuid
from typing import Dict, List, Any, Optional

from biosimulate.simulation.config import SimulationConfig


class InnovationModel:
    """Innovation model for simulating technology and trait discovery.
    
    This class simulates the innovation process in the plant biotechnology
    industry, including the discovery of new technologies and traits based
    on research activities and collaborations between agents.
    
    Attributes:
        config: Simulation configuration
        technology_categories: List of available technology categories
        trait_categories: List of available trait categories
    """
    
    def __init__(self, config: SimulationConfig):
        """Initialize the innovation model.
        
        Args:
            config: Simulation configuration
        """
        self.config = config
        self.logger = logging.getLogger(__name__)
        
        # Define available technology categories
        self.technology_categories = [
            "gene_editing",
            "synthetic_biology",
            "genomics",
            "breeding",
            "bioinformatics"
        ]
        
        # Define available trait categories
        self.trait_categories = [
            "yield",
            "drought_resistance",
            "pest_resistance",
            "disease_resistance",
            "herbicide_tolerance",
            "nutritional_enhancement",
            "shelf_life"
        ]
        
        # Initialize innovation parameters
        self.params = {
            # Technology success rates
            "crispr_success_rate": 0.75,
            "breeding_success_rate": 0.85,
            "synthetic_biology_success_rate": 0.60,
            "genomics_success_rate": 0.70,
            "bioinformatics_success_rate": 0.65,
            
            # Development times (in years)
            "technology_development_time": 3.0,
            "trait_development_time": 2.5,
            
            # Cost factors
            "research_cost_factor": 1.0,
            "development_cost_factor": 1.2,
            
            # Innovation probabilities
            "base_discovery_probability": 0.2,
            "collaboration_bonus": 0.15,
            "funding_impact_factor": 0.0000001  # Per dollar of funding
        }
    
    def generate_technology(self, developer_id: str, current_year: int) -> Dict[str, Any]:
        """Generate a new technology.
        
        Args:
            developer_id: ID of the agent developing the technology
            current_year: Current simulation year
        
        Returns:
            Dictionary containing technology attributes
        """
        # Select a random technology category
        category = random.choice(self.technology_categories)
        
        # Generate a unique ID
        technology_id = f"tech_{str(uuid.uuid4())[:8]}"
        
        # Generate technology attributes based on category
        if category == "gene_editing":
            name = "CRISPR-Cas9 Gene Editing"
            maturity = 0.7
            development_cost = 10000000
            success_rate = 0.65
            traits_enabled = ["yield", "drought_resistance", "pest_resistance"]
        elif category == "synthetic_biology":
            name = "Synthetic Biology Platform"
            maturity = 0.5
            development_cost = 15000000
            success_rate = 0.45
            traits_enabled = ["nutritional_enhancement", "shelf_life"]
        elif category == "genomics":
            name = "Advanced Genomics Sequencing"
            maturity = 0.8
            development_cost = 8000000
            success_rate = 0.75
            traits_enabled = ["yield", "disease_resistance"]
        elif category == "breeding":
            name = "Marker-Assisted Breeding"
            maturity = 0.9
            development_cost = 5000000
            success_rate = 0.85
            traits_enabled = ["yield", "drought_resistance"]
        elif category == "bioinformatics":
            name = "AI-Driven Bioinformatics"
            maturity = 0.6
            development_cost = 12000000
            success_rate = 0.55
            traits_enabled = ["yield", "nutritional_enhancement"]
        else:
            name = f"Generic {category.title()} Technology"
            maturity = 0.5
            development_cost = 10000000
            success_rate = 0.5
            traits_enabled = [random.choice(self.trait_categories)]
        
        # Create technology dictionary
        technology = {
            "id": technology_id,
            "name": name,
            "category": category,
            "maturity": maturity,
            "development_cost": development_cost,
            "success_rate": success_rate,
            "traits_enabled": traits_enabled,
            "developer_id": developer_id,
            "discovery_year": current_year
        }
        
        self.logger.info(f"Generated new technology: {name} (ID: {technology_id})")
        
        return technology
    
    def generate_trait(self, developer_id: str, current_year: int) -> Dict[str, Any]:
        """Generate a new trait.
        
        Args:
            developer_id: ID of the agent developing the trait
            current_year: Current simulation year
        
        Returns:
            Dictionary containing trait attributes
        """
        # Select a random trait category
        category = random.choice(self.trait_categories)
        
        # Generate a unique ID
        trait_id = f"trait_{str(uuid.uuid4())[:8]}"
        
        # Generate trait attributes based on category
        if category == "yield":
            name = "High Yield"
            description = "Increases crop yield"
            complexity = 0.8
            development_cost = 5000000
            market_value = 0.75
            sustainability_impact = 0.3
            technologies_required = ["gene_editing", "breeding"]
        elif category == "drought_resistance":
            name = "Drought Resistance"
            description = "Enhances crop survival in drought conditions"
            complexity = 0.7
            development_cost = 4500000
            market_value = 0.8
            sustainability_impact = 0.7
            technologies_required = ["gene_editing", "genomics"]
        elif category == "pest_resistance":
            name = "Pest Resistance"
            description = "Reduces crop damage from pests"
            complexity = 0.6
            development_cost = 4000000
            market_value = 0.7
            sustainability_impact = 0.5
            technologies_required = ["gene_editing"]
        elif category == "disease_resistance":
            name = "Disease Resistance"
            description = "Reduces crop damage from diseases"
            complexity = 0.65
            development_cost = 4200000
            market_value = 0.75
            sustainability_impact = 0.6
            technologies_required = ["gene_editing", "genomics"]
        elif category == "herbicide_tolerance":
            name = "Herbicide Tolerance"
            description = "Allows crops to survive herbicide application"
            complexity = 0.5
            development_cost = 3500000
            market_value = 0.65
            sustainability_impact = 0.2
            technologies_required = ["gene_editing"]
        elif category == "nutritional_enhancement":
            name = "Nutritional Enhancement"
            description = "Improves nutritional content of crops"
            complexity = 0.75
            development_cost = 5500000
            market_value = 0.7
            sustainability_impact = 0.8
            technologies_required = ["synthetic_biology", "gene_editing"]
        elif category == "shelf_life":
            name = "Extended Shelf Life"
            description = "Extends the shelf life of harvested crops"
            complexity = 0.6
            development_cost = 4000000
            market_value = 0.6
            sustainability_impact = 0.4
            technologies_required = ["synthetic_biology"]
        else:
            name = f"Generic {category.title()} Trait"
            description = f"Enhances {category} in crops"
            complexity = 0.5
            development_cost = 4000000
            market_value = 0.5
            sustainability_impact = 0.5
            technologies_required = [random.choice(self.technology_categories)]
        
        # Create trait dictionary
        trait = {
            "id": trait_id,
            "name": name,
            "category": category,
            "description": description,
            "complexity": complexity,
            "development_cost": development_cost,
            "market_value": market_value,
            "sustainability_impact": sustainability_impact,
            "technologies_required": technologies_required,
            "developer_id": developer_id,
            "development_stage": "research",
            "discovery_year": current_year
        }
        
        self.logger.info(f"Generated new trait: {name} (ID: {trait_id})")
        
        return trait
    
    def calculate_research_output(self, research_inputs: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate research output based on inputs.
        
        Args:
            research_inputs: Dictionary containing research inputs such as
                research_capacity, funding, collaboration_level, focus_areas,
                and existing_knowledge.
        
        Returns:
            Dictionary containing research output metrics
        """
        # Extract research inputs
        research_capacity = research_inputs.get("research_capacity", 50)  # 0-100 scale
        funding = research_inputs.get("funding", 1000000)  # in dollars
        collaboration_level = research_inputs.get("collaboration_level", 0.5)  # 0-1 scale
        focus_areas = research_inputs.get("focus_areas", [])  # list of technology categories
        existing_knowledge = research_inputs.get("existing_knowledge", 0.5)  # 0-1 scale
        
        # Calculate knowledge gain
        # Base knowledge gain from research capacity
        knowledge_gain = (research_capacity / 100) * 0.2
        
        # Funding impact (diminishing returns)
        funding_impact = min(0.3, funding * self.params["funding_impact_factor"])
        knowledge_gain += funding_impact
        
        # Collaboration bonus
        collaboration_bonus = collaboration_level * self.params["collaboration_bonus"]
        knowledge_gain += collaboration_bonus
        
        # Existing knowledge impact (diminishing returns for high knowledge)
        knowledge_factor = existing_knowledge * (1 - existing_knowledge/2)
        knowledge_gain *= (1 + knowledge_factor)
        
        # Calculate discovery probability
        discovery_probability = self.params["base_discovery_probability"]
        discovery_probability += (research_capacity / 100) * 0.3
        discovery_probability += funding_impact * 0.5
        discovery_probability += collaboration_bonus
        discovery_probability = min(0.95, max(0.05, discovery_probability))
        
        # Determine potential technologies based on focus areas
        potential_technologies = []
        for area in focus_areas:
            if area in self.technology_categories:
                potential_technologies.append(area)
        
        # If no specific focus areas, consider all technologies
        if not potential_technologies:
            potential_technologies = self.technology_categories.copy()
        
        return {
            "knowledge_gain": knowledge_gain,
            "discovery_probability": discovery_probability,
            "potential_technologies": potential_technologies,
            "research_efficiency": (knowledge_gain / max(1, funding / 1000000)),
            "focus_strength": len(focus_areas) / len(self.technology_categories) if focus_areas else 0.5
        }
    
    def simulate_discovery(self, discovery_params: Dict[str, Any]) -> Dict[str, Any]:
        """Simulate technology discovery based on research parameters.
        
        Args:
            discovery_params: Dictionary containing discovery parameters such as
                research_entity_id, research_focus, discovery_probability, and year.
        
        Returns:
            Dictionary containing discovery results
        """
        # Extract discovery parameters
        research_entity_id = discovery_params.get("research_entity_id", "unknown")
        research_focus = discovery_params.get("research_focus", [])
        discovery_probability = discovery_params.get("discovery_probability", 0.2)
        year = discovery_params.get("year", 2020)
        
        # Initialize result
        result = {
            "discovery_made": False,
            "research_entity_id": research_entity_id,
            "year": year
        }
        
        # Determine if discovery is made
        if random.random() < discovery_probability:
            result["discovery_made"] = True
            
            # Determine technology category based on research focus
            if research_focus and all(focus in self.technology_categories for focus in research_focus):
                category = random.choice(research_focus)
            else:
                category = random.choice(self.technology_categories)
            
            # Generate technology
            technology = self.generate_technology(research_entity_id, year)
            
            # Override category if needed
            if category != technology["category"]:
                technology["category"] = category
                
                # Adjust other attributes based on category
                if category == "gene_editing":
                    technology["success_rate"] = self.params["crispr_success_rate"]
                elif category == "breeding":
                    technology["success_rate"] = self.params["breeding_success_rate"]
                elif category == "synthetic_biology":
                    technology["success_rate"] = self.params["synthetic_biology_success_rate"]
                elif category == "genomics":
                    technology["success_rate"] = self.params["genomics_success_rate"]
                elif category == "bioinformatics":
                    technology["success_rate"] = self.params["bioinformatics_success_rate"]
            
            result["technology"] = technology
            self.logger.info(f"Discovery made by {research_entity_id}: {technology['name']}")
        else:
            self.logger.info(f"No discovery made by {research_entity_id} this year")
        
        return result
        
    def calculate_development_success(self, development_params: Dict[str, Any]) -> float:
        """Calculate the probability of successful technology development.
        
        Args:
            development_params: Dictionary containing development parameters
                - technology_maturity: Float between 0-1 indicating technology maturity
                - trait_complexity: Float between 0-1 indicating trait complexity
                - research_capacity: Integer representing research capacity
                - investment: Float representing financial investment
                - technology_category: String indicating technology category
                
        Returns:
            Float between 0-1 representing success probability
        """
        # Extract parameters
        tech_maturity = development_params.get("technology_maturity", 0.5)
        trait_complexity = development_params.get("trait_complexity", 0.5)
        research_capacity = development_params.get("research_capacity", 50)
        investment = development_params.get("investment", 1000000)
        tech_category = development_params.get("technology_category", "breeding")
        
        # Get base success rate for technology category
        base_success_rate = 0.6
        if tech_category == "gene_editing":
            base_success_rate = self.params["crispr_success_rate"]
        elif tech_category == "breeding":
            base_success_rate = self.params["breeding_success_rate"]
        elif tech_category == "synthetic_biology":
            base_success_rate = self.params["synthetic_biology_success_rate"]
        elif tech_category == "genomics":
            base_success_rate = self.params["genomics_success_rate"]
        elif tech_category == "bioinformatics":
            base_success_rate = self.params["bioinformatics_success_rate"]
        
        # Calculate modifiers
        maturity_modifier = tech_maturity * 0.3  # Higher maturity increases success
        complexity_modifier = -trait_complexity * 0.4  # Higher complexity decreases success
        
        # Research capacity and investment have diminishing returns
        capacity_modifier = min(0.2, (research_capacity / 100) * 0.2)
        investment_modifier = min(0.2, (investment / 5000000) * 0.2)
        
        # Calculate final success probability
        success_probability = base_success_rate + maturity_modifier + complexity_modifier + capacity_modifier + investment_modifier
        
        # Ensure probability is between 0 and 1
        success_probability = max(0.0, min(1.0, success_probability))
        
        return success_probability
        
    def simulate_innovation(self, current_year: int, agents: Dict[str, Any]) -> Dict[str, Any]:
        """Simulate innovation for a year.
        
        This method simulates the innovation process for a year, potentially
        generating new technologies and traits based on research activities
        and collaborations between agents.
        
        Args:
            current_year: Current simulation year
            agents: Dictionary of agent instances by ID
        
        Returns:
            Dictionary containing innovation results
        """
        # Initialize results
        results = {
            "new_technologies": [],
            "new_traits": []
        }
        
        # Simplified innovation simulation
        # In a real implementation, this would consider agent research capacity,
        # funding, collaborations, and other factors
        
        # Chance to generate a new technology
        if random.random() < 0.3:  # 30% chance per year
            # Select a random research entity or commercial player as developer
            developer_candidates = [agent_id for agent_id, agent in agents.items()
                                  if agent.get('type') in ['research_entity', 'commercial_player']]
            if developer_candidates:
                developer_id = random.choice(developer_candidates)
                technology = self.generate_technology(developer_id, current_year)
                results["new_technologies"].append(technology)
        
        # Chance to generate a new trait
        if random.random() < 0.4:  # 40% chance per year
            # Select a random commercial player as developer
            developer_candidates = [agent_id for agent_id, agent in agents.items()
                                  if agent.get('type') == 'commercial_player']
            if developer_candidates:
                developer_id = random.choice(developer_candidates)
                trait = self.generate_trait(developer_id, current_year)
                results["new_traits"].append(trait)
        
        return results