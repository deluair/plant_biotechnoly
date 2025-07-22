#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Test script for the BIOSIMULATE simulation engine.

This module contains tests for the simulation engine and related components,
including SimulationConfig, SimulationEngine, and MetricsTracker.
"""

import unittest
import os
import sys
import tempfile
import shutil
import json
from pathlib import Path
from typing import Dict, List, Any

# Add the parent directory to the path so we can import the biosimulate package
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from biosimulate.simulation.config import SimulationConfig
from biosimulate.simulation.engine import SimulationEngine
from biosimulate.simulation.metrics import MetricsTracker
from biosimulate.agents.agent_factory import create_agent


class TestSimulationConfig(unittest.TestCase):
    """Test cases for the SimulationConfig class."""

    def setUp(self):
        """Set up test fixtures."""
        self.temp_dir = tempfile.mkdtemp()
        self.config = SimulationConfig(
            start_year=2020,
            end_year=2030,
            scenario="baseline",
            output_dir=self.temp_dir,
            seed=42
        )

    def tearDown(self):
        """Tear down test fixtures."""
        shutil.rmtree(self.temp_dir)

    def test_initialization(self):
        """Test simulation config initialization."""
        self.assertEqual(self.config.start_year, 2020)
        self.assertEqual(self.config.end_year, 2030)
        self.assertEqual(self.config.scenario, "baseline")
        self.assertEqual(self.config.output_dir, self.temp_dir)
        self.assertEqual(self.config.seed, 42)

    def test_scenario_params_baseline(self):
        """Test baseline scenario parameters."""
        # Check that baseline parameters were loaded
        self.assertIsNotNone(self.config.params)
        self.assertIn("market", self.config.params)
        self.assertIn("technology", self.config.params)
        self.assertIn("regulatory", self.config.params)
        self.assertIn("economic", self.config.params)
        self.assertIn("adoption", self.config.params)

    def test_scenario_params_regulatory_harmonization(self):
        """Test regulatory harmonization scenario parameters."""
        config = SimulationConfig(
            start_year=2020,
            end_year=2030,
            scenario="regulatory_harmonization",
            output_dir=self.temp_dir,
            seed=42
        )
        
        # Check that regulatory parameters were adjusted
        self.assertLess(
            config.params["regulatory"]["approval_time_mean"],
            self.config.params["regulatory"]["approval_time_mean"]
        )
        self.assertGreater(
            config.params["regulatory"]["harmonization_level"],
            self.config.params["regulatory"]["harmonization_level"]
        )

    def test_scenario_params_climate_crisis(self):
        """Test climate crisis scenario parameters."""
        config = SimulationConfig(
            start_year=2020,
            end_year=2030,
            scenario="climate_crisis",
            output_dir=self.temp_dir,
            seed=42
        )
        
        # Check that climate crisis parameters were adjusted
        self.assertGreater(
            config.params["market"]["growth_rate"],
            self.config.params["market"]["growth_rate"]
        )
        self.assertGreater(
            config.params["adoption"]["sustainability_weight"],
            self.config.params["adoption"]["sustainability_weight"]
        )

    def test_save_and_load(self):
        """Test saving and loading configuration."""
        config_path = os.path.join(self.temp_dir, "config.json")
        
        # Save the configuration
        self.config.save(config_path)
        
        # Check that the file was created
        self.assertTrue(os.path.exists(config_path))
        
        # Load the configuration
        loaded_config = SimulationConfig.load(config_path)
        
        # Check that the loaded configuration matches the original
        self.assertEqual(loaded_config.start_year, self.config.start_year)
        self.assertEqual(loaded_config.end_year, self.config.end_year)
        self.assertEqual(loaded_config.scenario, self.config.scenario)
        self.assertEqual(loaded_config.seed, self.config.seed)


class TestSimulationEngine(unittest.TestCase):
    """Test cases for the SimulationEngine class."""

    def setUp(self):
        """Set up test fixtures."""
        self.temp_dir = tempfile.mkdtemp()
        self.config = SimulationConfig(
            start_year=2020,
            end_year=2022,  # Short simulation for testing
            scenario="baseline",
            output_dir=self.temp_dir,
            seed=42
        )
        self.engine = SimulationEngine(self.config)

    def tearDown(self):
        """Tear down test fixtures."""
        shutil.rmtree(self.temp_dir)

    def test_initialization(self):
        """Test simulation engine initialization."""
        self.assertEqual(self.engine.config, self.config)
        self.assertEqual(self.engine.current_year, self.config.start_year)
        self.assertIsNotNone(self.engine.agent_factory)
        self.assertIsNotNone(self.engine.regulatory_framework)
        self.assertIsNotNone(self.engine.technology_pipeline)
        self.assertIsNotNone(self.engine.market_model)
        self.assertIsNotNone(self.engine.metrics_tracker)
        self.assertIsNotNone(self.engine.event_manager)

    def test_initialize_simulation(self):
        """Test simulation initialization."""
        self.engine.initialize_simulation()
        
        # Check that agents were created
        self.assertGreater(len(self.engine.agents), 0)
        
        # Check that different types of agents were created
        agent_types = set(agent.type for agent in self.engine.agents.values())
        self.assertIn("research_entity", agent_types)
        self.assertIn("commercial_player", agent_types)
        self.assertIn("regulatory_body", agent_types)
        self.assertIn("market_participant", agent_types)

    def test_create_research_entities(self):
        """Test creation of research entities."""
        self.engine._create_research_entities()
        
        # Check that research entities were created
        research_entities = [agent for agent in self.engine.agents.values() 
                            if agent.type == "research_entity"]
        self.assertGreater(len(research_entities), 0)
        
        # Check that different types of research entities were created
        research_entity_names = [entity.name for entity in research_entities]
        self.assertTrue(any("University" in name for name in research_entity_names))
        self.assertTrue(any("Institute" in name for name in research_entity_names))

    def test_create_commercial_players(self):
        """Test creation of commercial players."""
        self.engine._create_commercial_players()
        
        # Check that commercial players were created
        commercial_players = [agent for agent in self.engine.agents.values() 
                             if agent.type == "commercial_player"]
        self.assertGreater(len(commercial_players), 0)
        
        # Check that different types of commercial players were created
        player_types = set(player.attributes.get("company_type") for player in commercial_players)
        self.assertIn("biotech_corporation", player_types)
        self.assertIn("startup", player_types)
        self.assertIn("seed_company", player_types)

    def test_create_regulatory_bodies(self):
        """Test creation of regulatory bodies."""
        self.engine._create_regulatory_bodies()
        
        # Check that regulatory bodies were created
        regulatory_bodies = [agent for agent in self.engine.agents.values() 
                            if agent.type == "regulatory_body"]
        self.assertGreater(len(regulatory_bodies), 0)
        
        # Check that different regions have regulatory bodies
        regions = set(body.region for body in regulatory_bodies)
        self.assertGreaterEqual(len(regions), 3)  # At least 3 different regions

    def test_create_market_participants(self):
        """Test creation of market participants."""
        self.engine._create_market_participants()
        
        # Check that market participants were created
        market_participants = [agent for agent in self.engine.agents.values() 
                              if agent.type == "market_participant"]
        self.assertGreater(len(market_participants), 0)
        
        # Check that different types of market participants were created
        participant_types = set(participant.attributes.get("participant_type") 
                               for participant in market_participants)
        self.assertIn("farmer", participant_types)
        self.assertIn("food_processor", participant_types)
        self.assertIn("consumer", participant_types)

    def test_run_simulation(self):
        """Test running a short simulation."""
        # Initialize and run the simulation
        self.engine.initialize_simulation()
        self.engine.run()
        
        # Check that the simulation ran to completion
        self.assertEqual(self.engine.current_year, self.config.end_year + 1)
        
        # Check that metrics were collected
        self.assertGreater(len(self.engine.metrics_tracker.innovation_metrics), 0)
        self.assertGreater(len(self.engine.metrics_tracker.market_metrics), 0)
        self.assertGreater(len(self.engine.metrics_tracker.societal_metrics), 0)

    def test_save_results(self):
        """Test saving simulation results."""
        # Initialize and run the simulation
        self.engine.initialize_simulation()
        self.engine.run()
        
        # Save the results
        self.engine.save_results()
        
        # Check that result files were created
        results_dir = Path(self.config.output_dir) / "results"
        self.assertTrue(results_dir.exists())
        
        expected_files = [
            "market_size.csv",
            "technology_metrics.csv",
            "regulatory_metrics.csv",
            "economic_metrics.csv",
            "detailed_metrics.csv"
        ]
        
        for file_name in expected_files:
            self.assertTrue((results_dir / file_name).exists())


class TestMetricsTracker(unittest.TestCase):
    """Test cases for the MetricsTracker class."""

    def setUp(self):
        """Set up test fixtures."""
        self.metrics_tracker = MetricsTracker(scenario="baseline")

    def test_initialization(self):
        """Test metrics tracker initialization."""
        self.assertEqual(self.metrics_tracker.scenario, "baseline")
        self.assertEqual(len(self.metrics_tracker.innovation_metrics), 0)
        self.assertEqual(len(self.metrics_tracker.market_metrics), 0)
        self.assertEqual(len(self.metrics_tracker.societal_metrics), 0)

    def test_record_yearly_metrics(self):
        """Test recording yearly metrics."""
        # Create a simplified context for testing
        agents = {}
        technology_pipeline = None
        regulatory_framework = None
        market_model = None
        
        # Record metrics for a year
        self.metrics_tracker.record_yearly_metrics(
            year=2025,
            agents=agents,
            technology_pipeline=technology_pipeline,
            regulatory_framework=regulatory_framework,
            market_model=market_model
        )
        
        # Check that metrics were recorded
        self.assertEqual(len(self.metrics_tracker.innovation_metrics), 1)
        self.assertEqual(len(self.metrics_tracker.market_metrics), 1)
        self.assertEqual(len(self.metrics_tracker.societal_metrics), 1)
        
        # Check that the year was recorded correctly
        self.assertEqual(self.metrics_tracker.innovation_metrics[0]["year"], 2025)
        self.assertEqual(self.metrics_tracker.market_metrics[0]["year"], 2025)
        self.assertEqual(self.metrics_tracker.societal_metrics[0]["year"], 2025)

    def test_collect_patent_data(self):
        """Test collecting patent data."""
        # Collect patent data for a year
        patent_data = self.metrics_tracker._collect_patent_data(
            year=2025,
            scenario="baseline"
        )
        
        # Check that patent data was generated
        self.assertIsInstance(patent_data, dict)
        self.assertIn("total_patents", patent_data)
        self.assertIn("by_category", patent_data)
        self.assertIn("by_region", patent_data)


if __name__ == "__main__":
    unittest.main()