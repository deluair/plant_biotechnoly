#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Market model for plant biotechnology products.

This module implements economic market models for simulating the adoption,
pricing, and economic impact of plant biotechnology products.
"""

import logging
import random
import numpy as np
import pandas as pd
from typing import Dict, List, Any, Optional, Tuple

from biosimulate.simulation.config import SimulationConfig


class MarketModel:
    """Economic market model for plant biotechnology products.
    
    This class simulates market dynamics for plant biotechnology products,
    including adoption rates, pricing, competition, and economic impacts.
    
    Attributes:
        config: Simulation configuration
        market_segments: Dictionary of market segments and their characteristics
        adoption_curves: Dictionary of technology adoption curves by segment
        price_models: Dictionary of pricing models by product type
        competition_matrix: Matrix of competition factors between products
    """
    
    def __init__(self, config: SimulationConfig):
        """Initialize the market model.
        
        Args:
            config: Simulation configuration
        """
        self.config = config
        self.logger = logging.getLogger(__name__)
        
        # Initialize market parameters
        self.params = {
            "base_adoption_rate": 0.05,  # Base annual adoption rate
            "price_elasticity": -0.7,    # Price elasticity of demand
            "innovation_premium": 0.2,   # Price premium for innovative products
            "competition_factor": 0.3,   # Impact of competition on pricing
            "market_growth_rate": 0.03,  # Annual market growth rate
            "regional_factors": {        # Regional market factors
                "north_america": 1.2,
                "europe": 1.0,
                "asia": 1.5,
                "south_america": 1.3,
                "africa": 0.8
            }
        }
        
        # Initialize market segments
        self.market_segments = self._initialize_market_segments()
        
        # Initialize adoption curves
        self.adoption_curves = self._initialize_adoption_curves()
        
        # Initialize price models
        self.price_models = self._initialize_price_models()
        
        # Initialize competition matrix
        self.competition_matrix = self._initialize_competition_matrix()
        
        # Market data storage
        self.market_data = {
            "products": {},
            "annual_sales": {},
            "market_shares": {},
            "prices": {},
            "adoption_rates": {}
        }

    def register_product(self, product: Dict[str, Any], agent_id: str):
        """Register a new product in the market."""
        product_id = f"{agent_id}_{product.get('name', 'UnnamedProduct')}"
        if product_id not in self.market_data['products']:
            self.market_data['products'][product_id] = product
            self.logger.info(f"Product '{product.get('name')}' from agent {agent_id} registered in the market.")
        else:
            self.logger.warning(f"Attempted to register existing product {product_id}.")
    
    def _initialize_market_segments(self) -> Dict[str, Dict[str, Any]]:
        """Initialize market segments.
        
        Returns:
            Dictionary of market segments and their characteristics
        """
        return {
            "row_crops": {
                "size": 100000000000,  # $100B initial market size
                "growth_rate": 0.02,
                "price_sensitivity": 0.8,
                "innovation_receptivity": 0.6,
                "regions": {
                    "north_america": 0.35,
                    "europe": 0.15,
                    "asia": 0.25,
                    "south_america": 0.2,
                    "africa": 0.05
                }
            },
            "specialty_crops": {
                "size": 50000000000,  # $50B initial market size
                "growth_rate": 0.04,
                "price_sensitivity": 0.6,
                "innovation_receptivity": 0.8,
                "regions": {
                    "north_america": 0.3,
                    "europe": 0.25,
                    "asia": 0.2,
                    "south_america": 0.15,
                    "africa": 0.1
                }
            },
            "biofuels": {
                "size": 30000000000,  # $30B initial market size
                "growth_rate": 0.05,
                "price_sensitivity": 0.9,
                "innovation_receptivity": 0.7,
                "regions": {
                    "north_america": 0.4,
                    "europe": 0.3,
                    "asia": 0.15,
                    "south_america": 0.1,
                    "africa": 0.05
                }
            }
        }
    
    def _initialize_adoption_curves(self) -> Dict[str, Dict[str, Any]]:
        """Initialize technology adoption curves by market segment.
        
        Returns:
            Dictionary of adoption curve parameters by segment and technology
        """
        return {
            "row_crops": {
                "conventional": {"max_adoption": 0.95, "rate": 0.1},
                "gene_editing": {"max_adoption": 0.8, "rate": 0.15},
                "transgenics": {"max_adoption": 0.7, "rate": 0.12}
            },
            "specialty_crops": {
                "conventional": {"max_adoption": 0.9, "rate": 0.08},
                "gene_editing": {"max_adoption": 0.75, "rate": 0.1},
                "transgenics": {"max_adoption": 0.6, "rate": 0.09}
            },
            "biofuels": {
                "conventional": {"max_adoption": 0.85, "rate": 0.12},
                "gene_editing": {"max_adoption": 0.9, "rate": 0.18},
                "transgenics": {"max_adoption": 0.8, "rate": 0.15}
            }
        }
    
    def _initialize_price_models(self) -> Dict[str, Dict[str, Any]]:
        """Initialize pricing models by product type.
        
        Returns:
            Dictionary of pricing model parameters by product type
        """
        return {
            "seed": {
                "base_price": 100,  # Base price per unit
                "innovation_premium": 0.3,  # Premium for innovative traits
                "trait_value_factor": 0.2,  # Price increase per trait value point
                "competition_discount": 0.1  # Price discount due to competition
            },
            "crop_protection": {
                "base_price": 50,
                "innovation_premium": 0.4,
                "trait_value_factor": 0.15,
                "competition_discount": 0.15
            },
            "biostimulants": {
                "base_price": 30,
                "innovation_premium": 0.5,
                "trait_value_factor": 0.25,
                "competition_discount": 0.05
            }
        }
    
    def _initialize_competition_matrix(self) -> Dict[str, Dict[str, float]]:
        """Initialize competition matrix between product types.
        
        Returns:
            Dictionary of competition factors between product types
        """
        return {
            "conventional": {
                "conventional": 1.0,
                "gene_editing": 0.7,
                "transgenics": 0.5
            },
            "gene_editing": {
                "conventional": 0.8,
                "gene_editing": 1.0,
                "transgenics": 0.6
            },
            "transgenics": {
                "conventional": 0.6,
                "gene_editing": 0.7,
                "transgenics": 1.0
            }
        }
    
    def register_product(self, product_id: str, product_data: Dict[str, Any]) -> None:
        """Register a new product in the market.
        
        Args:
            product_id: Unique identifier for the product
            product_data: Dictionary of product data including type, traits, etc.
        """
        self.market_data["products"][product_id] = product_data
        self.market_data["annual_sales"][product_id] = {}
        self.market_data["prices"][product_id] = {}
        self.market_data["adoption_rates"][product_id] = {}
        
        self.logger.info(f"Registered product {product_id} in market model")
    
    def calculate_product_price(self, product_id: str, year: int, region: str) -> float:
        """Calculate the price for a product in a given year and region.
        
        Args:
            product_id: Product identifier
            year: Simulation year
            region: Market region
            
        Returns:
            Calculated price for the product
        """
        if product_id not in self.market_data["products"]:
            self.logger.warning(f"Product {product_id} not registered in market model")
            return 0.0
        
        product = self.market_data["products"][product_id]
        product_type = product.get("type", "seed")
        technology = product.get("technology", "conventional")
        traits = product.get("traits", [])
        
        # Get base price from price model
        if product_type in self.price_models:
            price_model = self.price_models[product_type]
            base_price = price_model["base_price"]
        else:
            base_price = 100  # Default base price
        
        # Apply innovation premium based on technology
        if technology == "gene_editing":
            innovation_factor = 1.2
        elif technology == "transgenics":
            innovation_factor = 1.3
        else:
            innovation_factor = 1.0
        
        # Apply trait value premium
        trait_value = sum(trait.get("value", 1) for trait in traits) if traits else 0
        trait_premium = 1.0 + (trait_value * 0.05)  # 5% premium per trait value point
        
        # Apply regional factor
        regional_factor = self.params["regional_factors"].get(region, 1.0)
        
        # Apply competition discount based on similar products
        competition_discount = self._calculate_competition_discount(product_id, year, region)
        
        # Calculate final price
        price = base_price * innovation_factor * trait_premium * regional_factor * (1 - competition_discount)
        
        # Store price in market data
        if year not in self.market_data["prices"][product_id]:
            self.market_data["prices"][product_id][year] = {}
        self.market_data["prices"][product_id][year][region] = price
        
        return price
    
    def _calculate_competition_discount(self, product_id: str, year: int, region: str) -> float:
        """Calculate competition discount based on similar products in the market.
        
        Args:
            product_id: Product identifier
            year: Simulation year
            region: Market region
            
        Returns:
            Competition discount factor (0-1)
        """
        # Simple implementation - in a real model this would be more sophisticated
        product = self.market_data["products"][product_id]
        product_type = product.get("type", "seed")
        technology = product.get("technology", "conventional")
        
        # Count competing products of similar type and technology
        competing_products = 0
        for pid, pdata in self.market_data["products"].items():
            if pid != product_id and pdata.get("type") == product_type:
                competing_products += 1
        
        # Calculate discount based on number of competitors
        base_discount = min(0.5, competing_products * 0.05)  # Max 50% discount
        
        # Adjust discount based on competition matrix
        if technology in self.competition_matrix:
            competition_factors = []
            for pid, pdata in self.market_data["products"].items():
                if pid != product_id:
                    other_tech = pdata.get("technology", "conventional")
                    if other_tech in self.competition_matrix[technology]:
                        competition_factors.append(self.competition_matrix[technology][other_tech])
            
            if competition_factors:
                avg_competition = sum(competition_factors) / len(competition_factors)
                return base_discount * avg_competition
        
        return base_discount
    
    def calculate_adoption_rate(self, product_id: str, year: int, region: str) -> float:
        """Calculate the adoption rate for a product in a given year and region.
        
        Args:
            product_id: Product identifier
            year: Simulation year
            region: Market region
            
        Returns:
            Adoption rate (0-1) for the product
        """
        if product_id not in self.market_data["products"]:
            self.logger.warning(f"Product {product_id} not registered in market model")
            return 0.0
        
        product = self.market_data["products"][product_id]
        segment = product.get("segment", "row_crops")
        technology = product.get("technology", "conventional")
        launch_year = product.get("launch_year", self.config.start_year)
        
        # Calculate years since launch
        years_since_launch = max(0, year - launch_year)
        
        # Get adoption curve parameters
        if segment in self.adoption_curves and technology in self.adoption_curves[segment]:
            curve = self.adoption_curves[segment][technology]
            max_adoption = curve["max_adoption"]
            rate = curve["rate"]
        else:
            max_adoption = 0.7  # Default max adoption
            rate = 0.1  # Default adoption rate
        
        # Apply S-curve adoption model
        if years_since_launch <= 0:
            adoption = 0.0
        else:
            # S-curve formula: max_adoption / (1 + exp(-rate * (years_since_launch - midpoint)))
            midpoint = 5  # Years to reach 50% of max adoption
            adoption = max_adoption / (1 + np.exp(-rate * (years_since_launch - midpoint)))
        
        # Apply regional adjustment
        if segment in self.market_segments and "regions" in self.market_segments[segment]:
            regional_weight = self.market_segments[segment]["regions"].get(region, 1.0)
            adoption = adoption * regional_weight
        
        # Apply regulatory impact if available
        if "regulatory_impact" in product:
            reg_impact = product["regulatory_impact"].get(region, 1.0)
            adoption = adoption * reg_impact
        
        # Store adoption rate in market data
        if year not in self.market_data["adoption_rates"][product_id]:
            self.market_data["adoption_rates"][product_id][year] = {}
        self.market_data["adoption_rates"][product_id][year][region] = adoption
        
        return adoption

    def simulate_market_for_year(self, year: int, agents: Dict[str, Any], technology_pipeline: Any, regulatory_framework: Any) -> Dict[str, Any]:
        """Simulate market dynamics for a given year.

        Args:
            year: The simulation year.
            agents: Dictionary of agent instances.
            technology_pipeline: The technology pipeline instance.
            regulatory_framework: The regulatory framework instance.

        Returns:
            A dictionary of market metrics for the year.
        """
        total_sales = 0
        regional_sales = {region: 0 for region in self.params['regional_factors']}
        product_sales = {}

        if not self.market_data["products"]:
            self.logger.warning(f"No products registered in the market for year {year}. Returning zero metrics.")
            return {
                'total_market_size': 0,
                'regional_sales': regional_sales,
                'product_sales': product_sales,
                'average_price': 0
            }

        all_prices = []
        for product_id, product_data in self.market_data["products"].items():
            sales_for_product = 0
            for region in self.params['regional_factors']:
                price = self.calculate_product_price(product_id, year, region)
                adoption_rate = self.calculate_adoption_rate(product_id, year, region)
                sales = self.calculate_sales(product_id, year, region)
                
                # Update market data
                if year not in self.market_data['annual_sales'][product_id]:
                    self.market_data['annual_sales'][product_id][year] = {}
                self.market_data['annual_sales'][product_id][year][region] = sales
                
                regional_sales[region] += sales
                sales_for_product += sales
                if price > 0:
                    all_prices.append(price)
            
            product_sales[product_id] = sales_for_product
            total_sales += sales_for_product

        # Update total market data for the year
        self.market_data['annual_sales'][year] = regional_sales
        self.market_data['market_shares'][year] = {pid: sales / total_sales if total_sales > 0 else 0 for pid, sales in product_sales.items()}
        
        avg_price = sum(all_prices) / len(all_prices) if all_prices else 0

        market_metrics = {
            'total_market_size': total_sales,
            'regional_sales': regional_sales,
            'product_sales': product_sales,
            'average_price': avg_price
        }
        
        self.logger.info(f"Market simulation for year {year} complete. Total sales: ${total_sales:,.2f}")
        return market_metrics

    def calculate_market_share(self, product_id: str, year: int) -> float:
        """Calculate the market share for a product in a given year.

        Args:
            product_id: Product identifier
            year: Simulation year

        Returns:
            Market share (0-1) for the product
        """
        if year not in self.market_data['market_shares'] or product_id not in self.market_data['market_shares'][year]:
            return 0.0
        
        return self.market_data['market_shares'][year][product_id]
    
    def calculate_sales(self, product_id: str, year: int, region: str) -> float:
        """Calculate sales for a product in a given year and region.

        Args:
            product_id: Product identifier
            year: Simulation year
            region: Market region

        Returns:
            Sales value for the product
        """
        if product_id not in self.market_data["products"]:
            self.logger.warning(f"Product {product_id} not registered in market model")
            return 0.0

        product = self.market_data["products"][product_id]
        segment = product.get("segment", "row_crops")

        # Get market size for segment and region
        if segment in self.market_segments:
            total_market_size = self.market_segments[segment]["size"]
            growth_rate = self.market_segments[segment]["growth_rate"]

            # Apply market growth over time
            years_growth = year - self.config.start_year
            market_size = total_market_size * ((1 + growth_rate) ** years_growth)

            # Apply regional distribution
            if "regions" in self.market_segments[segment]:
                regional_share = self.market_segments[segment]["regions"].get(region, 0.2)
                regional_market_size = market_size * regional_share
            else:
                regional_market_size = market_size * 0.2  # Default regional share
        else:
            regional_market_size = 0

        # Get adoption rate
        adoption_rate = self.calculate_adoption_rate(product_id, year, region)

        # Calculate market share
        market_share = self._calculate_market_share(product_id, year, region, segment)

        # Calculate sales
        sales = regional_market_size * adoption_rate * market_share

        return sales

    def _calculate_market_share(self, product_id: str, year: int, region: str, segment: str) -> float:
        """Calculate market share for a product among competing products.

        Args:
            product_id: Product identifier
            year: Simulation year
            region: Market region
            segment: Market segment

        Returns:
            Market share (0-1) for the product
        """
        # Identify competing products in the same segment
        competing_products = []
        for pid, pdata in self.market_data["products"].items():
            if pdata.get("segment") == segment:
                competing_products.append(pid)

        if not competing_products or product_id not in competing_products:
            return 0.0

        if len(competing_products) == 1:
            return 1.0

        # Calculate relative attractiveness of each product
        attractiveness = {}
        total_attractiveness = 0.0

        for pid in competing_products:
            product = self.market_data["products"][pid]

            # Calculate adoption rate
            adoption = self.calculate_adoption_rate(pid, year, region)

            # Calculate price factor (lower price = higher attractiveness)
            price = self.calculate_product_price(pid, year, region)
            price_factor = 1.0 / max(1.0, price)  # Inverse relationship with price

            # Calculate trait value
            traits = product.get("traits", [])
            trait_value = sum(trait.get("value", 1) for trait in traits) if traits else 0
            trait_factor = 1.0 + (trait_value * 0.1)  # 10% increase per trait value point

            # Calculate product attractiveness
            product_attractiveness = adoption * price_factor * trait_factor
            attractiveness[pid] = product_attractiveness
            total_attractiveness += product_attractiveness

        # Calculate market share based on relative attractiveness
        if total_attractiveness > 0:
            market_share = attractiveness.get(product_id, 0.0) / total_attractiveness
        else:
            market_share = 1.0 / len(competing_products)  # Equal share if no attractiveness

        return market_share
    
    def simulate_market_year(self, year: int) -> Dict[str, Any]:
        """Simulate market dynamics for a given year.
        
        Args:
            year: Simulation year
            
        Returns:
            Dictionary with market simulation results
        """
        results = {
            "year": year,
            "total_market_value": 0.0,
            "products": {},
            "segments": {},
            "regions": {}
        }
        
        # Initialize segment and region totals
        for segment in self.market_segments:
            results["segments"][segment] = {"sales": 0.0, "products": 0}
        
        for region in self.params["regional_factors"]:
            results["regions"][region] = {"sales": 0.0, "products": 0}
        
        # Calculate sales for each product in each region
        for product_id, product in self.market_data["products"].items():
            segment = product.get("segment", "row_crops")
            results["products"][product_id] = {"total_sales": 0.0, "regions": {}}
            
            for region in self.params["regional_factors"]:
                # Calculate sales for this product in this region
                sales = self.calculate_sales(product_id, year, region)
                
                # Update product results
                results["products"][product_id]["regions"][region] = sales
                results["products"][product_id]["total_sales"] += sales
                
                # Update segment results
                results["segments"][segment]["sales"] += sales
                
                # Update region results
                results["regions"][region]["sales"] += sales
                
                # Update total market value
                results["total_market_value"] += sales
            
            # Count product in segment and regions where it has sales
            results["segments"][segment]["products"] += 1
            for region, sales in results["products"][product_id]["regions"].items():
                if sales > 0:
                    results["regions"][region]["products"] += 1
        
        return results