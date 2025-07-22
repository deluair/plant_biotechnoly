#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Test script for the BIOSIMULATE project.

This module contains tests for the core components of the simulation,
including agent creation, simulation engine functionality, and metrics tracking.
"""

import unittest
import os
import sys
import logging
from typing import Dict, List, Any

# Add the parent directory to the path so we can import the biosimulate package
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from biosimulate.simulation.config import SimulationConfig
from biosimulate.agents.agent_factory import (
    create_agent, create_research_entity, create_commercial_player,
    create_regulatory_body, create_market_participant
)
from biosimulate.agents.base_agent import BaseAgent
from biosimulate.agents.research_entity import ResearchEntity
from biosimulate.agents.commercial_player import CommercialPlayer
from biosimulate.agents.regulatory_body import RegulatoryBody
from biosimulate.agents.market_participant import MarketParticipant
from biosimulate.simulation.engine import SimulationEngine
from biosimulate.simulation.metrics import MetricsTracker


class TestAgentCreation(unittest.TestCase):
    """Test cases for agent creation functionality."""

    def test_create_research_entity(self):
        """Test creation of a research entity agent."""
        agent = create_research_entity(
            name="Test University",
            region="north_america",
            research_focus=["crispr", "breeding"],
            research_capacity=75,
            publication_rate=10.0,
            collaboration_tendency=65
        )
        
        self.assertIsInstance(agent, ResearchEntity)
        self.assertEqual(agent.name, "Test University")
        self.assertEqual(agent.region, "north_america")
        self.assertEqual(agent.research_focus, ["crispr", "breeding"])
        self.assertEqual(agent.research_capacity, 75)
        self.assertEqual(agent.publication_rate, 10.0)
        self.assertEqual(agent.collaboration_tendency, 65)

    def test_create_commercial_player(self):
        """Test creation of a commercial player agent."""
        agent = create_commercial_player(
            name="Biotech Corp",
            region="europe",
            company_size="large",
            market_segments=["crops", "seeds"],
            r_and_d_investment=0.15,
            innovation_capacity=80
        )
        
        self.assertIsInstance(agent, CommercialPlayer)
        self.assertEqual(agent.name, "Biotech Corp")
        self.assertEqual(agent.region, "europe")
        self.assertEqual(agent.company_size, "large")
        self.assertEqual(agent.market_segments, ["crops", "seeds"])
        self.assertEqual(agent.r_and_d_investment, 0.15)
        self.assertEqual(agent.innovation_capacity, 80)

    def test_create_regulatory_body(self):
        """Test creation of a regulatory body agent."""
        agent = create_regulatory_body(
            name="FDA",
            region="north_america",
            jurisdiction="usa",
            enforcement_capacity=85,
            transparency=75,
            risk_tolerance=40
        )
        
        self.assertIsInstance(agent, RegulatoryBody)
        self.assertEqual(agent.name, "FDA")
        self.assertEqual(agent.region, "north_america")
        self.assertEqual(agent.jurisdiction, "usa")
        self.assertEqual(agent.enforcement_capacity, 85)
        self.assertEqual(agent.transparency, 75)
        self.assertEqual(agent.risk_tolerance, 40)

    def test_create_market_participant(self):
        """Test creation of a market participant agent."""
        agent = create_market_participant(
            name="Farmer Group A",
            region="latin_america",
            participant_type="farmer",
            size="medium",
            market_segments=["grain_crops"],
            risk_aversion=60,
            price_sensitivity=70,
            innovation_openness=50
        )
        
        self.assertIsInstance(agent, MarketParticipant)
        self.assertEqual(agent.name, "Farmer Group A")
        self.assertEqual(agent.region, "latin_america")
        self.assertEqual(agent.participant_type, "farmer")
        self.assertEqual(agent.size, "medium")
        self.assertEqual(agent.market_segments, ["grain_crops"])
        self.assertEqual(agent.risk_aversion, 60)
        self.assertEqual(agent.price_sensitivity, 70)
        self.assertEqual(agent.innovation_openness, 50)

    def test_create_agent_generic(self):
        """Test the generic agent creation function."""
        agent = create_agent(
            agent_type="research_entity",
            name="Generic Research Lab",
            region="asia_pacific",
            research_focus=["synthetic_biology"],
            research_capacity=60
        )
        
        self.assertIsInstance(agent, ResearchEntity)
        self.assertEqual(agent.name, "Generic Research Lab")
        self.assertEqual(agent.region, "asia_pacific")
        self.assertEqual(agent.research_focus, ["synthetic_biology"])
        self.assertEqual(agent.research_capacity, 60)


class TestBaseAgentFunctionality(unittest.TestCase):
    """Test cases for base agent functionality."""

    def setUp(self):
        """Set up test fixtures."""
        self.agent = BaseAgent(
            name="Test Agent",
            type="test",
            region="test_region"
        )

    def test_agent_initialization(self):
        """Test agent initialization."""
        self.assertEqual(self.agent.name, "Test Agent")
        self.assertEqual(self.agent.type, "test")
        self.assertEqual(self.agent.region, "test_region")
        self.assertTrue(self.agent.is_active())

    def test_agent_connections(self):
        """Test agent connection management."""
        other_agent_id = "test_connection"
        
        # Test adding a connection
        self.agent.add_connection(other_agent_id)
        self.assertTrue(self.agent.has_connection(other_agent_id))
        
        # Test removing a connection
        self.agent.remove_connection(other_agent_id)
        self.assertFalse(self.agent.has_connection(other_agent_id))

    def test_agent_resources(self):
        """Test agent resource management."""
        # Test adding a resource
        self.agent.add_resource("money", 1000)
        self.assertEqual(self.agent.get_resource("money"), 1000)
        
        # Test adding more of the same resource
        self.agent.add_resource("money", 500)
        self.assertEqual(self.agent.get_resource("money"), 1500)
        
        # Test removing a resource
        removed = self.agent.remove_resource("money", 300)
        self.assertEqual(removed, 300)
        self.assertEqual(self.agent.get_resource("money"), 1200)
        
        # Test removing all of a resource
        removed = self.agent.remove_resource("money")
        self.assertEqual(removed, 1200)
        self.assertIsNone(self.agent.get_resource("money"))

    def test_agent_state(self):
        """Test agent state management."""
        # Test setting a state variable
        self.agent.set_state("test_state", "test_value")
        self.assertEqual(self.agent.get_state("test_state"), "test_value")
        
        # Test getting a non-existent state variable
        self.assertIsNone(self.agent.get_state("non_existent"))
        self.assertEqual(self.agent.get_state("non_existent", "default"), "default")
        
        # Test activation/deactivation
        self.agent.deactivate()
        self.assertFalse(self.agent.is_active())
        self.agent.activate()
        self.assertTrue(self.agent.is_active())

    def test_agent_history(self):
        """Test agent history recording."""
        # Simulate a step to record history
        actions = {"test_action": "test_value"}
        self.agent._record_history(2025, actions)
        
        # Check that history was recorded
        self.assertEqual(len(self.agent.history), 1)
        self.assertEqual(self.agent.history[0]["year"], 2025)
        self.assertEqual(self.agent.history[0]["actions"], actions)

    def test_agent_serialization(self):
        """Test agent serialization to and from dictionary."""
        # Add some test data
        self.agent.add_connection("test_connection")
        self.agent.add_resource("test_resource", 100)
        self.agent.set_state("test_state", "test_value")
        
        # Convert to dictionary
        agent_dict = self.agent.to_dict()
        
        # Check dictionary values
        self.assertEqual(agent_dict["name"], "Test Agent")
        self.assertEqual(agent_dict["type"], "test")
        self.assertEqual(agent_dict["region"], "test_region")
        self.assertEqual(agent_dict["resources"]["test_resource"], 100)
        self.assertEqual(agent_dict["state"]["test_state"], "test_value")
        self.assertIn("test_connection", agent_dict["connections"])
        
        # Convert back to agent
        new_agent = BaseAgent.from_dict(agent_dict)
        
        # Check new agent values
        self.assertEqual(new_agent.name, "Test Agent")
        self.assertEqual(new_agent.type, "test")
        self.assertEqual(new_agent.region, "test_region")
        self.assertEqual(new_agent.get_resource("test_resource"), 100)
        self.assertEqual(new_agent.get_state("test_state"), "test_value")
        self.assertTrue(new_agent.has_connection("test_connection"))


class TestSimulationConfig(unittest.TestCase):
    """Test cases for simulation configuration."""

    def test_default_config(self):
        """Test default configuration."""
        config = SimulationConfig()
        
        self.assertEqual(config.start_year, 2025)
        self.assertEqual(config.end_year, 2035)
        self.assertEqual(config.scenario, "baseline")
        self.assertIn("market_growth_rate", config.params)
        self.assertIn("market_size_2025", config.params)

    def test_custom_config(self):
        """Test custom configuration."""
        config = SimulationConfig(
            start_year=2026,
            end_year=2036,
            scenario="tech_breakthrough",
            seed=42
        )
        
        self.assertEqual(config.start_year, 2026)
        self.assertEqual(config.end_year, 2036)
        self.assertEqual(config.scenario, "tech_breakthrough")
        self.assertEqual(config.seed, 42)
        
        # Check that scenario-specific parameters were loaded
        self.assertGreater(config.params["crispr_success_rate"], 0.25)  # Should be higher in tech_breakthrough


class TestMetricsTracker(unittest.TestCase):
    """Test cases for metrics tracking."""

    def setUp(self):
        """Set up test fixtures."""
        self.config = SimulationConfig()
        self.metrics_tracker = MetricsTracker(self.config)

    def test_metrics_initialization(self):
        """Test metrics tracker initialization."""
        self.assertIn("patent_filings", self.metrics_tracker.metrics)
        self.assertIn("research_collaborations", self.metrics_tracker.metrics)
        self.assertIn("time_to_market", self.metrics_tracker.metrics)
        self.assertIn("technology_adoption", self.metrics_tracker.metrics)
        self.assertIn("market_concentration", self.metrics_tracker.metrics)
        self.assertIn("price_premiums", self.metrics_tracker.metrics)
        self.assertIn("food_security", self.metrics_tracker.metrics)
        self.assertIn("environmental_impact", self.metrics_tracker.metrics)
        self.assertIn("economic_development", self.metrics_tracker.metrics)


class TestSimulationEngine(unittest.TestCase):
    """Test cases for simulation engine."""

    @unittest.skip("Requires full implementation of dependent components")
    def test_simulation_initialization(self):
        """Test simulation engine initialization."""
        config = SimulationConfig(
            start_year=2025,
            end_year=2026,  # Short simulation for testing
            scenario="baseline"
        )
        
        engine = SimulationEngine(config)
        
        # Check that components were initialized
        self.assertIsNotNone(engine.agent_factory)
        self.assertIsNotNone(engine.regulatory_framework)
        self.assertIsNotNone(engine.technology_pipeline)
        self.assertIsNotNone(engine.market_model)
        self.assertIsNotNone(engine.metrics_tracker)
        self.assertIsNotNone(engine.event_manager)
        
        # Check that agents were created
        self.assertGreater(len(engine.agents), 0)

    @unittest.skip("Requires full implementation of dependent components")
    def test_simulation_run(self):
        """Test running a simulation."""
        config = SimulationConfig(
            start_year=2025,
            end_year=2026,  # Short simulation for testing
            scenario="baseline"
        )
        
        engine = SimulationEngine(config)
        results = engine.run()
        
        # Check that results were generated
        self.assertEqual(len(results["years"]), 2)  # 2025 and 2026
        self.assertEqual(len(results["market_size"]), 2)
        self.assertEqual(len(results["technology_metrics"]), 2)
        self.assertEqual(len(results["regulatory_metrics"]), 2)
        self.assertEqual(len(results["economic_metrics"]), 2)
        self.assertEqual(len(results["agent_states"]), 2)


if __name__ == "__main__":
    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    
    # Run the tests
    unittest.main()