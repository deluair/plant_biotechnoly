#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Metrics tracking for the BIOSIMULATE project.

This module implements the metrics tracking system that collects and
analyzes performance indicators throughout the simulation.
"""

import logging
import pandas as pd
import numpy as np
from typing import Dict, List, Any, Optional

from biosimulate.simulation.config import SimulationConfig


class MetricsTracker:
    """Tracks and analyzes metrics throughout the simulation.
    
    This class collects various performance indicators related to innovation,
    market development, and societal impact throughout the simulation run.
    
    Attributes:
        config: Simulation configuration
        logger: Logger instance
        metrics: Dictionary of metric collections
    """
    
    def __init__(self, config: SimulationConfig):
        """Initialize the metrics tracker.
        
        Args:
            config: Simulation configuration
        """
        self.config = config
        self.logger = logging.getLogger(__name__)
        
        # Initialize metrics collections
        self.metrics = {
            # Innovation metrics
            'patent_filings': [],
            'research_collaborations': [],
            'time_to_market': [],
            
            # Market development metrics
            'technology_adoption': [],
            'market_concentration': [],
            'price_premiums': [],
            
            # Societal impact metrics
            'food_security': [],
            'environmental_impact': [],
            'economic_development': []
        }
        
        self.logger.info("Initialized metrics tracker")
    
    def record_year(self, year: int, agents: Dict[str, Any], 
                   technology_pipeline: Any, regulatory_framework: Any, 
                   market_model: Any) -> None:
        """Record metrics for a simulation year.
        
        Args:
            year: Current simulation year
            agents: Dictionary of agent instances
            technology_pipeline: Technology pipeline instance
            regulatory_framework: Regulatory framework instance
            market_model: Market model instance
        """
        self.logger.debug(f"Recording metrics for year {year}")
        
        # Record innovation metrics
        self._record_innovation_metrics(year, agents, technology_pipeline)
        
        # Record market development metrics
        self._record_market_metrics(year, agents, market_model)
        
        # Record societal impact metrics
        self._record_societal_metrics(year, agents, technology_pipeline, market_model)
    
    def _record_innovation_metrics(self, year: int, agents: Dict[str, Any], 
                                  technology_pipeline: Any) -> None:
        """Record innovation-related metrics.
        
        Args:
            year: Current simulation year
            agents: Dictionary of agent instances
            technology_pipeline: Technology pipeline instance
        """
        # Patent filing trends
        patent_data = self._collect_patent_data(year, agents, technology_pipeline)
        self.metrics['patent_filings'].append(patent_data)
        
        # Research collaboration network
        collab_data = self._analyze_research_collaborations(year, agents)
        self.metrics['research_collaborations'].append(collab_data)
        
        # Time-to-market acceleration
        ttm_data = self._analyze_time_to_market(year, technology_pipeline)
        self.metrics['time_to_market'].append(ttm_data)
    
    def _record_market_metrics(self, year: int, agents: Dict[str, Any], 
                              market_model: Any) -> None:
        """Record market development metrics.
        
        Args:
            year: Current simulation year
            agents: Dictionary of agent instances
            market_model: Market model instance
        """
        # Technology adoption curves
        adoption_data = self._analyze_technology_adoption(year, agents, market_model)
        self.metrics['technology_adoption'].append(adoption_data)
        
        # Market concentration ratios
        concentration_data = self._calculate_market_concentration(year, agents, market_model)
        self.metrics['market_concentration'].append(concentration_data)
        
        # Price premium sustainability
        premium_data = self._analyze_price_premiums(year, market_model)
        self.metrics['price_premiums'].append(premium_data)
    
    def _record_societal_metrics(self, year: int, agents: Dict[str, Any], 
                               technology_pipeline: Any, market_model: Any) -> None:
        """Record societal impact metrics.
        
        Args:
            year: Current simulation year
            agents: Dictionary of agent instances
            technology_pipeline: Technology pipeline instance
            market_model: Market model instance
        """
        # Food security improvement indicators
        food_security_data = self._analyze_food_security(year, agents, technology_pipeline)
        self.metrics['food_security'].append(food_security_data)
        
        # Environmental sustainability measures
        env_data = self._analyze_environmental_impact(year, agents, technology_pipeline)
        self.metrics['environmental_impact'].append(env_data)
        
        # Economic development effects
        econ_data = self._analyze_economic_development(year, agents, market_model)
        self.metrics['economic_development'].append(econ_data)
    
    def _collect_patent_data(self, year: int, agents: Dict[str, Any], 
                            technology_pipeline: Any) -> Dict[str, Any]:
        """Collect patent filing data for the current year.
        
        Args:
            year: Current simulation year
            agents: Dictionary of agent instances
            technology_pipeline: Technology pipeline instance
            
        Returns:
            Dictionary containing patent filing metrics
        """
        # In a full implementation, this would analyze actual patent filings by agents
        # For this simulation, we'll generate synthetic data based on the scenario
        
        # Base patent counts by technology category
        base_counts = {
            'crispr': 120,
            'synthetic_biology': 85,
            'breeding': 65,
            'other': 30
        }
        
        # Adjust based on year (increasing trend)
        year_factor = 1.0 + 0.05 * (year - self.config.start_year)
        
        # Adjust based on scenario
        scenario_factors = {
            'baseline': 1.0,
            'regulatory_harmonization': 1.1,
            'climate_crisis': 1.2,
            'tech_breakthrough': 1.5,
            'market_disruption': 0.9
        }
        scenario_factor = scenario_factors.get(self.config.scenario, 1.0)
        
        # Calculate patent counts
        patent_counts = {}
        for tech, base_count in base_counts.items():
            count = int(base_count * year_factor * scenario_factor * (0.9 + 0.2 * np.random.random()))
            patent_counts[tech] = count
        
        # Geographic distribution
        geo_distribution = {
            'north_america': 0.35,
            'europe': 0.25,
            'asia_pacific': 0.30,
            'latin_america': 0.07,
            'africa_middle_east': 0.03
        }
        
        # Adjust geographic distribution based on scenario
        if self.config.scenario == 'market_disruption':
            geo_distribution['asia_pacific'] += 0.05
            geo_distribution['north_america'] -= 0.05
        elif self.config.scenario == 'tech_breakthrough':
            geo_distribution['north_america'] += 0.03
            geo_distribution['europe'] += 0.02
            geo_distribution['africa_middle_east'] -= 0.05
        
        # Calculate geographic counts
        geo_counts = {}
        total_patents = sum(patent_counts.values())
        for region, share in geo_distribution.items():
            geo_counts[region] = int(total_patents * share)
        
        return {
            'year': year,
            'total_patents': total_patents,
            'by_technology': patent_counts,
            'by_geography': geo_counts
        }
    
    def _analyze_research_collaborations(self, year: int, agents: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze research collaboration networks.
        
        Args:
            year: Current simulation year
            agents: Dictionary of agent instances
            
        Returns:
            Dictionary containing research collaboration metrics
        """
        # In a full implementation, this would analyze actual collaboration networks
        # For this simulation, we'll generate synthetic data
        
        # Base collaboration metrics
        base_metrics = {
            'total_collaborations': 250,
            'academic_industry': 120,
            'cross_border': 85,
            'public_private': 45
        }
        
        # Adjust based on year (increasing trend)
        year_factor = 1.0 + 0.08 * (year - self.config.start_year)
        
        # Adjust based on scenario
        scenario_factors = {
            'baseline': 1.0,
            'regulatory_harmonization': 1.15,
            'climate_crisis': 1.25,
            'tech_breakthrough': 1.3,
            'market_disruption': 0.95
        }
        scenario_factor = scenario_factors.get(self.config.scenario, 1.0)
        
        # Calculate collaboration metrics
        collab_metrics = {}
        for metric, base_value in base_metrics.items():
            value = int(base_value * year_factor * scenario_factor * (0.95 + 0.1 * np.random.random()))
            collab_metrics[metric] = value
        
        # Network density (0-1 scale)
        network_density = min(0.95, 0.3 + 0.05 * (year - self.config.start_year))
        
        # Average collaborations per entity
        avg_collaborations = 2.5 + 0.2 * (year - self.config.start_year)
        
        return {
            'year': year,
            'metrics': collab_metrics,
            'network_density': network_density,
            'avg_collaborations_per_entity': avg_collaborations
        }
    
    def _analyze_time_to_market(self, year: int, technology_pipeline: Any) -> Dict[str, Any]:
        """Analyze time-to-market acceleration rates.
        
        Args:
            year: Current simulation year
            technology_pipeline: Technology pipeline instance
            
        Returns:
            Dictionary containing time-to-market metrics
        """
        # Base time-to-market in years by technology category
        base_ttm = {
            'crispr': 7.0,
            'synthetic_biology': 5.5,
            'breeding': 4.0
        }
        
        # Improvement rate per year
        improvement_rate = 0.03  # 3% improvement per year
        
        # Adjust based on scenario
        scenario_factors = {
            'baseline': 1.0,
            'regulatory_harmonization': 0.85,  # 15% faster
            'climate_crisis': 0.9,  # 10% faster
            'tech_breakthrough': 0.75,  # 25% faster
            'market_disruption': 1.05  # 5% slower
        }
        scenario_factor = scenario_factors.get(self.config.scenario, 1.0)
        
        # Calculate current time-to-market
        years_elapsed = year - self.config.start_year
        current_ttm = {}
        for tech, base in base_ttm.items():
            # Time decreases with improvements over time
            reduction_factor = (1.0 - improvement_rate) ** years_elapsed
            current_ttm[tech] = base * reduction_factor * scenario_factor
        
        # Overall average
        avg_ttm = sum(current_ttm.values()) / len(current_ttm)
        
        # Improvement from start year
        if years_elapsed == 0:
            avg_improvement = 0.0
        else:
            avg_base = sum(base_ttm.values()) / len(base_ttm)
            avg_improvement = (avg_base - avg_ttm) / avg_base * 100.0
        
        return {
            'year': year,
            'by_technology': current_ttm,
            'average_ttm': avg_ttm,
            'improvement_pct': avg_improvement
        }
    
    def _analyze_technology_adoption(self, year: int, agents: Dict[str, Any], 
                                    market_model: Any) -> Dict[str, Any]:
        """Analyze technology adoption curves by crop and region.
        
        Args:
            year: Current simulation year
            agents: Dictionary of agent instances
            market_model: Market model instance
            
        Returns:
            Dictionary containing technology adoption metrics
        """
        # Base adoption rates by crop type and region
        base_adoption = {
            'staple': {
                'north_america': 0.85,
                'europe': 0.35,
                'asia_pacific': 0.60,
                'latin_america': 0.75,
                'africa_middle_east': 0.40
            },
            'fruits_vegetables': {
                'north_america': 0.40,
                'europe': 0.20,
                'asia_pacific': 0.30,
                'latin_america': 0.35,
                'africa_middle_east': 0.15
            },
            'specialty': {
                'north_america': 0.30,
                'europe': 0.15,
                'asia_pacific': 0.20,
                'latin_america': 0.25,
                'africa_middle_east': 0.10
            }
        }
        
        # Annual growth rates by crop type
        annual_growth = {
            'staple': 0.02,  # 2% annual growth
            'fruits_vegetables': 0.04,  # 4% annual growth
            'specialty': 0.05  # 5% annual growth
        }
        
        # Adjust based on scenario
        scenario_factors = {
            'baseline': 1.0,
            'regulatory_harmonization': 1.2,  # 20% higher adoption
            'climate_crisis': 1.15,  # 15% higher adoption
            'tech_breakthrough': 1.25,  # 25% higher adoption
            'market_disruption': 0.9  # 10% lower adoption
        }
        scenario_factor = scenario_factors.get(self.config.scenario, 1.0)
        
        # Calculate current adoption rates
        years_elapsed = year - self.config.start_year
        current_adoption = {}
        
        for crop, regions in base_adoption.items():
            current_adoption[crop] = {}
            growth_rate = annual_growth[crop]
            
            for region, base_rate in regions.items():
                # Apply growth over time with logistic curve to cap at 100%
                growth_factor = (1.0 + growth_rate) ** years_elapsed
                raw_rate = base_rate * growth_factor * scenario_factor
                
                # Logistic function to ensure rates stay below 1.0
                current_adoption[crop][region] = min(0.99, raw_rate)
        
        # Calculate weighted average adoption rate
        crop_weights = {'staple': 0.6, 'fruits_vegetables': 0.3, 'specialty': 0.1}
        region_weights = {
            'north_america': 0.25, 
            'europe': 0.2, 
            'asia_pacific': 0.3, 
            'latin_america': 0.15, 
            'africa_middle_east': 0.1
        }
        
        weighted_avg = 0.0
        for crop, crop_weight in crop_weights.items():
            for region, region_weight in region_weights.items():
                weighted_avg += current_adoption[crop][region] * crop_weight * region_weight
        
        return {
            'year': year,
            'by_crop_and_region': current_adoption,
            'weighted_average': weighted_avg
        }
    
    def _calculate_market_concentration(self, year: int, agents: Dict[str, Any], 
                                       market_model: Any) -> Dict[str, Any]:
        """Calculate market concentration ratios.
        
        Args:
            year: Current simulation year
            agents: Dictionary of agent instances
            market_model: Market model instance
            
        Returns:
            Dictionary containing market concentration metrics
        """
        # Base Herfindahl-Hirschman Index (HHI) by market segment
        # HHI ranges from 0 (perfect competition) to 10000 (monopoly)
        base_hhi = {
            'seeds': 2200,  # Moderately concentrated
            'crop_protection': 1800,  # Moderately concentrated
            'synthetic_biology': 1500  # Moderately concentrated
        }
        
        # Annual change in concentration
        annual_change = {
            'seeds': 50,  # Increasing concentration
            'crop_protection': 30,  # Increasing concentration
            'synthetic_biology': -20  # Decreasing concentration (new entrants)
        }
        
        # Adjust based on scenario
        scenario_adjustments = {
            'baseline': {'seeds': 0, 'crop_protection': 0, 'synthetic_biology': 0},
            'regulatory_harmonization': {'seeds': -100, 'crop_protection': -80, 'synthetic_biology': -50},
            'climate_crisis': {'seeds': 150, 'crop_protection': 100, 'synthetic_biology': 50},
            'tech_breakthrough': {'seeds': -200, 'crop_protection': -150, 'synthetic_biology': -100},
            'market_disruption': {'seeds': 300, 'crop_protection': 250, 'synthetic_biology': 200}
        }
        scenario_adj = scenario_adjustments.get(self.config.scenario, 
                                              {'seeds': 0, 'crop_protection': 0, 'synthetic_biology': 0})
        
        # Calculate current HHI
        years_elapsed = year - self.config.start_year
        current_hhi = {}
        
        for segment, base in base_hhi.items():
            change = annual_change[segment] * years_elapsed
            adj = scenario_adj[segment]
            
            # Ensure HHI stays within reasonable bounds
            current_hhi[segment] = max(1000, min(8000, base + change + adj))
        
        # Calculate CR4 (four-firm concentration ratio) from HHI
        # This is a simplification; in reality, CR4 would be calculated directly
        cr4 = {}
        for segment, hhi in current_hhi.items():
            # Approximate CR4 from HHI (simplified relationship)
            cr4[segment] = min(0.95, hhi / 10000 * 1.5)
        
        # Overall market concentration
        segment_weights = {'seeds': 0.4, 'crop_protection': 0.4, 'synthetic_biology': 0.2}
        weighted_hhi = sum(current_hhi[s] * segment_weights[s] for s in current_hhi)
        
        return {
            'year': year,
            'hhi_by_segment': current_hhi,
            'cr4_by_segment': cr4,
            'weighted_hhi': weighted_hhi
        }
    
    def _analyze_price_premiums(self, year: int, market_model: Any) -> Dict[str, Any]:
        """Analyze price premium sustainability.
        
        Args:
            year: Current simulation year
            market_model: Market model instance
            
        Returns:
            Dictionary containing price premium metrics
        """
        # Base price premiums by technology type
        base_premiums = {
            'herbicide_tolerance': 0.35,  # 35% premium
            'insect_resistance': 0.30,  # 30% premium
            'drought_tolerance': 0.40,  # 40% premium
            'yield_enhancement': 0.25,  # 25% premium
            'nutritional_enhancement': 0.20  # 20% premium
        }
        
        # Annual erosion rates
        annual_erosion = {
            'herbicide_tolerance': 0.02,  # 2% annual erosion
            'insect_resistance': 0.015,  # 1.5% annual erosion
            'drought_tolerance': 0.01,  # 1% annual erosion
            'yield_enhancement': 0.015,  # 1.5% annual erosion
            'nutritional_enhancement': 0.01  # 1% annual erosion
        }
        
        # Adjust based on scenario
        scenario_factors = {
            'baseline': 1.0,
            'regulatory_harmonization': 0.95,  # 5% lower premiums
            'climate_crisis': 1.2,  # 20% higher premiums
            'tech_breakthrough': 0.9,  # 10% lower premiums
            'market_disruption': 0.8  # 20% lower premiums
        }
        scenario_factor = scenario_factors.get(self.config.scenario, 1.0)
        
        # Calculate current premiums
        years_elapsed = year - self.config.start_year
        current_premiums = {}
        
        for tech, base in base_premiums.items():
            erosion = annual_erosion[tech] * years_elapsed
            current_premiums[tech] = max(0.05, (base - erosion) * scenario_factor)
        
        # Calculate average premium
        avg_premium = sum(current_premiums.values()) / len(current_premiums)
        
        # Calculate premium erosion rate
        if years_elapsed == 0:
            avg_erosion_rate = 0.0
        else:
            avg_base = sum(base_premiums.values()) / len(base_premiums)
            avg_erosion_rate = (avg_base - avg_premium) / avg_base / years_elapsed * 100.0
        
        return {
            'year': year,
            'by_technology': current_premiums,
            'average_premium': avg_premium,
            'average_erosion_rate_pct': avg_erosion_rate
        }
    
    def _analyze_food_security(self, year: int, agents: Dict[str, Any], 
                              technology_pipeline: Any) -> Dict[str, Any]:
        """Analyze food security improvement indicators.
        
        Args:
            year: Current simulation year
            agents: Dictionary of agent instances
            technology_pipeline: Technology pipeline instance
            
        Returns:
            Dictionary containing food security metrics
        """
        # Base yield gains by crop type (percentage)
        base_yield_gains = {
            'staple': 2.0,  # 2% annual yield gain
            'fruits_vegetables': 1.5,  # 1.5% annual yield gain
            'specialty': 1.0  # 1% annual yield gain
        }
        
        # Base nutrition enhancement by crop type (percentage)
        base_nutrition = {
            'staple': 0.5,  # 0.5% annual nutrition improvement
            'fruits_vegetables': 1.0,  # 1% annual nutrition improvement
            'specialty': 1.5  # 1.5% annual nutrition improvement
        }
        
        # Adjust based on scenario
        scenario_factors = {
            'baseline': {'yield': 1.0, 'nutrition': 1.0},
            'regulatory_harmonization': {'yield': 1.1, 'nutrition': 1.05},
            'climate_crisis': {'yield': 0.8, 'nutrition': 0.9},
            'tech_breakthrough': {'yield': 1.3, 'nutrition': 1.2},
            'market_disruption': {'yield': 0.9, 'nutrition': 0.95}
        }
        scenario_factor = scenario_factors.get(self.config.scenario, {'yield': 1.0, 'nutrition': 1.0})
        
        # Calculate cumulative gains
        years_elapsed = year - self.config.start_year
        
        # Yield gains (compound annual growth)
        yield_gains = {}
        for crop, base in base_yield_gains.items():
            annual_gain = base * scenario_factor['yield'] / 100.0
            cumulative_gain = (1.0 + annual_gain) ** years_elapsed - 1.0
            yield_gains[crop] = cumulative_gain * 100.0  # Convert back to percentage
        
        # Nutrition enhancement (compound annual growth)
        nutrition_gains = {}
        for crop, base in base_nutrition.items():
            annual_gain = base * scenario_factor['nutrition'] / 100.0
            cumulative_gain = (1.0 + annual_gain) ** years_elapsed - 1.0
            nutrition_gains[crop] = cumulative_gain * 100.0  # Convert back to percentage
        
        # Food security index (0-100 scale)
        # Starting from 60 in 2025, improving over time
        base_security_index = 60.0
        annual_improvement = 1.5  # 1.5 points per year
        security_index = min(100.0, base_security_index + 
                           annual_improvement * years_elapsed * scenario_factor['yield'])
        
        return {
            'year': year,
            'yield_gains_pct': yield_gains,
            'nutrition_enhancement_pct': nutrition_gains,
            'food_security_index': security_index
        }
    
    def _analyze_environmental_impact(self, year: int, agents: Dict[str, Any], 
                                     technology_pipeline: Any) -> Dict[str, Any]:
        """Analyze environmental sustainability measures.
        
        Args:
            year: Current simulation year
            agents: Dictionary of agent instances
            technology_pipeline: Technology pipeline instance
            
        Returns:
            Dictionary containing environmental impact metrics
        """
        # Base pesticide reduction (percentage from conventional)
        base_pesticide_reduction = 15.0  # 15% reduction in 2025
        
        # Base fertilizer reduction (percentage from conventional)
        base_fertilizer_reduction = 10.0  # 10% reduction in 2025
        
        # Base carbon footprint reduction (percentage from conventional)
        base_carbon_reduction = 5.0  # 5% reduction in 2025
        
        # Annual improvement rates
        annual_improvements = {
            'pesticide': 2.0,  # 2 percentage points per year
            'fertilizer': 1.5,  # 1.5 percentage points per year
            'carbon': 1.0  # 1 percentage point per year
        }
        
        # Adjust based on scenario
        scenario_factors = {
            'baseline': {'pesticide': 1.0, 'fertilizer': 1.0, 'carbon': 1.0},
            'regulatory_harmonization': {'pesticide': 1.1, 'fertilizer': 1.05, 'carbon': 1.1},
            'climate_crisis': {'pesticide': 1.2, 'fertilizer': 1.3, 'carbon': 1.5},
            'tech_breakthrough': {'pesticide': 1.3, 'fertilizer': 1.4, 'carbon': 1.2},
            'market_disruption': {'pesticide': 0.9, 'fertilizer': 0.95, 'carbon': 1.0}
        }
        scenario_factor = scenario_factors.get(self.config.scenario, 
                                             {'pesticide': 1.0, 'fertilizer': 1.0, 'carbon': 1.0})
        
        # Calculate current reductions
        years_elapsed = year - self.config.start_year
        
        pesticide_reduction = min(80.0, base_pesticide_reduction + 
                                annual_improvements['pesticide'] * years_elapsed * 
                                scenario_factor['pesticide'])
        
        fertilizer_reduction = min(70.0, base_fertilizer_reduction + 
                                 annual_improvements['fertilizer'] * years_elapsed * 
                                 scenario_factor['fertilizer'])
        
        carbon_reduction = min(60.0, base_carbon_reduction + 
                             annual_improvements['carbon'] * years_elapsed * 
                             scenario_factor['carbon'])
        
        # Environmental sustainability index (0-100 scale)
        # Starting from 50 in 2025, improving over time
        base_sustainability_index = 50.0
        annual_improvement = 2.0  # 2 points per year
        avg_scenario_factor = (scenario_factor['pesticide'] + 
                              scenario_factor['fertilizer'] + 
                              scenario_factor['carbon']) / 3.0
        
        sustainability_index = min(100.0, base_sustainability_index + 
                                 annual_improvement * years_elapsed * avg_scenario_factor)
        
        return {
            'year': year,
            'pesticide_reduction_pct': pesticide_reduction,
            'fertilizer_reduction_pct': fertilizer_reduction,
            'carbon_footprint_reduction_pct': carbon_reduction,
            'sustainability_index': sustainability_index
        }
    
    def _analyze_economic_development(self, year: int, agents: Dict[str, Any], 
                                     market_model: Any) -> Dict[str, Any]:
        """Analyze economic development effects.
        
        Args:
            year: Current simulation year
            agents: Dictionary of agent instances
            market_model: Market model instance
            
        Returns:
            Dictionary containing economic development metrics
        """
        # Base rural income improvement (percentage)
        base_income_improvement = {
            'north_america': 1.0,  # 1% annual improvement
            'europe': 0.8,  # 0.8% annual improvement
            'asia_pacific': 2.0,  # 2% annual improvement
            'latin_america': 1.5,  # 1.5% annual improvement
            'africa_middle_east': 2.5  # 2.5% annual improvement
        }
        
        # Base trade balance impact ($ millions)
        base_trade_impact = {
            'north_america': 500,  # $500M positive impact
            'europe': -200,  # $200M negative impact
            'asia_pacific': 300,  # $300M positive impact
            'latin_america': 400,  # $400M positive impact
            'africa_middle_east': -300  # $300M negative impact
        }
        
        # Adjust based on scenario
        scenario_factors = {
            'baseline': {'income': 1.0, 'trade': 1.0},
            'regulatory_harmonization': {'income': 1.1, 'trade': 1.2},
            'climate_crisis': {'income': 0.8, 'trade': 0.7},
            'tech_breakthrough': {'income': 1.2, 'trade': 1.3},
            'market_disruption': {'income': 0.9, 'trade': 0.8}
        }
        scenario_factor = scenario_factors.get(self.config.scenario, {'income': 1.0, 'trade': 1.0})
        
        # Calculate current metrics
        years_elapsed = year - self.config.start_year
        
        # Rural income improvement (compound annual growth)
        income_improvement = {}
        for region, base in base_income_improvement.items():
            annual_gain = base * scenario_factor['income'] / 100.0
            cumulative_gain = (1.0 + annual_gain) ** years_elapsed - 1.0
            income_improvement[region] = cumulative_gain * 100.0  # Convert back to percentage
        
        # Trade balance impact (growing over time)
        trade_impact = {}
        for region, base in base_trade_impact.items():
            annual_growth = 1.05  # 5% annual growth
            trade_impact[region] = base * (annual_growth ** years_elapsed) * scenario_factor['trade']
        
        # Economic development index (0-100 scale)
        # Starting from 55 in 2025, improving over time
        base_development_index = 55.0
        annual_improvement = 1.8  # 1.8 points per year
        development_index = min(100.0, base_development_index + 
                              annual_improvement * years_elapsed * scenario_factor['income'])
        
        return {
            'year': year,
            'rural_income_improvement_pct': income_improvement,
            'trade_balance_impact_millions': trade_impact,
            'economic_development_index': development_index
        }
    
    def get_all_metrics(self) -> Dict[str, List[Dict[str, Any]]]:
        """Get all collected metrics.
        
        Returns:
            Dictionary containing all metrics collections
        """
        return self.metrics
    
    def get_metric(self, metric_name: str) -> List[Dict[str, Any]]:
        """Get a specific metric collection.
        
        Args:
            metric_name: Name of the metric collection
            
        Returns:
            List of metric dictionaries for each year
        """
        return self.metrics.get(metric_name, [])