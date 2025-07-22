#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Test script for the BIOSIMULATE economic and market components.

This module contains tests for the economic and market-related components,
including MarketModel, EconomicModel, and related functionality.
"""

import unittest
import os
import sys
import tempfile
import shutil
from typing import Dict, List, Any

# Add the parent directory to the path so we can import the biosimulate package
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from biosimulate.economic.market_model import MarketModel
from biosimulate.economic.pricing import PricingModel
from biosimulate.economic.adoption import AdoptionModel
from biosimulate.simulation.config import SimulationConfig


class TestMarketModel(unittest.TestCase):
    """Test cases for the MarketModel class."""

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
        self.market_model = MarketModel(self.config)

    def tearDown(self):
        """Tear down test fixtures."""
        shutil.rmtree(self.temp_dir)

    def test_initialization(self):
        """Test market model initialization."""
        self.assertEqual(self.market_model.config, self.config)
        self.assertIsNotNone(self.market_model.pricing_model)
        self.assertIsNotNone(self.market_model.adoption_model)
        self.assertIsNotNone(self.market_model.market_segments)
        self.assertIsNotNone(self.market_model.market_size)
        self.assertIsNotNone(self.market_model.product_registry)

    def test_register_product(self):
        """Test registering a product in the market model."""
        # Create a test product
        product = {
            "id": "product_123",
            "name": "High-Yield Corn",
            "company_id": "company_456",
            "segment": "grain_crops",
            "technology": "crispr",
            "traits": ["yield", "drought_resistance"],
            "performance": 85,
            "price": 150,
            "development_cost": 5000000,
            "regulatory_status": "approved",
            "regions_approved": ["north_america", "europe"],
            "launch_year": 2022
        }
        
        # Register the product
        result = self.market_model.register_product(product)
        
        # Check that the product was registered
        self.assertTrue(result["success"])
        self.assertIn(product["id"], self.market_model.product_registry)
        self.assertEqual(self.market_model.product_registry[product["id"]], product)

    def test_update_market_size(self):
        """Test updating market size."""
        # Record initial market size
        initial_market_size = self.market_model.market_size.copy()
        
        # Update market size for a year
        self.market_model.update_market_size(2022)
        
        # Check that market size was updated
        for segment in self.market_model.market_segments:
            self.assertGreater(
                self.market_model.market_size[segment],
                initial_market_size[segment]
            )

    def test_calculate_market_shares(self):
        """Test calculating market shares."""
        # Register some test products
        products = [
            {
                "id": "product_1",
                "name": "High-Yield Corn",
                "company_id": "company_1",
                "segment": "grain_crops",
                "technology": "crispr",
                "traits": ["yield"],
                "performance": 85,
                "price": 150,
                "development_cost": 5000000,
                "regulatory_status": "approved",
                "regions_approved": ["north_america", "europe"],
                "launch_year": 2020,
                "sales": {"2020": 1000000, "2021": 1500000}
            },
            {
                "id": "product_2",
                "name": "Drought-Resistant Corn",
                "company_id": "company_2",
                "segment": "grain_crops",
                "technology": "breeding",
                "traits": ["drought_resistance"],
                "performance": 75,
                "price": 120,
                "development_cost": 3000000,
                "regulatory_status": "approved",
                "regions_approved": ["north_america", "latin_america"],
                "launch_year": 2020,
                "sales": {"2020": 800000, "2021": 1200000}
            }
        ]
        
        for product in products:
            self.market_model.register_product(product)
        
        # Calculate market shares
        market_shares = self.market_model.calculate_market_shares(2021)
        
        # Check that market shares were calculated
        self.assertIsInstance(market_shares, dict)
        self.assertIn("by_company", market_shares)
        self.assertIn("by_technology", market_shares)
        self.assertIn("by_segment", market_shares)
        
        # Check that market shares add up to approximately 1.0
        self.assertAlmostEqual(sum(market_shares["by_company"].values()), 1.0, places=1)
        self.assertAlmostEqual(sum(market_shares["by_technology"].values()), 1.0, places=1)
        self.assertAlmostEqual(sum(market_shares["by_segment"].values()), 1.0, places=1)

    def test_process_transactions(self):
        """Test processing market transactions."""
        # Create some test agents
        agents = {
            "seller_1": type("Agent", (), {
                "id": "seller_1",
                "type": "commercial_player",
                "resources": {"capital": 10000000},
                "add_resource": lambda resource, amount: setattr(
                    agents["seller_1"], "resources", 
                    {**agents["seller_1"].resources, resource: agents["seller_1"].resources.get(resource, 0) + amount}
                )
            }),
            "buyer_1": type("Agent", (), {
                "id": "buyer_1",
                "type": "market_participant",
                "resources": {"capital": 500000},
                "add_resource": lambda resource, amount: setattr(
                    agents["buyer_1"], "resources", 
                    {**agents["buyer_1"].resources, resource: agents["buyer_1"].resources.get(resource, 0) + amount}
                ),
                "remove_resource": lambda resource, amount: setattr(
                    agents["buyer_1"], "resources", 
                    {**agents["buyer_1"].resources, resource: agents["buyer_1"].resources.get(resource, 0) - amount}
                )
            })
        }
        
        # Register a test product
        product = {
            "id": "product_123",
            "name": "High-Yield Corn",
            "company_id": "seller_1",
            "segment": "grain_crops",
            "technology": "crispr",
            "traits": ["yield"],
            "performance": 85,
            "price": 150,
            "development_cost": 5000000,
            "regulatory_status": "approved",
            "regions_approved": ["north_america"],
            "launch_year": 2020
        }
        self.market_model.register_product(product)
        
        # Create a test transaction
        transaction = {
            "buyer_id": "buyer_1",
            "seller_id": "seller_1",
            "product_id": "product_123",
            "quantity": 1000,
            "price_per_unit": 150,
            "year": 2022
        }
        
        # Process the transaction
        result = self.market_model.process_transaction(transaction, agents)
        
        # Check that the transaction was processed
        self.assertTrue(result["success"])
        
        # Check that resources were updated
        total_price = transaction["quantity"] * transaction["price_per_unit"]
        self.assertEqual(agents["seller_1"].resources["capital"], 10000000 + total_price)
        self.assertEqual(agents["buyer_1"].resources["capital"], 500000 - total_price)


class TestPricingModel(unittest.TestCase):
    """Test cases for the PricingModel class."""

    def setUp(self):
        """Set up test fixtures."""
        self.pricing_model = PricingModel()

    def test_calculate_base_price(self):
        """Test calculating base price for a product."""
        # Create a test product
        product = {
            "segment": "grain_crops",
            "technology": "crispr",
            "traits": ["yield", "drought_resistance"],
            "performance": 85,
            "development_cost": 5000000
        }
        
        # Calculate base price
        base_price = self.pricing_model.calculate_base_price(product)
        
        # Check that a reasonable base price was calculated
        self.assertGreater(base_price, 0)
        
        # Check that a product with higher performance has a higher price
        high_performance_product = {**product, "performance": 95}
        high_performance_price = self.pricing_model.calculate_base_price(high_performance_product)
        self.assertGreater(high_performance_price, base_price)
        
        # Check that a product with more traits has a higher price
        more_traits_product = {**product, "traits": ["yield", "drought_resistance", "pest_resistance"]}
        more_traits_price = self.pricing_model.calculate_base_price(more_traits_product)
        self.assertGreater(more_traits_price, base_price)

    def test_adjust_price_for_market(self):
        """Test adjusting price based on market conditions."""
        # Create a test product with base price
        product = {
            "id": "product_123",
            "segment": "grain_crops",
            "technology": "crispr",
            "traits": ["yield"],
            "performance": 85,
            "price": 150,
            "launch_year": 2020
        }
        
        # Create market conditions
        market_conditions = {
            "competition_level": 0.7,  # High competition
            "demand_level": 0.8,      # High demand
            "price_sensitivity": 0.6,  # Moderate price sensitivity
            "year": 2022
        }
        
        # Adjust price
        adjusted_price = self.pricing_model.adjust_price_for_market(
            product, market_conditions
        )
        
        # Check that the price was adjusted
        self.assertNotEqual(adjusted_price, product["price"])
        
        # Check that with higher competition and price sensitivity, price decreases
        high_competition = {**market_conditions, "competition_level": 0.9, "price_sensitivity": 0.8}
        high_competition_price = self.pricing_model.adjust_price_for_market(
            product, high_competition
        )
        self.assertLess(high_competition_price, adjusted_price)
        
        # Check that with higher demand, price increases
        high_demand = {**market_conditions, "demand_level": 0.95, "competition_level": 0.5}
        high_demand_price = self.pricing_model.adjust_price_for_market(
            product, high_demand
        )
        self.assertGreater(high_demand_price, adjusted_price)


class TestAdoptionModel(unittest.TestCase):
    """Test cases for the AdoptionModel class."""

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
        self.adoption_model = AdoptionModel(self.config)

    def tearDown(self):
        """Tear down test fixtures."""
        shutil.rmtree(self.temp_dir)

    def test_initialization(self):
        """Test adoption model initialization."""
        self.assertEqual(self.adoption_model.config, self.config)
        self.assertIsNotNone(self.adoption_model.params)
        self.assertIn("farmer_roi_threshold", self.adoption_model.params)
        self.assertIn("consumer_price_sensitivity", self.adoption_model.params)
        self.assertIn("sustainability_weight", self.adoption_model.params)

    def test_calculate_adoption_rate(self):
        """Test calculating adoption rate for a product."""
        # Create a test product
        product = {
            "id": "product_123",
            "name": "High-Yield Corn",
            "segment": "grain_crops",
            "technology": "crispr",
            "traits": ["yield", "drought_resistance"],
            "performance": 85,
            "price": 150,
            "sustainability_score": 70,
            "launch_year": 2020
        }
        
        # Create market conditions
        market_conditions = {
            "year": 2022,
            "region": "north_america",
            "segment": "grain_crops",
            "average_price": 120,
            "average_performance": 75,
            "technology_familiarity": {"crispr": 0.6},
            "regulatory_sentiment": 0.7
        }
        
        # Calculate adoption rate
        adoption_rate = self.adoption_model.calculate_adoption_rate(
            product, market_conditions
        )
        
        # Check that a valid adoption rate was calculated
        self.assertGreaterEqual(adoption_rate, 0.0)
        self.assertLessEqual(adoption_rate, 1.0)
        
        # Check that a product with higher performance has a higher adoption rate
        high_performance_product = {**product, "performance": 95}
        high_performance_rate = self.adoption_model.calculate_adoption_rate(
            high_performance_product, market_conditions
        )
        self.assertGreater(high_performance_rate, adoption_rate)
        
        # Check that a product with higher price has a lower adoption rate
        high_price_product = {**product, "price": 200}
        high_price_rate = self.adoption_model.calculate_adoption_rate(
            high_price_product, market_conditions
        )
        self.assertLess(high_price_rate, adoption_rate)

    def test_simulate_diffusion(self):
        """Test simulating technology diffusion over time."""
        # Create initial adoption data
        initial_adoption = {
            "product_123": {
                "adoption_rate": 0.05,  # 5% initial adoption
                "cumulative_adoption": 0.05,
                "year": 2020
            }
        }
        
        # Create product data
        product = {
            "id": "product_123",
            "name": "High-Yield Corn",
            "segment": "grain_crops",
            "technology": "crispr",
            "traits": ["yield"],
            "performance": 85,
            "price": 150,
            "launch_year": 2020
        }
        
        # Create market conditions
        market_conditions = {
            "region": "north_america",
            "segment": "grain_crops",
            "average_price": 120,
            "average_performance": 75,
            "technology_familiarity": {"crispr": 0.6},
            "regulatory_sentiment": 0.7,
            "market_size": 1000000
        }
        
        # Simulate diffusion for 5 years
        diffusion_results = self.adoption_model.simulate_diffusion(
            product, initial_adoption["product_123"], market_conditions, 5
        )
        
        # Check that diffusion was simulated
        self.assertIsInstance(diffusion_results, dict)
        self.assertIn("yearly_adoption", diffusion_results)
        self.assertEqual(len(diffusion_results["yearly_adoption"]), 5)
        
        # Check that adoption increases over time
        yearly_rates = [year_data["adoption_rate"] 
                       for year_data in diffusion_results["yearly_adoption"]]
        self.assertGreater(yearly_rates[-1], yearly_rates[0])
        
        # Check that cumulative adoption increases over time
        cumulative_adoption = [year_data["cumulative_adoption"] 
                              for year_data in diffusion_results["yearly_adoption"]]
        self.assertGreater(cumulative_adoption[-1], cumulative_adoption[0])
        
        # Check that cumulative adoption follows an S-curve pattern
        # (acceleration followed by deceleration)
        differences = [cumulative_adoption[i+1] - cumulative_adoption[i] 
                      for i in range(len(cumulative_adoption)-1)]
        # In an S-curve, differences increase then decrease
        # Check if there's a peak in the differences
        has_peak = any(differences[i] > differences[i-1] and differences[i] > differences[i+1] 
                      for i in range(1, len(differences)-1))
        self.assertTrue(has_peak)


if __name__ == "__main__":
    unittest.main()