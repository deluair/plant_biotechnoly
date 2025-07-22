#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Simulation engine for the BIOSIMULATE project.

This module implements the core simulation engine that orchestrates the
interactions between agents, regulatory frameworks, technology pipelines,
and economic models over the simulation time period.
"""

import os
import logging
import inspect
import pandas as pd
import numpy as np
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime

from biosimulate.simulation.config import SimulationConfig
from biosimulate.agents.agent_factory import AgentFactory
from biosimulate.regulatory.framework import RegulatoryFramework
from biosimulate.technology.pipeline import TechnologyPipeline
from biosimulate.economic.market import MarketModel
from biosimulate.simulation.metrics import MetricsTracker
from biosimulate.simulation.events import EventManager


class SimulationEngine:
    """Core simulation engine for the BIOSIMULATE project.
    
    This class orchestrates the simulation by initializing all components,
    advancing the simulation time step by step, and collecting results.
    
    Attributes:
        config: Simulation configuration
        logger: Logger instance
        agents: Dictionary of agent instances by ID
        regulatory_framework: Regulatory framework instance
        technology_pipeline: Technology pipeline instance
        market_model: Market model instance
        metrics_tracker: Metrics tracker instance
        event_manager: Event manager instance
    """
    
    def __init__(self, config: SimulationConfig):
        """Initialize the simulation engine.
        
        Args:
            config: Simulation configuration
        """
        self.config = config
        self.logger = logging.getLogger(__name__)
        
        # Initialize simulation components
        self.agent_factory = AgentFactory(config)
        self.regulatory_framework = RegulatoryFramework(config)
        self.technology_pipeline = TechnologyPipeline(config)
        self.market_model = MarketModel(config)
        self.metrics_tracker = MetricsTracker(config)
        self.event_manager = EventManager(config)
        
        # Initialize agent population
        self.agents = {}
        self._initialize_agents()
        
        self.logger.info(f"Initialized simulation engine with {len(self.agents)} agents")
    
    def _initialize_agents(self):
        """Initialize the agent population for the simulation."""
        # Create research entities
        self._create_research_entities()
        
        # Create commercial players
        self._create_commercial_players()
        
        # Create regulatory bodies
        self._create_regulatory_bodies()
        
        # Create market participants
        self._create_market_participants()
    
    def _create_research_entities(self):
        """Create research entity agents."""
        # University research labs
        for i in range(50):  # 50 university labs
            agent = self.agent_factory.create_university_lab(
                funding_level=np.random.choice(['high', 'medium', 'low'], p=[0.2, 0.5, 0.3]),
                research_focus=np.random.choice(['crispr', 'synthetic_biology', 'breeding'])
            )
            self.agents[agent.id] = agent
        
        # Government research institutes
        for i in range(20):  # 20 government institutes
            agent = self.agent_factory.create_government_institute(
                country=np.random.choice(['usa', 'eu', 'china', 'brazil', 'india']),
                budget=np.random.uniform(10, 100)  # $10-100 million
            )
            self.agents[agent.id] = agent
        
        # Private R&D companies
        for i in range(30):  # 30 private R&D companies
            agent = self.agent_factory.create_private_rd_company(
                company_size=np.random.choice(['large', 'medium', 'small']),
                specialization=np.random.choice(['gene_editing', 'trait_development', 'diagnostics'])
            )
            self.agents[agent.id] = agent
    
    def _create_commercial_players(self):
        """Create commercial player agents."""
        # Agricultural biotechnology corporations
        # Tier 1: >$10B revenue
        for i in range(5):  # 5 Tier 1 corporations
            agent = self.agent_factory.create_biotech_corporation(
                tier=1,
                revenue=np.random.uniform(10, 30)  # $10-30 billion
            )
            self.agents[agent.id] = agent
        
        # Tier 2: $1-10B revenue
        for i in range(15):  # 15 Tier 2 corporations
            agent = self.agent_factory.create_biotech_corporation(
                tier=2,
                revenue=np.random.uniform(1, 10)  # $1-10 billion
            )
            self.agents[agent.id] = agent
        
        # Tier 3: $500M-1B revenue
        for i in range(25):  # 25 Tier 3 corporations
            agent = self.agent_factory.create_biotech_corporation(
                tier=3,
                revenue=np.random.uniform(0.5, 1)  # $500M-1B
            )
            self.agents[agent.id] = agent
        
        # Startup companies
        for i in range(100):  # 100 startups
            agent = self.agent_factory.create_startup(
                focus_area=np.random.choice(['crispr', 'synthetic_biology', 'breeding', 'digital']),
                funding=np.random.uniform(1, 50)  # $1-50 million
            )
            self.agents[agent.id] = agent
        
        # Traditional seed companies
        for i in range(50):  # 50 traditional seed companies
            agent = self.agent_factory.create_seed_company(
                company_size=np.random.choice(['large', 'medium', 'small']),
                market_focus=np.random.choice(['grain_crops', 'vegetable_crops', 'oilseed_crops', 'fiber_crops', 'specialty_crops'], size=np.random.randint(1, 4), replace=False).tolist()
            )
            self.agents[agent.id] = agent
    
    def _create_regulatory_bodies(self):
        """Create regulatory body agents."""
        # Regional regulatory agencies
        regions = [
            'usa_fda', 'usa_usda', 'usa_epa',  # US agencies
            'eu_efsa', 'eu_echa',  # EU agencies
            'china_moa', 'brazil_ctnbio', 'india_geac',  # Emerging market agencies
            'japan_maff', 'australia_ogtr'  # Other major markets
        ]
        
        for region in regions:
            agent = self.agent_factory.create_regulatory_agency(region=region)
            self.agents[agent.id] = agent
        
        # International harmonization bodies
        for body in ['codex_alimentarius', 'oecd', 'wto']:
            agent = self.agent_factory.create_harmonization_body(name=body)
            self.agents[agent.id] = agent
    
    def _create_market_participants(self):
        """Create market participant agents."""
        # Farmers (simplified - in reality would be thousands/millions)
        regions = ['north_america', 'europe', 'asia_pacific', 'latin_america', 'africa_middle_east']
        farm_sizes = ['large', 'medium', 'small']
        crop_types = ['staple', 'fruits_vegetables', 'specialty']
        
        for region in regions:
            for size in farm_sizes:
                for crop in crop_types:
                    # Number of farmer agents depends on region and size
                    count = self._get_farmer_count(region, size)
                    
                    for i in range(count):
                        agent = self.agent_factory.create_farmer(
                            region=region,
                            size=size,
                            crop_type=crop
                        )
                        self.agents[agent.id] = agent
        
        # Food processors and distributors
        for i in range(50):  # 50 food processors/distributors
            agent = self.agent_factory.create_food_processor(
                size=np.random.choice(['large', 'medium', 'small']),
                biotech_policy=np.random.choice(['accepts', 'avoids', 'case_by_case'])
            )
            self.agents[agent.id] = agent
        
        # Consumer segments (simplified representation)
        for region in regions:
            for attitude in ['positive', 'neutral', 'negative']:
                agent = self.agent_factory.create_consumer_segment(
                    region=region,
                    biotech_attitude=attitude,
                    size=self._get_consumer_segment_size(region, attitude)
                )
                self.agents[agent.id] = agent
    
    def _get_farmer_count(self, region: str, size: str) -> int:
        """Get the number of farmer agents to create for a given region and size.
        
        Args:
            region: Geographic region
            size: Farm size category
            
        Returns:
            Number of farmer agents to create
        """
        # These are simplified representations - real numbers would be much larger
        counts = {
            'north_america': {'large': 10, 'medium': 5, 'small': 3},
            'europe': {'large': 5, 'medium': 8, 'small': 5},
            'asia_pacific': {'large': 3, 'medium': 10, 'small': 15},
            'latin_america': {'large': 8, 'medium': 6, 'small': 4},
            'africa_middle_east': {'large': 2, 'medium': 5, 'small': 10}
        }
        return counts.get(region, {}).get(size, 5)
    
    def _get_consumer_segment_size(self, region: str, attitude: str) -> float:
        """Get the size (as percentage) of a consumer segment for a region and attitude.
        
        Args:
            region: Geographic region
            attitude: Attitude toward biotechnology
            
        Returns:
            Segment size as a percentage (0-1)
        """
        # These represent the percentage of consumers in each attitude category
        sizes = {
            'north_america': {'positive': 0.4, 'neutral': 0.4, 'negative': 0.2},
            'europe': {'positive': 0.2, 'neutral': 0.3, 'negative': 0.5},
            'asia_pacific': {'positive': 0.3, 'neutral': 0.5, 'negative': 0.2},
            'latin_america': {'positive': 0.5, 'neutral': 0.3, 'negative': 0.2},
            'africa_middle_east': {'positive': 0.4, 'neutral': 0.4, 'negative': 0.2}
        }
        return sizes.get(region, {}).get(attitude, 0.33)
    
    def run(self) -> Dict[str, Any]:
        """Run the simulation from start_year to end_year.

        Returns:
            Dictionary containing simulation results
        """
        self.logger.info(f"Starting simulation run from {self.config.start_year} to {self.config.end_year}")

        self.results = {
            'annual_market_metrics': {},
            'agent_states': {}
        }

        for year in range(self.config.start_year, self.config.end_year + 1):
            self.logger.info(f"Simulating year {year}")

            # Process scheduled events for this year
            self.event_manager.process_events(year)

            # Update technology pipeline
            self.technology_pipeline.advance_year(year, self.agents)

            # Process regulatory decisions
            self.regulatory_framework.process_year(year, self.agents, self.technology_pipeline)

            # Update market conditions
            market_metrics = self.market_model.simulate_market_for_year(
                year, self.agents, self.technology_pipeline, self.regulatory_framework
            )
            self.results['annual_market_metrics'][year] = market_metrics

            # Update agent states
            for agent_id, agent in self.agents.items():
                # Dynamically call step method with correct arguments
                all_possible_args = {
                    'year': year,
                    'agents': self.agents,
                    'technology_pipeline': self.technology_pipeline,
                    'regulatory_framework': self.regulatory_framework,
                    'market_model': self.market_model,
                    'context': {  # For agents expecting a generic context dict
                        'agents': self.agents,
                        'technology_pipeline': self.technology_pipeline,
                        'regulatory_framework': self.regulatory_framework,
                        'market_model': self.market_model
                    }
                }

                try:
                    step_method = agent.step
                    sig = inspect.signature(step_method)
                    params_to_pass = {}
                    for param in sig.parameters:
                        if param in all_possible_args:
                            params_to_pass[param] = all_possible_args[param]
                    
                    step_method(**params_to_pass)

                except Exception as e:
                    self.logger.error(f"Error stepping agent {agent.id} ({agent.name}): {e}")
                    # Optionally, re-raise or handle more gracefully
                    raise e

            # Collect metrics
            self.metrics_tracker.record_year(year, self.agents, self.technology_pipeline,
                                             self.regulatory_framework, self.market_model)

        self.logger.info("Simulation run finished")

        # Process results into a DataFrame
        results_df = self._process_results_to_dataframe()
        self.results['dataframe'] = results_df

        if self.config.output_dir:
            self.save_results()

        return self.results

    def _process_results_to_dataframe(self) -> pd.DataFrame:
        """Process simulation results into a pandas DataFrame.

        Returns:
            A DataFrame with the simulation results.
        """
        processed_records = []
        for year, yearly_data in self.results.get('annual_market_metrics', {}).items():
            for product_id, sales in yearly_data.get('product_sales', {}).items():
                record = {
                    'year': year,
                    'product_id': product_id,
                    'total_sales': sales,
                }
                # Add regional sales
                for region, regional_sales_val in yearly_data.get('regional_sales', {}).items():
                    record[f'sales_{region}'] = self.market_model.market_data.get('annual_sales', {}).get(product_id, {}).get(year, {}).get(region, 0)

                # Add price
                avg_price = yearly_data.get('average_price', 0)
                record['average_price'] = avg_price

                processed_records.append(record)

        if not processed_records:
            return pd.DataFrame()

        return pd.DataFrame(processed_records)

    def save_results(self) -> None:
        """Save simulation results to output files."""
        if not self.results or 'dataframe' not in self.results:
            self.logger.warning("No results to save.")
            return

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = os.path.join(
            self.config.output_dir,
            f"{self.config.scenario}_{timestamp}.csv"
        )

        try:
            self.results['dataframe'].to_csv(output_file, index=False)
            self.logger.info(f"Successfully saved results to {output_file}")
        except Exception as e:
            self.logger.error(f"Failed to save results to {output_file}: {e}")