"""Market Participant Agent Module.

This module defines the MarketParticipant class, which represents various stakeholders
in the agricultural market within the plant biotechnology industry ecosystem simulation.
"""

from dataclasses import dataclass, field
from typing import Dict, List, Any, Optional, Set
import random
import logging

from biosimulate.agents.base_agent import BaseAgent
from biosimulate.utils.data_generator import generate_normal, generate_triangular, generate_beta


@dataclass
class MarketParticipant(BaseAgent):
    """Represents a market participant in the plant biotechnology industry.
    
    This class models various stakeholders in the agricultural market, including farmers,
    distributors, retailers, and consumers, who make decisions about adopting, distributing,
    selling, or purchasing biotechnology products.
    
    Attributes:
        participant_type: Type of market participant (farmer, distributor, retailer, consumer)
        size: Size of the participant (small, medium, large)
        market_segments: Market segments the participant operates in
        technology_adoption: Dictionary tracking adopted technologies
        product_portfolio: Dictionary of products the participant uses/sells
        preferences: Dictionary of participant preferences
        risk_aversion: Level of risk aversion (0-100)
        price_sensitivity: Level of price sensitivity (0-100)
        innovation_openness: Openness to innovation (0-100)
        sustainability_focus: Focus on sustainability (0-100)
        knowledge_level: Knowledge of biotechnology (0-100)
        social_influence: Level of social influence (0-100)
        economic_status: Economic status (0-100)
        satisfaction: Satisfaction with current products (0-100)
        purchase_history: History of purchases/adoptions
        relationships: Relationships with other market participants
    """
    
    # Market participant specific attributes
    participant_type: str = field(default="farmer")
    size: str = field(default="medium")
    market_segments: List[str] = field(default_factory=list)
    technology_adoption: Dict[str, Dict[str, Any]] = field(default_factory=dict)
    product_portfolio: Dict[str, Dict[str, Any]] = field(default_factory=dict)
    preferences: Dict[str, Any] = field(default_factory=dict)
    risk_aversion: float = field(default=50.0)
    price_sensitivity: float = field(default=50.0)
    innovation_openness: float = field(default=50.0)
    sustainability_focus: float = field(default=50.0)
    knowledge_level: float = field(default=50.0)
    social_influence: float = field(default=0.0)
    economic_status: float = field(default=50.0)
    satisfaction: float = field(default=50.0)
    purchase_history: List[Dict[str, Any]] = field(default_factory=list)
    relationships: Dict[str, Dict[str, Any]] = field(default_factory=dict)
    
    def __post_init__(self):
        """Initialize the market participant with default values based on type."""
        super().__post_init__()
        
        # Set agent type
        self.type = "market_participant"
        
        # Initialize attributes based on participant type
        self._initialize_attributes()
        
        # Initialize market segments
        self._initialize_market_segments()
        
        # Initialize preferences
        self._initialize_preferences()
        
        # Initialize resources
        self._initialize_resources()
    
    def _initialize_attributes(self):
        """Initialize attributes based on participant type."""
        # Set base attributes by participant type
        if self.participant_type == "farmer":
            self._initialize_farmer_attributes()
        elif self.participant_type == "distributor":
            self._initialize_distributor_attributes()
        elif self.participant_type == "retailer":
            self._initialize_retailer_attributes()
        elif self.participant_type == "consumer":
            self._initialize_consumer_attributes()
        elif self.participant_type == "processor":
            self._initialize_processor_attributes()
        
        # Adjust attributes based on size
        self._adjust_attributes_by_size()
    
    def _initialize_farmer_attributes(self):
        """Initialize attributes specific to farmers."""
        # Farmers tend to be more risk-averse and price-sensitive
        self.risk_aversion = generate_triangular(40, 70, 90)
        self.price_sensitivity = generate_triangular(60, 75, 90)
        self.innovation_openness = generate_triangular(20, 50, 80)
        self.sustainability_focus = generate_triangular(30, 60, 90)
        self.knowledge_level = generate_triangular(30, 60, 90)
        self.social_influence = generate_triangular(10, 30, 70)
        self.economic_status = generate_triangular(20, 50, 80)
        
        # Initialize technology adoption with common agricultural technologies
        self.technology_adoption = {
            "conventional_seeds": {
                "adoption_year": random.randint(1950, 1990),
                "satisfaction": generate_triangular(50, 70, 90),
                "usage_level": generate_triangular(70, 90, 100)
            },
            "chemical_fertilizers": {
                "adoption_year": random.randint(1950, 1990),
                "satisfaction": generate_triangular(50, 70, 90),
                "usage_level": generate_triangular(70, 90, 100)
            },
            "chemical_pesticides": {
                "adoption_year": random.randint(1950, 1990),
                "satisfaction": generate_triangular(50, 70, 90),
                "usage_level": generate_triangular(70, 90, 100)
            },
            "irrigation_systems": {
                "adoption_year": random.randint(1960, 2000),
                "satisfaction": generate_triangular(60, 80, 95),
                "usage_level": generate_triangular(50, 80, 100)
            }
        }
        
        # Add biotech adoption based on innovation openness
        if self.innovation_openness > 60:
            self.technology_adoption["first_gen_gmo"] = {
                "adoption_year": random.randint(1996, 2010),
                "satisfaction": generate_triangular(60, 75, 90),
                "usage_level": generate_triangular(30, 60, 90)
            }
        
        if self.innovation_openness > 80:
            self.technology_adoption["precision_agriculture"] = {
                "adoption_year": random.randint(2005, 2020),
                "satisfaction": generate_triangular(70, 85, 95),
                "usage_level": generate_triangular(20, 50, 80)
            }
    
    def _initialize_distributor_attributes(self):
        """Initialize attributes specific to distributors."""
        # Distributors are market-oriented and moderately innovative
        self.risk_aversion = generate_triangular(30, 50, 70)
        self.price_sensitivity = generate_triangular(40, 60, 80)
        self.innovation_openness = generate_triangular(40, 60, 80)
        self.sustainability_focus = generate_triangular(20, 50, 80)
        self.knowledge_level = generate_triangular(50, 70, 90)
        self.social_influence = generate_triangular(40, 60, 80)
        self.economic_status = generate_triangular(40, 70, 90)
        
        # Initialize technology adoption with logistics and supply chain technologies
        self.technology_adoption = {
            "inventory_management": {
                "adoption_year": random.randint(1980, 2000),
                "satisfaction": generate_triangular(60, 75, 90),
                "usage_level": generate_triangular(70, 85, 100)
            },
            "supply_chain_tracking": {
                "adoption_year": random.randint(1990, 2010),
                "satisfaction": generate_triangular(65, 80, 95),
                "usage_level": generate_triangular(60, 80, 95)
            },
            "quality_control_systems": {
                "adoption_year": random.randint(1985, 2005),
                "satisfaction": generate_triangular(70, 85, 95),
                "usage_level": generate_triangular(70, 85, 100)
            }
        }
        
        # Add biotech-specific systems based on innovation openness
        if self.innovation_openness > 60:
            self.technology_adoption["gmo_tracking_systems"] = {
                "adoption_year": random.randint(2000, 2015),
                "satisfaction": generate_triangular(65, 80, 90),
                "usage_level": generate_triangular(50, 70, 90)
            }
        
        if self.innovation_openness > 80:
            self.technology_adoption["blockchain_traceability"] = {
                "adoption_year": random.randint(2015, 2022),
                "satisfaction": generate_triangular(60, 75, 90),
                "usage_level": generate_triangular(20, 40, 70)
            }
    
    def _initialize_retailer_attributes(self):
        """Initialize attributes specific to retailers."""
        # Retailers are consumer-focused and responsive to market trends
        self.risk_aversion = generate_triangular(30, 50, 70)
        self.price_sensitivity = generate_triangular(50, 70, 90)
        self.innovation_openness = generate_triangular(40, 60, 80)
        self.sustainability_focus = generate_triangular(30, 60, 90)
        self.knowledge_level = generate_triangular(40, 60, 80)
        self.social_influence = generate_triangular(50, 70, 90)
        self.economic_status = generate_triangular(40, 65, 90)
        
        # Initialize technology adoption with retail technologies
        self.technology_adoption = {
            "inventory_management": {
                "adoption_year": random.randint(1980, 2000),
                "satisfaction": generate_triangular(60, 75, 90),
                "usage_level": generate_triangular(70, 85, 100)
            },
            "point_of_sale_systems": {
                "adoption_year": random.randint(1985, 2005),
                "satisfaction": generate_triangular(70, 85, 95),
                "usage_level": generate_triangular(80, 90, 100)
            },
            "customer_relationship_management": {
                "adoption_year": random.randint(1995, 2010),
                "satisfaction": generate_triangular(65, 80, 90),
                "usage_level": generate_triangular(60, 75, 90)
            }
        }
        
        # Add biotech-specific retail approaches based on sustainability focus
        if self.sustainability_focus > 60:
            self.technology_adoption["organic_product_lines"] = {
                "adoption_year": random.randint(1995, 2015),
                "satisfaction": generate_triangular(70, 85, 95),
                "usage_level": generate_triangular(30, 50, 80)
            }
        
        if self.sustainability_focus > 80:
            self.technology_adoption["sustainability_certification"] = {
                "adoption_year": random.randint(2005, 2020),
                "satisfaction": generate_triangular(75, 85, 95),
                "usage_level": generate_triangular(20, 40, 70)
            }
    
    def _initialize_consumer_attributes(self):
        """Initialize attributes specific to consumers."""
        # Consumers have varied preferences and are influenced by many factors
        self.risk_aversion = generate_triangular(30, 60, 90)
        self.price_sensitivity = generate_triangular(40, 70, 95)
        self.innovation_openness = generate_triangular(20, 50, 80)
        self.sustainability_focus = generate_triangular(20, 60, 90)
        self.knowledge_level = generate_triangular(10, 40, 80)
        self.social_influence = generate_triangular(30, 60, 90)
        self.economic_status = generate_triangular(20, 50, 90)
        
        # Initialize technology adoption with consumer technologies
        self.technology_adoption = {
            "online_shopping": {
                "adoption_year": random.randint(2000, 2020),
                "satisfaction": generate_triangular(60, 80, 95),
                "usage_level": generate_triangular(30, 60, 90)
            },
            "food_delivery_apps": {
                "adoption_year": random.randint(2010, 2022),
                "satisfaction": generate_triangular(65, 80, 95),
                "usage_level": generate_triangular(20, 50, 80)
            }
        }
        
        # Add biotech-specific consumer behaviors based on knowledge and sustainability focus
        if self.knowledge_level > 60 and self.sustainability_focus > 60:
            self.technology_adoption["eco_labeling_awareness"] = {
                "adoption_year": random.randint(2000, 2020),
                "satisfaction": generate_triangular(70, 85, 95),
                "usage_level": generate_triangular(40, 70, 90)
            }
    
    def _initialize_processor_attributes(self):
        """Initialize attributes specific to food processors."""
        # Processors focus on efficiency, quality, and regulatory compliance
        self.risk_aversion = generate_triangular(40, 60, 80)
        self.price_sensitivity = generate_triangular(50, 70, 90)
        self.innovation_openness = generate_triangular(40, 60, 80)
        self.sustainability_focus = generate_triangular(30, 50, 80)
        self.knowledge_level = generate_triangular(50, 70, 90)
        self.social_influence = generate_triangular(30, 50, 70)
        self.economic_status = generate_triangular(40, 65, 90)
        
        # Initialize technology adoption with processing technologies
        self.technology_adoption = {
            "automated_processing": {
                "adoption_year": random.randint(1980, 2000),
                "satisfaction": generate_triangular(70, 85, 95),
                "usage_level": generate_triangular(60, 80, 95)
            },
            "quality_control_systems": {
                "adoption_year": random.randint(1985, 2005),
                "satisfaction": generate_triangular(75, 85, 95),
                "usage_level": generate_triangular(70, 85, 100)
            },
            "food_safety_systems": {
                "adoption_year": random.randint(1990, 2010),
                "satisfaction": generate_triangular(80, 90, 100),
                "usage_level": generate_triangular(80, 90, 100)
            }
        }
        
        # Add biotech-specific processing technologies based on innovation openness
        if self.innovation_openness > 60:
            self.technology_adoption["gmo_ingredient_tracking"] = {
                "adoption_year": random.randint(2000, 2015),
                "satisfaction": generate_triangular(70, 80, 90),
                "usage_level": generate_triangular(60, 75, 90)
            }
        
        if self.innovation_openness > 80:
            self.technology_adoption["novel_processing_techniques"] = {
                "adoption_year": random.randint(2010, 2022),
                "satisfaction": generate_triangular(65, 80, 90),
                "usage_level": generate_triangular(30, 50, 70)
            }
    
    def _adjust_attributes_by_size(self):
        """Adjust attributes based on participant size."""
        if self.size == "small":
            # Small participants tend to be more risk-averse, price-sensitive, and have less resources
            self.risk_aversion = min(100, self.risk_aversion * 1.2)
            self.price_sensitivity = min(100, self.price_sensitivity * 1.2)
            self.innovation_openness = max(0, self.innovation_openness * 0.8)
            self.economic_status = max(0, self.economic_status * 0.7)
            self.social_influence = max(0, self.social_influence * 0.7)
            
        elif self.size == "large":
            # Large participants tend to be less risk-averse, less price-sensitive, and have more resources
            self.risk_aversion = max(0, self.risk_aversion * 0.8)
            self.price_sensitivity = max(0, self.price_sensitivity * 0.8)
            self.innovation_openness = min(100, self.innovation_openness * 1.2)
            self.economic_status = min(100, self.economic_status * 1.3)
            self.social_influence = min(100, self.social_influence * 1.3)
            self.knowledge_level = min(100, self.knowledge_level * 1.2)
    
    def _initialize_market_segments(self):
        """Initialize market segments based on participant type."""
        if self.participant_type == "farmer":
            # Farmers can be in various crop segments
            possible_segments = [
                "grain_crops", "oilseed_crops", "fiber_crops", "fruit_crops", 
                "vegetable_crops", "specialty_crops", "organic_farming"
            ]
            
            # Select 1-3 segments based on size
            if self.size == "small":
                num_segments = random.randint(1, 2)
            elif self.size == "medium":
                num_segments = random.randint(1, 3)
            else:  # large
                num_segments = random.randint(2, 4)
            
            self.market_segments = random.sample(possible_segments, min(num_segments, len(possible_segments)))
            
            # Add organic segment based on sustainability focus
            if self.sustainability_focus > 70 and "organic_farming" not in self.market_segments:
                self.market_segments.append("organic_farming")
        
        elif self.participant_type == "distributor":
            # Distributors can handle various product types
            possible_segments = [
                "seeds", "fertilizers", "pesticides", "agricultural_equipment", 
                "raw_agricultural_products", "processed_food_ingredients"
            ]
            
            # Select segments based on size
            if self.size == "small":
                num_segments = random.randint(1, 2)
            elif self.size == "medium":
                num_segments = random.randint(2, 4)
            else:  # large
                num_segments = random.randint(3, 6)
            
            self.market_segments = random.sample(possible_segments, min(num_segments, len(possible_segments)))
        
        elif self.participant_type == "retailer":
            # Retailers can focus on various consumer segments
            possible_segments = [
                "supermarket", "specialty_food_store", "farmers_market", 
                "online_retail", "convenience_store", "wholesale_club"
            ]
            
            # Select segments based on size
            if self.size == "small":
                num_segments = 1
            elif self.size == "medium":
                num_segments = random.randint(1, 2)
            else:  # large
                num_segments = random.randint(2, 4)
            
            self.market_segments = random.sample(possible_segments, min(num_segments, len(possible_segments)))
        
        elif self.participant_type == "consumer":
            # Consumers can be in various demographic segments
            possible_segments = [
                "budget_conscious", "health_conscious", "convenience_oriented", 
                "environmentally_conscious", "gourmet", "traditional"
            ]
            
            # Select 1-2 primary segments
            num_segments = random.randint(1, 2)
            self.market_segments = random.sample(possible_segments, min(num_segments, len(possible_segments)))
            
            # Add segments based on attributes
            if self.price_sensitivity > 70 and "budget_conscious" not in self.market_segments:
                self.market_segments.append("budget_conscious")
            
            if self.sustainability_focus > 70 and "environmentally_conscious" not in self.market_segments:
                self.market_segments.append("environmentally_conscious")
        
        elif self.participant_type == "processor":
            # Processors can focus on various food categories
            possible_segments = [
                "grain_processing", "dairy_processing", "meat_processing", 
                "fruit_and_vegetable_processing", "beverage_production", 
                "snack_food_production", "specialty_food_production"
            ]
            
            # Select segments based on size
            if self.size == "small":
                num_segments = 1
            elif self.size == "medium":
                num_segments = random.randint(1, 3)
            else:  # large
                num_segments = random.randint(2, 4)
            
            self.market_segments = random.sample(possible_segments, min(num_segments, len(possible_segments)))
    
    def _initialize_preferences(self):
        """Initialize preferences based on participant type and attributes."""
        # Common preferences for all participant types
        self.preferences = {
            "price_importance": self.price_sensitivity / 100.0,
            "quality_importance": generate_triangular(0.5, 0.8, 1.0),
            "reliability_importance": generate_triangular(0.6, 0.8, 1.0),
            "innovation_importance": self.innovation_openness / 100.0,
            "sustainability_importance": self.sustainability_focus / 100.0,
            "brand_loyalty": generate_triangular(0.2, 0.5, 0.8),
            "local_preference": generate_triangular(0.3, 0.6, 0.9)
        }
        
        # Add participant-specific preferences
        if self.participant_type == "farmer":
            self.preferences.update({
                "yield_importance": generate_triangular(0.7, 0.9, 1.0),
                "pest_resistance_importance": generate_triangular(0.6, 0.8, 1.0),
                "drought_tolerance_importance": generate_triangular(0.5, 0.7, 0.9),
                "ease_of_use_importance": generate_triangular(0.5, 0.7, 0.9),
                "regulatory_compliance_importance": generate_triangular(0.6, 0.8, 1.0),
                "gmo_acceptance": max(0.0, min(1.0, (self.innovation_openness - 20) / 80.0))
            })
        
        elif self.participant_type == "distributor":
            self.preferences.update({
                "margin_importance": generate_triangular(0.7, 0.8, 0.9),
                "inventory_turnover_importance": generate_triangular(0.6, 0.8, 0.9),
                "supplier_reliability_importance": generate_triangular(0.7, 0.9, 1.0),
                "market_demand_importance": generate_triangular(0.7, 0.8, 0.9),
                "regulatory_compliance_importance": generate_triangular(0.7, 0.8, 1.0),
                "gmo_acceptance": max(0.0, min(1.0, (self.innovation_openness - 10) / 90.0))
            })
        
        elif self.participant_type == "retailer":
            self.preferences.update({
                "margin_importance": generate_triangular(0.7, 0.8, 0.9),
                "consumer_demand_importance": generate_triangular(0.8, 0.9, 1.0),
                "shelf_life_importance": generate_triangular(0.6, 0.8, 0.9),
                "visual_appeal_importance": generate_triangular(0.6, 0.8, 0.9),
                "supplier_reliability_importance": generate_triangular(0.7, 0.9, 1.0),
                "gmo_acceptance": max(0.0, min(1.0, (self.innovation_openness - 30) / 70.0))
            })
        
        elif self.participant_type == "consumer":
            self.preferences.update({
                "taste_importance": generate_triangular(0.7, 0.9, 1.0),
                "health_importance": generate_triangular(0.5, 0.7, 0.9),
                "convenience_importance": generate_triangular(0.6, 0.8, 0.9),
                "appearance_importance": generate_triangular(0.5, 0.7, 0.9),
                "novelty_importance": generate_triangular(0.3, 0.5, 0.8),
                "gmo_acceptance": max(0.0, min(1.0, (self.innovation_openness - 40) / 60.0))
            })
        
        elif self.participant_type == "processor":
            self.preferences.update({
                "consistency_importance": generate_triangular(0.8, 0.9, 1.0),
                "processing_efficiency_importance": generate_triangular(0.7, 0.8, 0.9),
                "ingredient_quality_importance": generate_triangular(0.7, 0.9, 1.0),
                "supplier_reliability_importance": generate_triangular(0.8, 0.9, 1.0),
                "regulatory_compliance_importance": generate_triangular(0.8, 0.9, 1.0),
                "gmo_acceptance": max(0.0, min(1.0, (self.innovation_openness - 20) / 80.0))
            })
        
        # Adjust GMO acceptance based on knowledge level
        if "gmo_acceptance" in self.preferences:
            knowledge_factor = self.knowledge_level / 100.0
            self.preferences["gmo_acceptance"] = (
                self.preferences["gmo_acceptance"] * 0.7 + knowledge_factor * 0.3
            )
    
    def _initialize_resources(self):
        """Initialize resources based on participant type and size."""
        # Base resources by size
        if self.size == "small":
            size_factor = 0.5
        elif self.size == "medium":
            size_factor = 1.0
        else:  # large
            size_factor = 2.0
        
        # Economic status affects resource levels
        economic_factor = self.economic_status / 50.0  # 1.0 at economic_status 50
        
        # Initialize common resources
        self.resources = {
            "capital": generate_triangular(10000, 50000, 200000) * size_factor * economic_factor,
            "employees": max(1, int(generate_triangular(1, 5, 20) * size_factor))
        }
        
        # Add participant-specific resources
        if self.participant_type == "farmer":
            self.resources.update({
                "land_hectares": generate_triangular(5, 50, 500) * size_factor,
                "equipment_value": generate_triangular(10000, 50000, 200000) * size_factor * economic_factor,
                "storage_capacity_tons": generate_triangular(50, 200, 1000) * size_factor
            })
        
        elif self.participant_type == "distributor":
            self.resources.update({
                "warehouse_capacity_m3": generate_triangular(1000, 5000, 20000) * size_factor,
                "vehicles": max(1, int(generate_triangular(2, 10, 50) * size_factor)),
                "distribution_network_size": max(1, int(generate_triangular(5, 20, 100) * size_factor))
            })
        
        elif self.participant_type == "retailer":
            self.resources.update({
                "store_count": max(1, int(generate_triangular(1, 5, 50) * size_factor)),
                "shelf_space_m2": generate_triangular(100, 500, 5000) * size_factor,
                "customer_base_size": generate_triangular(1000, 10000, 100000) * size_factor
            })
        
        elif self.participant_type == "consumer":
            self.resources.update({
                "household_size": max(1, int(generate_triangular(1, 3, 6))),
                "annual_food_budget": generate_triangular(2000, 5000, 15000) * economic_factor,
                "shopping_frequency_per_month": generate_triangular(2, 4, 8)
            })
        
        elif self.participant_type == "processor":
            self.resources.update({
                "processing_capacity_tons_per_day": generate_triangular(5, 50, 500) * size_factor,
                "facility_count": max(1, int(generate_triangular(1, 3, 10) * size_factor)),
                "equipment_value": generate_triangular(50000, 500000, 5000000) * size_factor * economic_factor
            })
    
    def step(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Execute one step of the market participant's decision cycle.
        
        Args:
            context: Contextual information for the current simulation step
            
        Returns:
            Dict containing the actions taken by the market participant
        """
        # Make decisions based on current state and context
        actions = self._make_decisions(context)
        
        # Update state based on actions and context
        self._update_state(actions, context)
        
        # Record history
        self._record_history(actions, context)
        
        return actions
    
    def _make_decisions(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Make decisions based on current state and context.
        
        Args:
            context: Contextual information for the current simulation step
            
        Returns:
            Dict containing the decisions made by the market participant
        """
        decisions = {}
        
        # Evaluate available products
        decisions["product_evaluations"] = self._evaluate_available_products(context)
        
        # Make purchase/adoption decisions
        decisions["purchase_decisions"] = self._make_purchase_decisions(context, decisions["product_evaluations"])
        
        # Make technology adoption decisions
        decisions["technology_adoption_decisions"] = self._make_technology_adoption_decisions(context)
        
        # Make relationship decisions
        decisions["relationship_decisions"] = self._make_relationship_decisions(context)
        
        # Make market expansion/contraction decisions
        decisions["market_decisions"] = self._make_market_decisions(context)
        
        # Make investment decisions
        decisions["investment_decisions"] = self._make_investment_decisions(context)
        
        return decisions
    
    def _update_state(self, actions: Dict[str, Any], context: Dict[str, Any]) -> None:
        """Update the market participant's state based on actions and context.
        
        Args:
            actions: Actions taken by the market participant
            context: Contextual information for the current simulation step
        """
        # Update product portfolio based on purchase decisions
        self._update_product_portfolio(actions.get("purchase_decisions", []))
        
        # Update technology adoption based on adoption decisions
        self._update_technology_adoption(actions.get("technology_adoption_decisions", []))
        
        # Update relationships based on relationship decisions
        self._update_relationships(actions.get("relationship_decisions", []), context)
        
        # Update market segments based on market decisions
        self._update_market_segments(actions.get("market_decisions", []))
        
        # Update resources based on investment decisions
        self._update_resources(actions.get("investment_decisions", []))
        
        # Update attributes based on context and actions
        self._update_attributes(actions, context)
        
        # Update satisfaction based on product evaluations and purchases
        self._update_satisfaction(actions.get("product_evaluations", []), actions.get("purchase_decisions", []))
    
    def _update_product_portfolio(self, purchase_decisions: List[Dict[str, Any]]) -> None:
        """Update the product portfolio based on purchase decisions.
        
        Args:
            purchase_decisions: List of purchase decisions
        """
        for purchase in purchase_decisions:
            product_id = purchase.get("product_id", "")
            product_name = purchase.get("product_name", "")
            quantity = purchase.get("quantity", 0)
            price = purchase.get("price_per_unit", 0)
            utility = purchase.get("utility", 0.5)
            year = purchase.get("purchase_year", 0)
            month = purchase.get("purchase_month", 1)
            
            # Add to purchase history
            self.purchase_history.append(purchase)
            
            # Update product portfolio
            if product_id in self.product_portfolio:
                # Update existing product
                self.product_portfolio[product_id]["quantity"] = quantity
                self.product_portfolio[product_id]["last_purchase_price"] = price
                self.product_portfolio[product_id]["last_purchase_year"] = year
                self.product_portfolio[product_id]["last_purchase_month"] = month
                self.product_portfolio[product_id]["purchase_count"] += 1
                
                # Update satisfaction based on utility
                current_satisfaction = self.product_portfolio[product_id].get("satisfaction", 50)
                new_satisfaction = current_satisfaction * 0.7 + utility * 100 * 0.3
                self.product_portfolio[product_id]["satisfaction"] = new_satisfaction
            else:
                # Add new product
                self.product_portfolio[product_id] = {
                    "product_name": product_name,
                    "quantity": quantity,
                    "first_purchase_year": year,
                    "first_purchase_month": month,
                    "last_purchase_year": year,
                    "last_purchase_month": month,
                    "last_purchase_price": price,
                    "purchase_count": 1,
                    "satisfaction": utility * 100  # Convert utility (0-1) to satisfaction (0-100)
                }
            
            # Update capital
            total_cost = purchase.get("total_cost", 0)
            self.resources["capital"] -= total_cost
    
    def _update_technology_adoption(self, adoption_decisions: List[Dict[str, Any]]) -> None:
        """Update technology adoption based on adoption decisions.
        
        Args:
            adoption_decisions: List of technology adoption decisions
        """
        for adoption in adoption_decisions:
            tech_id = adoption.get("technology_id", "")
            tech_name = adoption.get("technology_name", "")
            cost = adoption.get("adoption_cost", 0)
            year = adoption.get("adoption_year", 0)
            month = adoption.get("adoption_month", 1)
            expected_roi = adoption.get("expected_roi", 1.0)
            
            # Add to technology adoption
            self.technology_adoption[tech_id] = {
                "technology_name": tech_name,
                "adoption_year": year,
                "adoption_month": month,
                "adoption_cost": cost,
                "expected_roi": expected_roi,
                "satisfaction": 70,  # Initial satisfaction (0-100)
                "usage_level": 50,  # Initial usage level (0-100)
                "maturity": 0  # Initial maturity (0-100)
            }
            
            # Update capital
            self.resources["capital"] -= cost
            
            # Update innovation openness (adopting new tech increases openness)
            self.innovation_openness = min(100, self.innovation_openness + 2)
    
    def _update_relationships(self, relationship_decisions: List[Dict[str, Any]], context: Dict[str, Any]) -> None:
        """Update relationships based on relationship decisions and context.
        
        Args:
            relationship_decisions: List of relationship decisions
            context: Contextual information for the current simulation step
        """
        # Add new relationships
        for relationship in relationship_decisions:
            partner_id = relationship.get("partner_id", "")
            
            # Add to relationships
            self.relationships[partner_id] = relationship
        
        # Update existing relationships
        for partner_id, relationship in list(self.relationships.items()):
            # Check if relationship exists in context
            partner_exists = False
            for participant in context.get("market_participants", []):
                if participant.get("id", "") == partner_id:
                    partner_exists = True
                    break
            
            if not partner_exists:
                # Partner no longer exists, remove relationship
                del self.relationships[partner_id]
                continue
            
            # Update relationship strength based on time
            formation_year = relationship.get("formation_year", 0)
            current_year = context.get("year", 0)
            years_active = current_year - formation_year
            
            if years_active > 0:
                # Relationship strengthens over time (up to a point)
                current_strength = relationship.get("strength", 0.3)
                new_strength = min(0.9, current_strength + 0.05)  # Max 0.9, increase by 0.05 per year
                relationship["strength"] = new_strength
            
            # Randomly determine if relationship value changes
            if random.random() < 0.3:  # 30% chance per year
                current_value = relationship.get("current_value", 0.5)
                value_change = random.uniform(-0.1, 0.2)  # -10% to +20% change
                new_value = max(0.1, min(1.0, current_value + value_change))
                relationship["current_value"] = new_value
            
            # Randomly determine if relationship should be terminated
            if random.random() < 0.05:  # 5% chance per year
                current_value = relationship.get("current_value", 0.5)
                strength = relationship.get("strength", 0.3)
                
                # Lower value and strength increase termination probability
                termination_probability = 0.5 - current_value * 0.3 - strength * 0.2
                termination_probability = max(0.01, min(0.5, termination_probability))
                
                if random.random() < termination_probability:
                    # Terminate relationship
                    del self.relationships[partner_id]
    
    def _update_market_segments(self, market_decisions: List[Dict[str, Any]]) -> None:
        """Update market segments based on market decisions.
        
        Args:
            market_decisions: List of market decisions
        """
        for decision in market_decisions:
            decision_type = decision.get("decision_type", "")
            segment = decision.get("segment", "")
            
            if decision_type == "expansion" and segment not in self.market_segments:
                # Add new segment
                self.market_segments.append(segment)
                
                # Update capital
                cost = decision.get("cost", 0)
                self.resources["capital"] -= cost
            
            elif decision_type == "contraction" and segment in self.market_segments:
                # Remove segment
                self.market_segments.remove(segment)
    
    def _update_resources(self, investment_decisions: List[Dict[str, Any]]) -> None:
        """Update resources based on investment decisions.
        
        Args:
            investment_decisions: List of investment decisions
        """
        for investment in investment_decisions:
            investment_type = investment.get("investment_type", "")
            amount = investment.get("amount", 0)
            
            # Update capital
            self.resources["capital"] -= amount
            
            # Update specific resources based on investment type
            if investment_type == "infrastructure":
                infrastructure_type = investment.get("infrastructure_type", "")
                
                if self.participant_type == "farmer" and infrastructure_type == "irrigation":
                    # Improve land productivity
                    if "land_productivity" not in self.resources:
                        self.resources["land_productivity"] = 100
                    
                    self.resources["land_productivity"] = min(200, self.resources["land_productivity"] + 10)
                
                elif self.participant_type == "distributor" and infrastructure_type == "warehouse":
                    # Increase warehouse capacity
                    if "warehouse_capacity_m3" in self.resources:
                        self.resources["warehouse_capacity_m3"] *= 1.2
                
                elif self.participant_type == "retailer" and infrastructure_type == "store_renovation":
                    # Increase customer base
                    if "customer_base_size" in self.resources:
                        self.resources["customer_base_size"] *= 1.15
                
                elif self.participant_type == "processor" and infrastructure_type == "processing_equipment":
                    # Increase processing capacity
                    if "processing_capacity_tons_per_day" in self.resources:
                        self.resources["processing_capacity_tons_per_day"] *= 1.25
            
            elif investment_type == "technology":
                # Improve efficiency
                if "efficiency" not in self.resources:
                    self.resources["efficiency"] = 100
                
                self.resources["efficiency"] = min(200, self.resources["efficiency"] + 15)
                
                # Update knowledge level
                self.knowledge_level = min(100, self.knowledge_level + 5)
            
            elif investment_type == "training":
                # Improve employee productivity
                if "employee_productivity" not in self.resources:
                    self.resources["employee_productivity"] = 100
                
                self.resources["employee_productivity"] = min(200, self.resources["employee_productivity"] + 20)
                
                # Update knowledge level
                self.knowledge_level = min(100, self.knowledge_level + 10)
    
    def _update_attributes(self, actions: Dict[str, Any], context: Dict[str, Any]) -> None:
        """Update attributes based on actions and context.
        
        Args:
            actions: Actions taken by the market participant
            context: Contextual information for the current simulation step
        """
        # Get market trends from context
        market_trends = context.get("market_trends", {})
        
        # Update risk aversion based on market volatility
        market_volatility = market_trends.get("volatility", 0.0)
        if market_volatility > 0.5:
            # High volatility increases risk aversion
            self.risk_aversion = min(100, self.risk_aversion + 2)
        else:
            # Low volatility decreases risk aversion
            self.risk_aversion = max(0, self.risk_aversion - 1)
        
        # Update price sensitivity based on economic conditions
        economic_growth = market_trends.get("economic_growth", 0.0)
        if economic_growth < 0:
            # Economic contraction increases price sensitivity
            self.price_sensitivity = min(100, self.price_sensitivity + 3)
        else:
            # Economic growth decreases price sensitivity
            self.price_sensitivity = max(0, self.price_sensitivity - 1)
        
        # Update innovation openness based on technology adoption
        if actions.get("technology_adoption_decisions", []):
            # Adopting new technologies increases openness
            self.innovation_openness = min(100, self.innovation_openness + 3)
        
        # Update sustainability focus based on market trends
        sustainability_trend = market_trends.get("sustainability_trend", 0.0)
        self.sustainability_focus = min(100, max(0, self.sustainability_focus + sustainability_trend * 5))
        
        # Update knowledge level based on experience
        self.knowledge_level = min(100, self.knowledge_level + 0.5)  # Gradual increase with experience
        
        # Update social influence based on relationships
        if len(self.relationships) > 5:
            # Many relationships increase social influence
            self.social_influence = min(100, self.social_influence + 2)
        
        # Update economic status based on capital changes
        initial_capital = self.state.get("initial_capital", self.resources.get("capital", 50000))
        current_capital = self.resources.get("capital", 50000)
        capital_ratio = current_capital / initial_capital if initial_capital > 0 else 1.0
        
        if capital_ratio > 1.2:
            # Significant capital growth improves economic status
            self.economic_status = min(100, self.economic_status + 3)
        elif capital_ratio < 0.8:
            # Significant capital decline reduces economic status
            self.economic_status = max(0, self.economic_status - 3)
    
    def _update_satisfaction(self, product_evaluations: List[Dict[str, Any]], purchase_decisions: List[Dict[str, Any]]) -> None:
        """Update satisfaction based on product evaluations and purchases.
        
        Args:
            product_evaluations: List of product evaluations
            purchase_decisions: List of purchase decisions
        """
        if not product_evaluations:
            return
        
        # Calculate average utility of evaluated products
        total_utility = sum(evaluation.get("adjusted_utility", 0) for evaluation in product_evaluations)
        avg_utility = total_utility / len(product_evaluations) if product_evaluations else 0
        
        # Calculate average utility of purchased products
        purchased_utilities = [purchase.get("utility", 0) for purchase in purchase_decisions]
        avg_purchased_utility = sum(purchased_utilities) / len(purchased_utilities) if purchased_utilities else 0
        
        # Update satisfaction based on available and purchased products
        if purchase_decisions:
            # If purchases were made, weight purchased utility more heavily
            new_satisfaction = avg_utility * 30 + avg_purchased_utility * 70
        else:
            # If no purchases were made, satisfaction may decrease
            new_satisfaction = self.satisfaction * 0.9 + avg_utility * 10
        
        # Update satisfaction (0-100 scale)
        self.satisfaction = min(100, max(0, new_satisfaction))
    
    def _record_history(self, actions: Dict[str, Any], context: Dict[str, Any]) -> None:
        """Record history of actions and state.
        
        Args:
            actions: Actions taken by the market participant
            context: Contextual information for the current simulation step
        """
        # Create history entry
        entry = {
            "year": context.get("year", 0),
            "month": context.get("month", 1),
            "actions": actions,
            "state": {
                "market_segments": self.market_segments.copy(),
                "technology_adoption": {k: v.copy() for k, v in self.technology_adoption.items()},
                "product_portfolio": {k: v.copy() for k, v in self.product_portfolio.items()},
                "relationships": {k: v.copy() for k, v in self.relationships.items()},
                "resources": self.resources.copy(),
                "risk_aversion": self.risk_aversion,
                "price_sensitivity": self.price_sensitivity,
                "innovation_openness": self.innovation_openness,
                "sustainability_focus": self.sustainability_focus,
                "knowledge_level": self.knowledge_level,
                "social_influence": self.social_influence,
                "economic_status": self.economic_status,
                "satisfaction": self.satisfaction
            }
        }
        
        # Add to history
        self.history.append(entry)
        
        # Update state with initial capital if not set
        if "initial_capital" not in self.state:
            self.state["initial_capital"] = self.resources.get("capital", 50000)
    
    def _evaluate_available_products(self, context: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Evaluate available products in the market.
        
        Args:
            context: Contextual information for the current simulation step
            
        Returns:
            List of product evaluations
        """
        evaluations = []
        
        # Get available products from context
        available_products = context.get("available_products", [])
        
        # Filter products relevant to this participant's market segments
        relevant_products = []
        for product in available_products:
            product_segments = product.get("market_segments", [])
            if any(segment in self.market_segments for segment in product_segments):
                relevant_products.append(product)
        
        # Evaluate each relevant product
        for product in relevant_products:
            # Calculate base utility
            utility = self._calculate_product_utility(product)
            
            # Adjust utility based on social influence
            social_adjustment = self._calculate_social_influence_adjustment(product, context)
            adjusted_utility = utility * (1 + social_adjustment)
            
            # Create evaluation record
            evaluation = {
                "product_id": product.get("id", ""),
                "product_name": product.get("name", ""),
                "product_type": product.get("type", ""),
                "manufacturer_id": product.get("manufacturer_id", ""),
                "base_utility": utility,
                "social_adjustment": social_adjustment,
                "adjusted_utility": adjusted_utility,
                "evaluation_year": context.get("year", 0),
                "evaluation_month": context.get("month", 1)
            }
            
            evaluations.append(evaluation)
        
        # Sort evaluations by adjusted utility (descending)
        evaluations.sort(key=lambda x: x.get("adjusted_utility", 0), reverse=True)
        
        return evaluations
    
    def _calculate_product_utility(self, product: Dict[str, Any]) -> float:
        """Calculate the utility of a product for this participant.
        
        Args:
            product: The product to evaluate
            
        Returns:
            Float representing the utility of the product
        """
        # Get product attributes
        price = product.get("price", 100)
        quality = product.get("quality", 50)
        innovation_level = product.get("innovation_level", 50)
        sustainability_level = product.get("sustainability_level", 50)
        reliability = product.get("reliability", 50)
        brand_reputation = product.get("brand_reputation", 50)
        is_gmo = product.get("is_gmo", False)
        is_local = product.get("region", "") == self.region
        
        # Get participant preferences
        price_importance = self.preferences.get("price_importance", 0.5)
        quality_importance = self.preferences.get("quality_importance", 0.5)
        innovation_importance = self.preferences.get("innovation_importance", 0.5)
        sustainability_importance = self.preferences.get("sustainability_importance", 0.5)
        reliability_importance = self.preferences.get("reliability_importance", 0.5)
        brand_loyalty = self.preferences.get("brand_loyalty", 0.5)
        local_preference = self.preferences.get("local_preference", 0.5)
        gmo_acceptance = self.preferences.get("gmo_acceptance", 0.5)
        
        # Calculate price utility (inverse relationship - lower price = higher utility)
        max_price = product.get("max_market_price", price * 2)
        min_price = product.get("min_market_price", price * 0.5)
        price_range = max_price - min_price
        if price_range > 0:
            price_utility = 1 - ((price - min_price) / price_range)
        else:
            price_utility = 0.5
        
        # Adjust price utility based on economic status
        economic_factor = self.economic_status / 50.0  # 1.0 at economic_status 50
        price_utility = price_utility * (2 - economic_factor)  # Lower economic status = higher price sensitivity
        
        # Calculate other utilities (direct relationship - higher value = higher utility)
        quality_utility = quality / 100.0
        innovation_utility = innovation_level / 100.0
        sustainability_utility = sustainability_level / 100.0
        reliability_utility = reliability / 100.0
        brand_utility = brand_reputation / 100.0
        local_utility = 1.0 if is_local else 0.0
        
        # Calculate GMO utility
        if is_gmo:
            gmo_utility = gmo_acceptance
        else:
            gmo_utility = 1.0  # Non-GMO products have neutral impact
        
        # Calculate weighted utility
        utility = (
            price_utility * price_importance +
            quality_utility * quality_importance +
            innovation_utility * innovation_importance +
            sustainability_utility * sustainability_importance +
            reliability_utility * reliability_importance +
            brand_utility * brand_loyalty +
            local_utility * local_preference +
            gmo_utility * (innovation_importance if is_gmo else 0.0)
        )
        
        # Add participant-specific utility factors
        if self.participant_type == "farmer":
            # Farmers care about yield, pest resistance, etc.
            yield_improvement = product.get("yield_improvement", 0)
            pest_resistance = product.get("pest_resistance", 0)
            drought_tolerance = product.get("drought_tolerance", 0)
            ease_of_use = product.get("ease_of_use", 50)
            
            yield_importance = self.preferences.get("yield_importance", 0.5)
            pest_resistance_importance = self.preferences.get("pest_resistance_importance", 0.5)
            drought_tolerance_importance = self.preferences.get("drought_tolerance_importance", 0.5)
            ease_of_use_importance = self.preferences.get("ease_of_use_importance", 0.5)
            
            farmer_utility = (
                (yield_improvement / 100.0) * yield_importance +
                (pest_resistance / 100.0) * pest_resistance_importance +
                (drought_tolerance / 100.0) * drought_tolerance_importance +
                (ease_of_use / 100.0) * ease_of_use_importance
            )
            
            utility += farmer_utility
        
        elif self.participant_type == "distributor" or self.participant_type == "retailer":
            # Distributors and retailers care about margins, demand, shelf life, etc.
            margin = product.get("margin", 20)
            market_demand = product.get("market_demand", 50)
            shelf_life = product.get("shelf_life", 50)
            
            margin_importance = self.preferences.get("margin_importance", 0.5)
            market_demand_importance = self.preferences.get(
                "market_demand_importance" if self.participant_type == "retailer" else "market_demand_importance", 0.5
            )
            shelf_life_importance = self.preferences.get("shelf_life_importance", 0.5)
            
            distribution_utility = (
                (margin / 100.0) * margin_importance +
                (market_demand / 100.0) * market_demand_importance +
                (shelf_life / 100.0) * shelf_life_importance
            )
            
            utility += distribution_utility
        
        elif self.participant_type == "consumer":
            # Consumers care about taste, health, convenience, etc.
            taste = product.get("taste", 50)
            health_benefits = product.get("health_benefits", 50)
            convenience = product.get("convenience", 50)
            appearance = product.get("appearance", 50)
            novelty = product.get("novelty", 50)
            
            taste_importance = self.preferences.get("taste_importance", 0.5)
            health_importance = self.preferences.get("health_importance", 0.5)
            convenience_importance = self.preferences.get("convenience_importance", 0.5)
            appearance_importance = self.preferences.get("appearance_importance", 0.5)
            novelty_importance = self.preferences.get("novelty_importance", 0.5)
            
            consumer_utility = (
                (taste / 100.0) * taste_importance +
                (health_benefits / 100.0) * health_importance +
                (convenience / 100.0) * convenience_importance +
                (appearance / 100.0) * appearance_importance +
                (novelty / 100.0) * novelty_importance
            )
            
            utility += consumer_utility
        
        elif self.participant_type == "processor":
            # Processors care about consistency, processing efficiency, etc.
            consistency = product.get("consistency", 50)
            processing_efficiency = product.get("processing_efficiency", 50)
            ingredient_quality = product.get("ingredient_quality", 50)
            
            consistency_importance = self.preferences.get("consistency_importance", 0.5)
            processing_efficiency_importance = self.preferences.get("processing_efficiency_importance", 0.5)
            ingredient_quality_importance = self.preferences.get("ingredient_quality_importance", 0.5)
            
            processor_utility = (
                (consistency / 100.0) * consistency_importance +
                (processing_efficiency / 100.0) * processing_efficiency_importance +
                (ingredient_quality / 100.0) * ingredient_quality_importance
            )
            
            utility += processor_utility
        
        # Normalize utility to 0-1 range
        utility = max(0.0, min(1.0, utility / 2.0))  # Divide by 2 because we added participant-specific utility
        
        return utility
    
    def _calculate_social_influence_adjustment(self, product: Dict[str, Any], context: Dict[str, Any]) -> float:
        """Calculate the social influence adjustment for a product.
        
        Args:
            product: The product to evaluate
            context: Contextual information for the current simulation step
            
        Returns:
            Float representing the social influence adjustment
        """
        # Get product adoption information from context
        product_id = product.get("id", "")
        adoption_data = context.get("product_adoption_data", {}).get(product_id, {})
        
        # Get adoption rates by participant type
        farmer_adoption = adoption_data.get("farmer_adoption_rate", 0.0)
        distributor_adoption = adoption_data.get("distributor_adoption_rate", 0.0)
        retailer_adoption = adoption_data.get("retailer_adoption_rate", 0.0)
        consumer_adoption = adoption_data.get("consumer_adoption_rate", 0.0)
        processor_adoption = adoption_data.get("processor_adoption_rate", 0.0)
        
        # Calculate influence based on participant type
        if self.participant_type == "farmer":
            # Farmers are influenced by other farmers and distributors
            influence = farmer_adoption * 0.7 + distributor_adoption * 0.3
        
        elif self.participant_type == "distributor":
            # Distributors are influenced by farmers, retailers, and other distributors
            influence = farmer_adoption * 0.3 + distributor_adoption * 0.4 + retailer_adoption * 0.3
        
        elif self.participant_type == "retailer":
            # Retailers are influenced by consumers, distributors, and other retailers
            influence = consumer_adoption * 0.4 + distributor_adoption * 0.3 + retailer_adoption * 0.3
        
        elif self.participant_type == "consumer":
            # Consumers are influenced by retailers and other consumers
            influence = retailer_adoption * 0.3 + consumer_adoption * 0.7
        
        elif self.participant_type == "processor":
            # Processors are influenced by farmers, distributors, and other processors
            influence = farmer_adoption * 0.3 + distributor_adoption * 0.3 + processor_adoption * 0.4
        
        else:
            influence = 0.0
        
        # Adjust influence based on social influence susceptibility
        social_susceptibility = self.social_influence / 100.0
        adjustment = influence * social_susceptibility
        
        # Cap adjustment
        adjustment = max(-0.5, min(0.5, adjustment))  # -50% to +50% adjustment
        
        return adjustment
    
    def _make_purchase_decisions(self, context: Dict[str, Any], evaluations: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Make purchase decisions based on product evaluations.
        
        Args:
            context: Contextual information for the current simulation step
            evaluations: List of product evaluations
            
        Returns:
            List of purchase decisions
        """
        decisions = []
        
        # Get budget constraints
        if self.participant_type == "consumer":
            budget = self.resources.get("annual_food_budget", 5000) / 12.0  # Monthly budget
        else:
            budget = self.resources.get("capital", 50000) * 0.1  # 10% of capital for purchases
        
        # Track remaining budget
        remaining_budget = budget
        
        # Consider top-rated products first
        for evaluation in evaluations:
            product_id = evaluation.get("product_id", "")
            product_name = evaluation.get("product_name", "")
            utility = evaluation.get("adjusted_utility", 0.0)
            
            # Get product details from context
            product = None
            for p in context.get("available_products", []):
                if p.get("id", "") == product_id:
                    product = p
                    break
            
            if not product:
                continue
            
            # Get product price
            price = product.get("price", 100)
            
            # Check if already using/selling this product
            already_adopted = product_id in self.product_portfolio
            
            # Calculate purchase probability
            base_probability = utility
            
            # Adjust probability based on risk aversion
            risk_factor = 1.0 - (self.risk_aversion / 100.0)  # Higher risk aversion = lower probability
            adjusted_probability = base_probability * risk_factor
            
            # Adjust probability based on already adopted status
            if already_adopted:
                # Much higher probability of continuing to use a product
                current_satisfaction = self.product_portfolio[product_id].get("satisfaction", 50) / 100.0
                adjusted_probability = 0.7 * current_satisfaction + 0.3 * adjusted_probability
            
            # Decide whether to purchase
            if random.random() < adjusted_probability:
                # Check budget
                quantity = 1
                if self.participant_type == "farmer":
                    # Farmers buy based on land area
                    land_hectares = self.resources.get("land_hectares", 50)
                    if product.get("type", "") == "seed":
                        quantity = land_hectares * 0.1  # 0.1 units per hectare
                    elif product.get("type", "") in ["fertilizer", "pesticide"]:
                        quantity = land_hectares * 0.2  # 0.2 units per hectare
                    else:
                        quantity = 1
                
                elif self.participant_type in ["distributor", "retailer"]:
                    # Distributors and retailers buy in bulk
                    if self.size == "small":
                        quantity = random.randint(10, 50)
                    elif self.size == "medium":
                        quantity = random.randint(50, 200)
                    else:  # large
                        quantity = random.randint(200, 1000)
                
                elif self.participant_type == "processor":
                    # Processors buy based on processing capacity
                    capacity = self.resources.get("processing_capacity_tons_per_day", 50)
                    quantity = capacity * 30 * 0.1  # 10% of monthly capacity
                
                # Calculate total cost
                total_cost = price * quantity
                
                # Check if affordable
                if total_cost <= remaining_budget:
                    # Make purchase
                    purchase = {
                        "product_id": product_id,
                        "product_name": product_name,
                        "quantity": quantity,
                        "price_per_unit": price,
                        "total_cost": total_cost,
                        "utility": utility,
                        "purchase_year": context.get("year", 0),
                        "purchase_month": context.get("month", 1)
                    }
                    
                    decisions.append(purchase)
                    
                    # Update remaining budget
                    remaining_budget -= total_cost
        
        return decisions
    
    def _make_technology_adoption_decisions(self, context: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Make technology adoption decisions.
        
        Args:
            context: Contextual information for the current simulation step
            
        Returns:
            List of technology adoption decisions
        """
        decisions = []
        
        # Get available technologies from context
        available_technologies = context.get("available_technologies", [])
        
        # Filter technologies relevant to this participant's type
        relevant_technologies = []
        for tech in available_technologies:
            tech_participant_types = tech.get("relevant_participant_types", [])
            if self.participant_type in tech_participant_types:
                relevant_technologies.append(tech)
        
        # Evaluate each relevant technology
        for tech in relevant_technologies:
            tech_id = tech.get("id", "")
            tech_name = tech.get("name", "")
            
            # Check if already adopted
            already_adopted = tech_id in self.technology_adoption
            
            if not already_adopted:
                # Calculate adoption probability
                base_probability = self.innovation_openness / 100.0
                
                # Adjust based on technology attributes
                tech_complexity = tech.get("complexity", 50) / 100.0
                tech_cost = tech.get("adoption_cost", 10000)
                tech_roi = tech.get("expected_roi", 1.5)
                tech_compatibility = tech.get("compatibility", 50) / 100.0
                
                # Complexity reduces probability (more for less knowledgeable participants)
                knowledge_factor = self.knowledge_level / 100.0
                complexity_adjustment = -tech_complexity * (1 - knowledge_factor)
                
                # Cost reduces probability (more for less economically strong participants)
                economic_factor = self.economic_status / 100.0
                cost_adjustment = -0.2 * (tech_cost / (self.resources.get("capital", 50000) * economic_factor))
                cost_adjustment = max(-0.5, cost_adjustment)  # Cap at -0.5
                
                # ROI increases probability
                roi_adjustment = 0.2 * (tech_roi - 1.0)
                
                # Compatibility increases probability
                compatibility_adjustment = 0.3 * tech_compatibility
                
                # Calculate adjusted probability
                adjusted_probability = base_probability + complexity_adjustment + cost_adjustment + roi_adjustment + compatibility_adjustment
                adjusted_probability = max(0.01, min(0.99, adjusted_probability))  # Cap between 0.01 and 0.99
                
                # Decide whether to adopt
                if random.random() < adjusted_probability:
                    # Check if affordable
                    if tech_cost <= self.resources.get("capital", 50000):
                        # Adopt technology
                        adoption = {
                            "technology_id": tech_id,
                            "technology_name": tech_name,
                            "adoption_cost": tech_cost,
                            "adoption_year": context.get("year", 0),
                            "adoption_month": context.get("month", 1),
                            "expected_roi": tech_roi
                        }
                        
                        decisions.append(adoption)
        
        return decisions
    
    def _make_relationship_decisions(self, context: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Make decisions about relationships with other market participants.
        
        Args:
            context: Contextual information for the current simulation step
            
        Returns:
            List of relationship decisions
        """
        decisions = []
        
        # Get potential relationship partners from context
        potential_partners = context.get("market_participants", [])
        
        # Filter out self and existing relationships
        potential_partners = [
            p for p in potential_partners 
            if p.get("id", "") != self.id and p.get("id", "") not in self.relationships
        ]
        
        # Determine number of new relationships to form
        if self.size == "small":
            max_new_relationships = 1
        elif self.size == "medium":
            max_new_relationships = 2
        else:  # large
            max_new_relationships = 3
        
        # Randomly select potential partners to evaluate
        if potential_partners:
            selected_partners = random.sample(
                potential_partners, 
                min(max_new_relationships * 3, len(potential_partners))
            )
            
            # Evaluate each potential partner
            for partner in selected_partners:
                partner_id = partner.get("id", "")
                partner_name = partner.get("name", "")
                partner_type = partner.get("participant_type", "")
                partner_size = partner.get("size", "medium")
                partner_region = partner.get("region", "")
                
                # Calculate relationship value
                value = self._calculate_relationship_value(partner)
                
                # Calculate formation probability
                base_probability = 0.3  # 30% base probability
                
                # Adjust based on value
                value_adjustment = value * 0.5  # Up to 50% increase
                
                # Adjust based on region (prefer same region)
                region_adjustment = 0.2 if partner_region == self.region else 0.0
                
                # Calculate adjusted probability
                adjusted_probability = base_probability + value_adjustment + region_adjustment
                adjusted_probability = max(0.0, min(0.9, adjusted_probability))  # Cap at 90%
                
                # Decide whether to form relationship
                if random.random() < adjusted_probability:
                    # Form relationship
                    relationship = {
                        "partner_id": partner_id,
                        "partner_name": partner_name,
                        "partner_type": partner_type,
                        "partner_size": partner_size,
                        "relationship_type": self._determine_relationship_type(partner_type),
                        "formation_year": context.get("year", 0),
                        "formation_month": context.get("month", 1),
                        "initial_value": value,
                        "current_value": value,
                        "strength": 0.3  # Initial strength (0.0-1.0)
                    }
                    
                    decisions.append(relationship)
                    
                    # Limit number of new relationships
                    if len(decisions) >= max_new_relationships:
                        break
        
        return decisions
    
    def _calculate_relationship_value(self, partner: Dict[str, Any]) -> float:
        """Calculate the value of a relationship with a potential partner.
        
        Args:
            partner: The potential partner
            
        Returns:
            Float representing the value of the relationship (0.0-1.0)
        """
        partner_type = partner.get("participant_type", "")
        
        # Value depends on participant types
        if self.participant_type == "farmer":
            if partner_type == "distributor":
                # Distributors provide market access for farmers
                return generate_triangular(0.6, 0.8, 0.9)
            elif partner_type == "processor":
                # Processors are direct buyers for farmers
                return generate_triangular(0.7, 0.8, 0.9)
            elif partner_type == "retailer":
                # Direct-to-retail relationships can be valuable but less common
                return generate_triangular(0.5, 0.7, 0.8)
            elif partner_type == "farmer":
                # Farmer cooperatives and knowledge sharing
                return generate_triangular(0.4, 0.6, 0.8)
            else:
                return generate_triangular(0.1, 0.3, 0.5)
        
        elif self.participant_type == "distributor":
            if partner_type == "farmer":
                # Farmers are suppliers for distributors
                return generate_triangular(0.6, 0.7, 0.8)
            elif partner_type == "retailer":
                # Retailers are customers for distributors
                return generate_triangular(0.7, 0.8, 0.9)
            elif partner_type == "processor":
                # Processors can be both suppliers and customers
                return generate_triangular(0.6, 0.7, 0.8)
            elif partner_type == "distributor":
                # Partnerships with other distributors
                return generate_triangular(0.3, 0.5, 0.7)
            else:
                return generate_triangular(0.1, 0.3, 0.5)
        
        elif self.participant_type == "retailer":
            if partner_type == "distributor":
                # Distributors are suppliers for retailers
                return generate_triangular(0.7, 0.8, 0.9)
            elif partner_type == "consumer":
                # Consumer relationships (loyalty programs, etc.)
                return generate_triangular(0.6, 0.7, 0.8)
            elif partner_type == "farmer":
                # Direct farm-to-retail relationships
                return generate_triangular(0.5, 0.6, 0.7)
            elif partner_type == "retailer":
                # Partnerships with other retailers
                return generate_triangular(0.2, 0.4, 0.6)
            else:
                return generate_triangular(0.1, 0.3, 0.5)
        
        elif self.participant_type == "consumer":
            if partner_type == "retailer":
                # Retailers are primary suppliers for consumers
                return generate_triangular(0.6, 0.7, 0.8)
            elif partner_type == "farmer":
                # Direct farm-to-consumer relationships
                return generate_triangular(0.5, 0.6, 0.7)
            elif partner_type == "consumer":
                # Consumer groups and communities
                return generate_triangular(0.3, 0.5, 0.7)
            else:
                return generate_triangular(0.1, 0.3, 0.5)
        
        elif self.participant_type == "processor":
            if partner_type == "farmer":
                # Farmers are suppliers for processors
                return generate_triangular(0.7, 0.8, 0.9)
            elif partner_type == "distributor":
                # Distributors help processors reach markets
                return generate_triangular(0.6, 0.7, 0.8)
            elif partner_type == "retailer":
                # Direct processor-to-retail relationships
                return generate_triangular(0.5, 0.7, 0.8)
            elif partner_type == "processor":
                # Partnerships with other processors
                return generate_triangular(0.3, 0.5, 0.7)
            else:
                return generate_triangular(0.1, 0.3, 0.5)
        
        else:
            return generate_triangular(0.1, 0.3, 0.5)
    
    def _determine_relationship_type(self, partner_type: str) -> str:
        """Determine the type of relationship based on participant types.
        
        Args:
            partner_type: The type of the partner
            
        Returns:
            String representing the relationship type
        """
        if self.participant_type == "farmer":
            if partner_type == "distributor":
                return "supplier_buyer"
            elif partner_type == "processor":
                return "supplier_buyer"
            elif partner_type == "retailer":
                return "supplier_buyer"
            elif partner_type == "farmer":
                return "cooperative"
            else:
                return "general"
        
        elif self.participant_type == "distributor":
            if partner_type == "farmer":
                return "buyer_supplier"
            elif partner_type == "retailer":
                return "supplier_buyer"
            elif partner_type == "processor":
                return "mixed"
            elif partner_type == "distributor":
                return "partnership"
            else:
                return "general"
        
        elif self.participant_type == "retailer":
            if partner_type == "distributor":
                return "buyer_supplier"
            elif partner_type == "consumer":
                return "seller_buyer"
            elif partner_type == "farmer":
                return "buyer_supplier"
            elif partner_type == "retailer":
                return "partnership"
            else:
                return "general"
        
        elif self.participant_type == "consumer":
            if partner_type == "retailer":
                return "buyer_seller"
            elif partner_type == "farmer":
                return "buyer_seller"
            elif partner_type == "consumer":
                return "community"
            else:
                return "general"
        
        elif self.participant_type == "processor":
            if partner_type == "farmer":
                return "buyer_supplier"
            elif partner_type == "distributor":
                return "mixed"
            elif partner_type == "retailer":
                return "supplier_buyer"
            elif partner_type == "processor":
                return "partnership"
            else:
                return "general"
        
        else:
            return "general"
    
    def _make_market_decisions(self, context: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Make decisions about market expansion or contraction.
        
        Args:
            context: Contextual information for the current simulation step
            
        Returns:
            List of market decisions
        """
        decisions = []
        
        # Skip for consumers (they don't make market expansion decisions)
        if self.participant_type == "consumer":
            return decisions
        
        # Get market trends from context
        market_trends = context.get("market_trends", {})
        
        # Consider expanding into new market segments
        possible_segments = self._get_possible_market_segments()
        
        # Filter out segments already in portfolio
        new_segments = [s for s in possible_segments if s not in self.market_segments]
        
        # Determine number of segments to consider
        if self.size == "small":
            max_new_segments = 1
        elif self.size == "medium":
            max_new_segments = 2
        else:  # large
            max_new_segments = 3
        
        # Randomly select segments to evaluate
        if new_segments:
            selected_segments = random.sample(
                new_segments, 
                min(max_new_segments * 2, len(new_segments))
            )
            
            # Evaluate each potential segment
            for segment in selected_segments:
                # Get segment growth rate from market trends
                growth_rate = market_trends.get("segment_growth", {}).get(segment, 0.0)
                
                # Calculate expansion probability
                base_probability = 0.2  # 20% base probability
                
                # Adjust based on growth rate
                growth_adjustment = growth_rate * 0.5  # Up to 50% increase for high growth
                
                # Adjust based on innovation openness
                innovation_adjustment = (self.innovation_openness - 50) / 100.0 * 0.2  # +/- 20%
                
                # Adjust based on risk aversion (inverse relationship)
                risk_adjustment = (50 - self.risk_aversion) / 100.0 * 0.2  # +/- 20%
                
                # Calculate adjusted probability
                adjusted_probability = base_probability + growth_adjustment + innovation_adjustment + risk_adjustment
                adjusted_probability = max(0.05, min(0.8, adjusted_probability))  # Cap between 5% and 80%
                
                # Decide whether to expand
                if random.random() < adjusted_probability:
                    # Calculate expansion cost
                    if self.participant_type == "farmer":
                        cost = self.resources.get("capital", 50000) * 0.2  # 20% of capital
                    elif self.participant_type in ["distributor", "retailer", "processor"]:
                        cost = self.resources.get("capital", 50000) * 0.3  # 30% of capital
                    else:
                        cost = 0
                    
                    # Check if affordable
                    if cost <= self.resources.get("capital", 50000):
                        # Expand into segment
                        expansion = {
                            "decision_type": "expansion",
                            "segment": segment,
                            "cost": cost,
                            "expected_growth": growth_rate,
                            "decision_year": context.get("year", 0),
                            "decision_month": context.get("month", 1)
                        }
                        
                        decisions.append(expansion)
        
        # Consider contracting from existing segments
        for segment in self.market_segments:
            # Skip if only one segment (need to maintain at least one)
            if len(self.market_segments) <= 1:
                break
            
            # Get segment growth rate from market trends
            growth_rate = market_trends.get("segment_growth", {}).get(segment, 0.0)
            
            # Calculate contraction probability
            base_probability = 0.1  # 10% base probability
            
            # Adjust based on growth rate (negative growth increases probability)
            growth_adjustment = -growth_rate * 0.5  # Up to 50% increase for negative growth
            
            # Calculate adjusted probability
            adjusted_probability = base_probability + growth_adjustment
            adjusted_probability = max(0.01, min(0.5, adjusted_probability))  # Cap between 1% and 50%
            
            # Decide whether to contract
            if random.random() < adjusted_probability:
                # Contract from segment
                contraction = {
                    "decision_type": "contraction",
                    "segment": segment,
                    "decision_year": context.get("year", 0),
                    "decision_month": context.get("month", 1)
                }
                
                decisions.append(contraction)
        
        return decisions
    
    def _get_possible_market_segments(self) -> List[str]:
        """Get possible market segments for this participant type.
        
        Returns:
            List of possible market segments
        """
        if self.participant_type == "farmer":
            return [
                "grain_crops", "oilseed_crops", "fiber_crops", "fruit_crops", 
                "vegetable_crops", "specialty_crops", "organic_farming"
            ]
        
        elif self.participant_type == "distributor":
            return [
                "seeds", "fertilizers", "pesticides", "agricultural_equipment", 
                "raw_agricultural_products", "processed_food_ingredients"
            ]
        
        elif self.participant_type == "retailer":
            return [
                "supermarket", "specialty_food_store", "farmers_market", 
                "online_retail", "convenience_store", "wholesale_club"
            ]
        
        elif self.participant_type == "processor":
            return [
                "grain_processing", "dairy_processing", "meat_processing", 
                "fruit_and_vegetable_processing", "beverage_production", 
                "snack_food_production", "specialty_food_production"
            ]
        
        else:
            return []
    
    def _make_investment_decisions(self, context: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Make investment decisions.
        
        Args:
            context: Contextual information for the current simulation step
            
        Returns:
            List of investment decisions
        """
        decisions = []
        
        # Skip for consumers (they don't make investment decisions)
        if self.participant_type == "consumer":
            return decisions
        
        # Get available capital
        capital = self.resources.get("capital", 50000)
        
        # Determine investment budget (percentage of capital)
        if self.size == "small":
            investment_budget = capital * 0.1  # 10% of capital
        elif self.size == "medium":
            investment_budget = capital * 0.15  # 15% of capital
        else:  # large
            investment_budget = capital * 0.2  # 20% of capital
        
        # Adjust based on risk aversion
        risk_factor = 1.0 - (self.risk_aversion / 100.0)  # Higher risk aversion = lower budget
        investment_budget *= risk_factor
        
        # Track remaining budget
        remaining_budget = investment_budget
        
        # Consider infrastructure investments
        if remaining_budget > 0 and random.random() < 0.5:  # 50% chance
            # Calculate investment amount
            amount = remaining_budget * random.uniform(0.3, 0.7)  # 30-70% of budget
            
            # Determine infrastructure type
            if self.participant_type == "farmer":
                infrastructure_types = ["irrigation", "storage", "equipment"]
            elif self.participant_type == "distributor":
                infrastructure_types = ["warehouse", "logistics", "tracking_systems"]
            elif self.participant_type == "retailer":
                infrastructure_types = ["store_renovation", "inventory_systems", "customer_experience"]
            elif self.participant_type == "processor":
                infrastructure_types = ["processing_equipment", "quality_control", "automation"]
            else:
                infrastructure_types = ["general"]
            
            infrastructure_type = random.choice(infrastructure_types)
            
            # Make investment
            investment = {
                "investment_type": "infrastructure",
                "infrastructure_type": infrastructure_type,
                "amount": amount,
                "expected_roi": random.uniform(1.1, 1.5),  # 10-50% ROI
                "investment_year": context.get("year", 0),
                "investment_month": context.get("month", 1)
            }
            
            decisions.append(investment)
            
            # Update remaining budget
            remaining_budget -= amount
        
        # Consider technology investments
        if remaining_budget > 0 and random.random() < 0.4:  # 40% chance
            # Calculate investment amount
            amount = remaining_budget * random.uniform(0.3, 0.7)  # 30-70% of budget
            
            # Determine technology type
            if self.participant_type == "farmer":
                technology_types = ["precision_agriculture", "farm_management_software", "sustainable_practices"]
            elif self.participant_type == "distributor":
                technology_types = ["inventory_management", "route_optimization", "blockchain_traceability"]
            elif self.participant_type == "retailer":
                technology_types = ["pos_systems", "customer_analytics", "e_commerce"]
            elif self.participant_type == "processor":
                technology_types = ["automation", "quality_control", "energy_efficiency"]
            else:
                technology_types = ["general"]
            
            technology_type = random.choice(technology_types)
            
            # Make investment
            investment = {
                "investment_type": "technology",
                "technology_type": technology_type,
                "amount": amount,
                "expected_roi": random.uniform(1.2, 1.8),  # 20-80% ROI
                "investment_year": context.get("year", 0),
                "investment_month": context.get("month", 1)
            }
            
            decisions.append(investment)
            
            # Update remaining budget
            remaining_budget -= amount
        
        # Consider training/skills investments
        if remaining_budget > 0 and random.random() < 0.3:  # 30% chance
            # Calculate investment amount
            amount = remaining_budget * random.uniform(0.2, 0.5)  # 20-50% of budget
            
            # Make investment
            investment = {
                "investment_type": "training",
                "amount": amount,
                "expected_roi": random.uniform(1.1, 1.4),  # 10-40% ROI
                "investment_year": context.get("year", 0),
                "investment_month": context.get("month", 1)
            }
            
            decisions.append(investment)
            
            # Update remaining budget
            remaining_budget -= amount
        
        return decisions