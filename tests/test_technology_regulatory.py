#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Test script for the BIOSIMULATE technology and regulatory components.

This module contains tests for the technology and regulatory-related components,
including TechnologyPipeline, RegulatoryFramework, and related functionality.
"""

import unittest
import os
import sys
import tempfile
import shutil
from typing import Dict, List, Any

# Add the parent directory to the path so we can import the biosimulate package
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Import the necessary modules
from biosimulate.technology.pipeline import TechnologyPipeline
from biosimulate.technology.innovation import InnovationModel
from biosimulate.regulatory.framework import RegulatoryFramework
from biosimulate.regulatory.approval import ApprovalProcess
from biosimulate.simulation.config import SimulationConfig


# class TestTechnologyPipeline(unittest.TestCase):
#     """Test cases for the TechnologyPipeline class."""

#     def setUp(self):
#         """Set up test fixtures."""
#         self.temp_dir = tempfile.mkdtemp()
#         self.config = SimulationConfig(
#             start_year=2020,
#             end_year=2030,
#             scenario="baseline",
#             output_dir=self.temp_dir,
#             seed=42
#         )
#         self.technology_pipeline = TechnologyPipeline(self.config)

#     def tearDown(self):
#         """Tear down test fixtures."""
#         shutil.rmtree(self.temp_dir)

#     def test_initialization(self):
#         """Test technology pipeline initialization."""
#         self.assertEqual(self.technology_pipeline.config, self.config)
#         self.assertIsNotNone(self.technology_pipeline.innovation_model)
#         self.assertIsNotNone(self.technology_pipeline.technologies)
#         self.assertIsNotNone(self.technology_pipeline.traits)
#         self.assertIsNotNone(self.technology_pipeline.development_stages)

#     def test_register_technology(self):
#         """Test registering a technology in the pipeline."""
#         # Create a test technology
#         technology = {
#             "id": "tech_123",
#             "name": "CRISPR-Cas9 Gene Editing",
#             "category": "gene_editing",
#             "description": "Precise gene editing technology",
#             "maturity": 0.7,
#             "development_cost": 10000000,
            #             "success_rate": 0.65,
#             "traits_enabled": ["yield", "drought_resistance", "pest_resistance"],
            #             "developer_id": "research_entity_456",
#             "patent_status": "patented",
            #             "patent_expiry": 2035,
#             "discovery_year": 2015
#         }
#         
#         # Register the technology
#         result = self.technology_pipeline.register_technology(technology)
#         
#         # Check that the technology was registered
#         self.assertTrue(result["success"])
#         self.assertIn(technology["id"], self.technology_pipeline.technologies)
#         self.assertEqual(self.technology_pipeline.technologies[technology["id"]], technology)

#     def test_register_trait(self):
#         """Test registering a trait in the pipeline."""
#         # Create a test trait
#         trait = {
#             "id": "trait_123",
#             "name": "High Yield",
#             "category": "agronomic",
#             "description": "Increases crop yield",
#             "complexity": 0.8,
            #             "development_cost": 5000000,
#             "market_value": 0.75,
            #             "sustainability_impact": 0.3,
#             "technologies_required": ["breeding", "gene_editing"],
            #             "developer_id": "commercial_player_456",
#             "patent_status": "patented",
            #             "patent_expiry": 2035,
#             "discovery_year": 2018
#         }
#         
#         # Register the trait
#         result = self.technology_pipeline.register_trait(trait)
#         
#         # Check that the trait was registered
#         self.assertTrue(result["success"])
#         self.assertIn(trait["id"], self.technology_pipeline.traits)
#         self.assertEqual(self.technology_pipeline.traits[trait["id"]], trait)

#     def test_advance_technology(self):
#         """Test advancing a technology's maturity."""
#         # Register a test technology
#         technology = {
#             "id": "tech_123",
#             "name": "CRISPR-Cas9 Gene Editing",
#             "category": "gene_editing",
            #             "maturity": 0.7,
#             "development_cost": 10000000,
            #             "success_rate": 0.65,
#             "traits_enabled": ["yield", "drought_resistance"],
            #             "developer_id": "research_entity_456",
#             "discovery_year": 2015
        #         }
#         self.technology_pipeline.register_technology(technology)
        
#         # Create advancement parameters
#         advancement_params = {
#             "investment": 2000000,
#             "research_capacity": 80,
#             "collaboration_level": 0.6,
#             "year": 2022
#         }
#         
#         # Advance the technology
#         result = self.technology_pipeline.advance_technology(
#             technology["id"], advancement_params
#         )
#         
#         # Check that the technology was advanced
#         self.assertTrue(result["success"])
#         self.assertGreater(
            #             self.technology_pipeline.technologies[technology["id"]]["maturity"],
#             technology["maturity"]
#         )

#     def test_develop_trait(self):
#         """Test developing a trait using available technologies."""
#         # Register a test technology
#         technology = {
#             "id": "tech_123",
#             "name": "CRISPR-Cas9 Gene Editing",
#             "category": "gene_editing",
#             "maturity": 0.9,  # High maturity
#             "development_cost": 10000000,
#             "success_rate": 0.8,  # High success rate
#             "traits_enabled": ["yield", "drought_resistance"],
#             "developer_id": "research_entity_456",
#             "discovery_year": 2015
#         }
#         self.technology_pipeline.register_technology(technology)
        
#         # Create a trait development request
#         trait_request = {
#             "name": "High Yield Trait",
#             "category": "agronomic",
#             "description": "Increases crop yield by 20%",
#             "target_trait": "yield",
#             "developer_id": "commercial_player_789",
#             "investment": 3000000,
#             "research_capacity": 75,
#             "year": 2022
#         }
#         
#         # Develop the trait
#         result = self.technology_pipeline.develop_trait(trait_request)
#         
#         # Check that the trait was developed
#         self.assertTrue(result["success"])
#         self.assertIn("trait_id", result)
#         self.assertIn(result["trait_id"], self.technology_pipeline.traits)

#     def test_update_pipeline(self):
#         """Test updating the technology pipeline for a year."""
#         # Register some test technologies and traits
#         technology = {
#             "id": "tech_123",
#             "name": "CRISPR-Cas9 Gene Editing",
#             "category": "gene_editing",
#             "maturity": 0.7,
#             "development_cost": 10000000,
#             "success_rate": 0.65,
#             "traits_enabled": ["yield", "drought_resistance"],
#             "developer_id": "research_entity_456",
#             "discovery_year": 2015
#         }
#         self.technology_pipeline.register_technology(technology)
#         
#         trait = {
#             "id": "trait_123",
#             "name": "High Yield",
#             "category": "agronomic",
#             "description": "Increases crop yield",
#             "complexity": 0.8,
#             "development_cost": 5000000,
#             "market_value": 0.75,
#             "sustainability_impact": 0.3,
#             "technologies_required": ["gene_editing"],
#             "developer_id": "commercial_player_456",
#             "development_stage": "research",
#             "discovery_year": 2018
#         }
#         self.technology_pipeline.register_trait(trait)
#         
#         # Create a simplified context for testing
#         agents = {}
#         
#         # Update the pipeline for a year
#         update_results = self.technology_pipeline.update_pipeline(2022, agents)
#         
#         # Check that the pipeline was updated
#         self.assertIsInstance(update_results, dict)
#         self.assertIn("technologies_updated", update_results)
#         self.assertIn("traits_updated", update_results)
#         self.assertIn("new_technologies", update_results)
#         self.assertIn("new_traits", update_results)


class TestInnovationModel(unittest.TestCase):
    """Test cases for the InnovationModel class."""

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
        self.innovation_model = InnovationModel(self.config)

    def tearDown(self):
        """Tear down test fixtures."""
        shutil.rmtree(self.temp_dir)

    def test_initialization(self):
        """Test innovation model initialization."""
        self.assertEqual(self.innovation_model.config, self.config)
        self.assertIsNotNone(self.innovation_model.params)
        self.assertIn("crispr_success_rate", self.innovation_model.params)
        self.assertIn("trait_development_time", self.innovation_model.params)

    def test_calculate_research_output(self):
        """Test calculating research output based on inputs."""
        # Create research inputs
        research_inputs = {
            "research_capacity": 80,
            "funding": 2000000,
            "collaboration_level": 0.7,
            "focus_areas": ["gene_editing", "breeding"],
            "existing_knowledge": 0.6
        }
        
        # Calculate research output
        output = self.innovation_model.calculate_research_output(research_inputs)
        
        # Check that research output was calculated
        self.assertIsInstance(output, dict)
        self.assertIn("knowledge_gain", output)
        self.assertIn("discovery_probability", output)
        self.assertIn("potential_technologies", output)
        
        # Check that higher inputs lead to higher outputs
        high_inputs = {**research_inputs, "research_capacity": 95, "funding": 3000000}
        high_output = self.innovation_model.calculate_research_output(high_inputs)
        self.assertGreater(high_output["knowledge_gain"], output["knowledge_gain"])
        self.assertGreater(high_output["discovery_probability"], output["discovery_probability"])

    def test_simulate_discovery(self):
        """Test simulating technology discovery."""
        # Create discovery parameters
        discovery_params = {
            "research_entity_id": "university_123",
            "research_focus": ["gene_editing", "breeding"],
            "discovery_probability": 0.8,  # High probability for testing
            "year": 2022
        }
        
        # Simulate discovery
        discovery_result = self.innovation_model.simulate_discovery(discovery_params)
        
        # Check that discovery was simulated
        self.assertIsInstance(discovery_result, dict)
        self.assertIn("discovery_made", discovery_result)
        
        # With high probability, a discovery should be made
        self.assertTrue(discovery_result["discovery_made"])
        self.assertIn("technology", discovery_result)
        self.assertIsInstance(discovery_result["technology"], dict)

    def test_calculate_development_success(self):
        """Test calculating development success probability."""
        # Create development parameters
        development_params = {
            "technology_maturity": 0.8,
            "trait_complexity": 0.7,
            "research_capacity": 75,
            "investment": 2000000,
            "technology_category": "gene_editing"
        }
        
        # Calculate success probability
        success_prob = self.innovation_model.calculate_development_success(development_params)
        
        # Check that a valid probability was calculated
        self.assertGreaterEqual(success_prob, 0.0)
        self.assertLessEqual(success_prob, 1.0)
        
        # Check that higher maturity leads to higher success probability
        high_maturity_params = {**development_params, "technology_maturity": 0.95}
        high_maturity_prob = self.innovation_model.calculate_development_success(high_maturity_params)
        self.assertGreater(high_maturity_prob, success_prob)
        
        # Check that higher complexity leads to lower success probability
        high_complexity_params = {**development_params, "trait_complexity": 0.9}
        high_complexity_prob = self.innovation_model.calculate_development_success(high_complexity_params)
        self.assertLess(high_complexity_prob, success_prob)


class TestRegulatoryFramework(unittest.TestCase):
    """Test cases for the RegulatoryFramework class."""

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
        self.regulatory_framework = RegulatoryFramework(self.config)

    def tearDown(self):
        """Tear down test fixtures."""
        shutil.rmtree(self.temp_dir)

    def test_initialization(self):
        """Test regulatory framework initialization."""
        self.assertEqual(self.regulatory_framework.config, self.config)
        self.assertIsNotNone(self.regulatory_framework.approval_process)
        self.assertIsNotNone(self.regulatory_framework.regulations)
        self.assertIsNotNone(self.regulatory_framework.regional_frameworks)
        self.assertIsNotNone(self.regulatory_framework.approval_history)

    def test_register_application(self):
        """Test registering a regulatory application."""
        # Create a test application
        application = {
            "id": "app_123",
            "product_id": "product_456",
            "company_id": "company_789",
            "technology": "crispr",
            "traits": ["yield", "drought_resistance"],
            "target_regions": ["north_america", "europe"],
            "submission_date": "2022-03-15",
            "data_package": {
                "safety_studies": 0.85,
                "efficacy_data": 0.9,
                "environmental_assessment": 0.75
            }
        }
        
        # Register the application
        result = self.regulatory_framework.register_application(application)
        
        # Check that the application was registered
        self.assertTrue(result["success"])
        self.assertIn(application["id"], self.regulatory_framework.applications)
        self.assertEqual(self.regulatory_framework.applications[application["id"]], application)

    def test_process_applications(self):
        """Test processing regulatory applications."""
        # Register some test applications
        applications = [
            {
                "id": "app_1",
                "product_id": "product_1",
                "company_id": "company_1",
                "technology": "crispr",
                "traits": ["yield"],
                "target_regions": ["north_america"],
                "submission_date": "2021-01-15",
                "data_package": {
                    "safety_studies": 0.9,
                    "efficacy_data": 0.95,
                    "environmental_assessment": 0.85
                },
                "status": "pending"
            },
            {
                "id": "app_2",
                "product_id": "product_2",
                "company_id": "company_2",
                "technology": "breeding",
                "traits": ["pest_resistance"],
                "target_regions": ["europe"],
                "submission_date": "2021-02-20",
                "data_package": {
                    "safety_studies": 0.8,
                    "efficacy_data": 0.85,
                    "environmental_assessment": 0.7
                },
                "status": "pending"
            }
        ]
        
        for app in applications:
            self.regulatory_framework.register_application(app)
        
        # Create a simplified context for testing
        agents = {}
        
        # Process the applications
        processing_results = self.regulatory_framework.process_applications(2022, agents)
        
        # Check that applications were processed
        self.assertIsInstance(processing_results, dict)
        self.assertIn("applications_processed", processing_results)
        self.assertIn("approvals", processing_results)
        self.assertIn("rejections", processing_results)
        
        # Check that application statuses were updated
        for app_id in self.regulatory_framework.applications:
            self.assertNotEqual(self.regulatory_framework.applications[app_id]["status"], "pending")

    def test_update_regulations(self):
        """Test updating regulations based on events and policy changes."""
        # Create a policy change event
        policy_event = {
            "type": "policy_change",
            "region": "europe",
            "policy_area": "gene_editing",
            "direction": "more_permissive",
            "magnitude": 0.3,
            "year": 2022
        }
        
        # Record initial regulatory stringency
        initial_stringency = self.regulatory_framework.regional_frameworks["europe"]["stringency"]
        
        # Update regulations based on the event
        update_result = self.regulatory_framework.update_regulations([policy_event])
        
        # Check that regulations were updated
        self.assertTrue(update_result["success"])
        self.assertIn("regulations_updated", update_result)
        
        # Check that stringency was reduced (more permissive)
        current_stringency = self.regulatory_framework.regional_frameworks["europe"]["stringency"]
        self.assertLess(current_stringency, initial_stringency)

    def test_calculate_approval_time(self):
        """Test calculating approval time for an application."""
        # Create a test application
        application = {
            "id": "app_123",
            "product_id": "product_456",
            "company_id": "company_789",
            "technology": "crispr",
            "traits": ["yield", "drought_resistance"],
            "target_regions": ["north_america"],
            "submission_date": "2022-03-15",
            "data_package": {
                "safety_studies": 0.85,
                "efficacy_data": 0.9,
                "environmental_assessment": 0.75
            }
        }
        
        # Calculate approval time
        approval_time = self.regulatory_framework.approval_process.calculate_approval_time(
            application, "north_america", self.regulatory_framework.regional_frameworks
        )
        
        # Check that a reasonable approval time was calculated
        self.assertGreater(approval_time, 0)
        
        # Check that a more complex application takes longer
        complex_application = {**application, "traits": ["yield", "drought_resistance", "pest_resistance", "herbicide_tolerance"]}
        complex_time = self.regulatory_framework.approval_process.calculate_approval_time(
            complex_application, "north_america", self.regulatory_framework.regional_frameworks
        )
        self.assertGreater(complex_time, approval_time)


class TestApprovalProcess(unittest.TestCase):
    """Test cases for the ApprovalProcess class."""

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
        self.approval_process = ApprovalProcess(self.config)

    def tearDown(self):
        """Tear down test fixtures."""
        shutil.rmtree(self.temp_dir)

    def test_initialization(self):
        """Test approval process initialization."""
        self.assertEqual(self.approval_process.config, self.config)
        self.assertIsNotNone(self.approval_process.params)
        self.assertIn("approval_time_mean", self.approval_process.params)
        self.assertIn("approval_time_std", self.approval_process.params)

    def test_evaluate_application(self):
        """Test evaluating a regulatory application."""
        # Create a test application
        application = {
            "id": "app_123",
            "product_id": "product_456",
            "company_id": "company_789",
            "technology": "crispr",
            "traits": ["yield", "drought_resistance"],
            "target_regions": ["north_america"],
            "submission_date": "2022-03-15",
            "data_package": {
                "safety_studies": 0.85,
                "efficacy_data": 0.9,
                "environmental_assessment": 0.75
            }
        }
        
        # Create regional frameworks for testing
        regional_frameworks = {
            "north_america": {
                "stringency": 0.7,
                "technology_restrictions": {"crispr": 0.5},
                "data_requirements": {
                    "safety": 0.8,
                    "efficacy": 0.7,
                    "environmental": 0.75
                }
            }
        }
        
        # Evaluate the application
        evaluation = self.approval_process.evaluate_application(
            application, "north_america", regional_frameworks
        )
        
        # Check that the application was evaluated
        self.assertIsInstance(evaluation, dict)
        self.assertIn("approval_probability", evaluation)
        self.assertIn("approval_time", evaluation)
        self.assertIn("requirements_met", evaluation)
        
        # Check that a high-quality application has a good chance of approval
        self.assertGreater(evaluation["approval_probability"], 0.5)
        
        # Check that a low-quality application has a lower chance of approval
        low_quality_app = {**application, "data_package": {
            "safety_studies": 0.5,
            "efficacy_data": 0.6,
            "environmental_assessment": 0.4
        }}
        low_quality_eval = self.approval_process.evaluate_application(
            low_quality_app, "north_america", regional_frameworks
        )
        self.assertLess(low_quality_eval["approval_probability"], evaluation["approval_probability"])

    def test_simulate_approval_decision(self):
        """Test simulating an approval decision."""
        # Create evaluation results
        evaluation = {
            "approval_probability": 0.8,  # High probability for testing
            "approval_time": 18,
            "requirements_met": True,
            "evaluation_details": {
                "safety_score": 0.85,
                "efficacy_score": 0.9,
                "environmental_score": 0.75
            }
        }
        
        # Simulate decision
        decision = self.approval_process.simulate_approval_decision(evaluation, 2022)
        
        # Check that a decision was made
        self.assertIsInstance(decision, dict)
        self.assertIn("approved", decision)
        self.assertIn("decision_date", decision)
        self.assertIn("decision_details", decision)
        
        # With high probability, the application should be approved
        self.assertTrue(decision["approved"])
        
        # Check that a low probability leads to rejection
        low_prob_eval = {**evaluation, "approval_probability": 0.1}
        low_prob_decision = self.approval_process.simulate_approval_decision(low_prob_eval, 2022)
        self.assertFalse(low_prob_decision["approved"])


if __name__ == "__main__":
    unittest.main()