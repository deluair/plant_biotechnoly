#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Commercial player agent class for the BIOSIMULATE project.

This module defines the CommercialPlayer class that represents companies,
startups, and other commercial entities in the plant biotechnology industry.
"""

import logging
import random
import uuid
from typing import Dict, List, Any, Optional, Set, Tuple
from dataclasses import dataclass, field

from biosimulate.agents.base_agent import BaseAgent
from biosimulate.utils.data_generator import generate_normal, generate_triangular

logger = logging.getLogger(__name__)


@dataclass
class CommercialPlayer(BaseAgent):
    """Class representing commercial entities in the simulation.
    
    Attributes:
        company_size (str): Size of the company ('startup', 'sme', 'large', 'multinational')
        market_segments (List[str]): Market segments the company operates in
        technologies (List[Dict]): Technologies in the company's portfolio
        products (List[Dict]): Products in the company's portfolio
        r_and_d_investment (float): Percentage of revenue invested in R&D (0-100)
        innovation_capacity (float): Capacity for innovation (0-100)
        market_share (Dict[str, float]): Market share in different segments
        partnerships (List[Dict]): Partnerships with other entities
        intellectual_property (List[Dict]): IP assets owned by the company
        financial_metrics (Dict): Financial performance metrics
    """
    
    company_size: str = 'sme'  # Default to small-medium enterprise
    market_segments: List[str] = field(default_factory=list)
    technologies: List[Dict] = field(default_factory=list)
    products: List[Dict] = field(default_factory=list)
    r_and_d_investment: float = 15.0  # Default 15% of revenue
    innovation_capacity: float = 50.0
    market_share: Dict[str, float] = field(default_factory=dict)
    partnerships: List[Dict] = field(default_factory=list)
    intellectual_property: List[Dict] = field(default_factory=list)
    financial_metrics: Dict[str, Any] = field(default_factory=dict)
    
    def __post_init__(self):
        """Initialize additional attributes after dataclass initialization."""
        super().__post_init__()
        
        # Set type to 'commercial' if not specified
        if self.type != 'commercial':
            self.type = 'commercial'
            logger.warning(f"Agent type overridden to 'commercial' for {self.name}")
        
        # Initialize resources if not provided
        if 'capital' not in self.resources:
            # Set initial capital based on company size
            if self.company_size == 'startup':
                self.resources['capital'] = generate_triangular(500000, 2000000, 5000000)  # 500k-5M
            elif self.company_size == 'sme':
                self.resources['capital'] = generate_triangular(5000000, 20000000, 50000000)  # 5M-50M
            elif self.company_size == 'large':
                self.resources['capital'] = generate_triangular(50000000, 200000000, 500000000)  # 50M-500M
            elif self.company_size == 'multinational':
                self.resources['capital'] = generate_triangular(500000000, 1000000000, 5000000000)  # 500M-5B
            else:
                self.resources['capital'] = 10000000  # Default 10M
        
        if 'employees' not in self.resources:
            # Set initial employees based on company size
            if self.company_size == 'startup':
                self.resources['employees'] = random.randint(5, 50)
            elif self.company_size == 'sme':
                self.resources['employees'] = random.randint(50, 500)
            elif self.company_size == 'large':
                self.resources['employees'] = random.randint(500, 5000)
            elif self.company_size == 'multinational':
                self.resources['employees'] = random.randint(5000, 50000)
            else:
                self.resources['employees'] = 100  # Default 100 employees
        
        # Initialize financial metrics if not provided
        if not self.financial_metrics:
            # Set initial financial metrics based on company size
            if self.company_size == 'startup':
                self.financial_metrics = {
                    'revenue': generate_triangular(0, 1000000, 5000000),  # 0-5M
                    'profit_margin': generate_triangular(-20, 0, 10),  # -20% to 10%
                    'r_and_d_budget': 0,  # Will be calculated
                    'marketing_budget': 0,  # Will be calculated
                    'valuation': generate_triangular(1000000, 5000000, 20000000),  # 1M-20M
                    'burn_rate': generate_triangular(50000, 200000, 500000)  # 50k-500k per month
                }
            elif self.company_size == 'sme':
                self.financial_metrics = {
                    'revenue': generate_triangular(5000000, 20000000, 100000000),  # 5M-100M
                    'profit_margin': generate_triangular(0, 10, 20),  # 0% to 20%
                    'r_and_d_budget': 0,  # Will be calculated
                    'marketing_budget': 0,  # Will be calculated
                    'valuation': generate_triangular(20000000, 50000000, 200000000),  # 20M-200M
                    'burn_rate': 0  # Not applicable for established companies
                }
            elif self.company_size == 'large':
                self.financial_metrics = {
                    'revenue': generate_triangular(100000000, 500000000, 1000000000),  # 100M-1B
                    'profit_margin': generate_triangular(5, 15, 25),  # 5% to 25%
                    'r_and_d_budget': 0,  # Will be calculated
                    'marketing_budget': 0,  # Will be calculated
                    'valuation': generate_triangular(200000000, 1000000000, 5000000000),  # 200M-5B
                    'burn_rate': 0  # Not applicable for established companies
                }
            elif self.company_size == 'multinational':
                self.financial_metrics = {
                    'revenue': generate_triangular(1000000000, 5000000000, 20000000000),  # 1B-20B
                    'profit_margin': generate_triangular(10, 20, 30),  # 10% to 30%
                    'r_and_d_budget': 0,  # Will be calculated
                    'marketing_budget': 0,  # Will be calculated
                    'valuation': generate_triangular(5000000000, 20000000000, 100000000000),  # 5B-100B
                    'burn_rate': 0  # Not applicable for established companies
                }
            else:
                self.financial_metrics = {
                    'revenue': 10000000,  # Default 10M
                    'profit_margin': 10,  # Default 10%
                    'r_and_d_budget': 0,  # Will be calculated
                    'marketing_budget': 0,  # Will be calculated
                    'valuation': 50000000,  # Default 50M
                    'burn_rate': 0  # Default 0
                }
        
        # Calculate derived financial metrics
        self._calculate_derived_financials()
        
        # Initialize state variables if not provided
        if 'r_and_d_projects' not in self.state:
            self.state['r_and_d_projects'] = []  # List of current R&D projects
        
        if 'product_development' not in self.state:
            self.state['product_development'] = []  # List of products under development
        
        if 'market_expansion' not in self.state:
            self.state['market_expansion'] = []  # List of market expansion initiatives
    
    def _calculate_derived_financials(self):
        """Calculate derived financial metrics."""
        # Calculate R&D budget based on revenue and R&D investment percentage
        revenue = self.financial_metrics.get('revenue', 0)
        self.financial_metrics['r_and_d_budget'] = revenue * (self.r_and_d_investment / 100)
        
        # Calculate marketing budget (typically 10-20% of revenue)
        marketing_percentage = generate_triangular(10, 15, 20)
        self.financial_metrics['marketing_budget'] = revenue * (marketing_percentage / 100)
        
        # Calculate profit
        profit_margin = self.financial_metrics.get('profit_margin', 0)
        self.financial_metrics['profit'] = revenue * (profit_margin / 100)
    
    def step(self, year: int, context: Dict[str, Any]) -> Dict[str, Any]:
        """Advance the commercial player by one time step (year).
        
        Args:
            year: Current simulation year
            context: Contextual information for the step
            
        Returns:
            Dictionary of actions and state changes
        """
        # Make decisions based on current state and context
        actions = self._make_decisions(year, context)
        
        # Update state based on actions and context
        self._update_state(year, actions, context)
        
        # Record history
        self._record_history(year, actions)
        
        return actions
    
    def _make_decisions(self, year: int, context: Dict[str, Any]) -> Dict[str, Any]:
        """Make decisions based on current state and context.
        
        Args:
            year: Current simulation year
            context: Contextual information for decision making
            
        Returns:
            Dictionary of decisions/actions
        """
        actions = {}
        
        # Decide on R&D projects to pursue
        actions['r_and_d_projects'] = self._decide_r_and_d_projects(context)
        
        # Decide on technology acquisition
        actions['technology_acquisition'] = self._decide_technology_acquisition(context)
        
        # Decide on product development
        product_development_initiatives = self._decide_product_development(context)
        actions['product_development'] = product_development_initiatives

        # Decide on partnerships
        actions['partnerships'] = self._decide_partnerships(context)

        # Decide on market expansion
        expansion_initiatives = self._decide_market_expansion(context)
        actions['market_expansion'] = expansion_initiatives

        # Decide on IP strategy
        actions['ip_strategy'] = self._decide_ip_strategy(context)

        # Decide on investment and funding
        actions['investment_strategy'] = self._decide_investment_strategy(
            context, expansion_initiatives, product_development_initiatives
        )
        
        return actions
    
    def _update_state(self, year: int, actions: Dict[str, Any], context: Dict[str, Any]) -> None:
        """Update agent state based on actions and context.
        
        Args:
            year: Current simulation year
            actions: Actions taken by the agent
            context: Contextual information
        """
        # Update R&D projects
        self._update_r_and_d_projects(actions, context)
        
        # Update technologies
        self._update_technologies(actions, context)
        
        # Update products
        self._update_products(actions, context)
        
        # Update partnerships
        self._update_partnerships(actions, context)
        
        # Update market presence
        self._update_market_presence(actions, context)
        
        # Update intellectual property
        self._update_intellectual_property(actions, context)
        
        # Update financial metrics
        self._update_financials(actions, context)
        
        # Update resources
        self._update_resources(context)
    
    def _decide_r_and_d_projects(self, context: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Decide on R&D projects to pursue.
        
        Args:
            context: Contextual information for decision making
            
        Returns:
            List of R&D projects to pursue
        """
        new_projects = []
        
        # Get available technologies and market trends from context
        available_technologies = context.get('available_technologies', [])
        market_trends = context.get('market_trends', {})
        
        # Filter technologies based on market segments
        relevant_technologies = [tech for tech in available_technologies 
                               if any(segment in tech.get('market_segments', []) for segment in self.market_segments)]
        
        # Determine R&D budget available for new projects
        r_and_d_budget = self.financial_metrics.get('r_and_d_budget', 0)
        current_projects = self.state.get('r_and_d_projects', [])
        committed_budget = sum(project.get('annual_budget', 0) for project in current_projects)
        available_budget = max(0, r_and_d_budget - committed_budget)
        
        # Determine number of new projects based on innovation capacity and available budget
        max_projects = max(1, int(self.innovation_capacity / 20))  # 1 project per 20 units of capacity
        num_new_projects = max(0, max_projects - len(current_projects))
        
        # Adjust based on available budget
        avg_project_cost = 500000 if self.company_size == 'startup' else 2000000  # Average cost per project
        budget_capacity = int(available_budget / avg_project_cost)
        num_new_projects = min(num_new_projects, budget_capacity)
        
        # Create new projects
        for _ in range(num_new_projects):
            # Determine project focus
            if relevant_technologies and random.random() < 0.7:  # 70% chance to focus on relevant technology
                tech = random.choice(relevant_technologies)
                focus = tech.get('name', 'Unknown Technology')
                segments = tech.get('market_segments', [])
            else:  # Otherwise, select from market segments
                focus = f"Innovation in {random.choice(self.market_segments)}" if self.market_segments else 'General R&D'
                segments = [random.choice(self.market_segments)] if self.market_segments else ['General']
            
            # Determine project parameters
            duration = random.randint(1, 3)  # 1-3 years
            
            # Budget depends on company size
            if self.company_size == 'startup':
                budget = generate_triangular(200000, 500000, 1000000)  # 200k-1M
            elif self.company_size == 'sme':
                budget = generate_triangular(500000, 2000000, 5000000)  # 500k-5M
            elif self.company_size == 'large':
                budget = generate_triangular(2000000, 5000000, 20000000)  # 2M-20M
            elif self.company_size == 'multinational':
                budget = generate_triangular(5000000, 20000000, 100000000)  # 5M-100M
            else:
                budget = 1000000  # Default 1M
            
            # Ensure budget doesn't exceed available budget
            budget = min(budget, available_budget)
            available_budget -= budget
            
            # Success probability based on innovation capacity
            base_success_prob = 0.3 + (self.innovation_capacity / 200)  # 0.3-0.8 based on capacity
            
            # Adjust based on market trends if available
            trend_factor = 1.0
            for segment in segments:
                if segment in market_trends:
                    trend = market_trends[segment]
                    if trend > 0:
                        trend_factor = 1.0 + (trend / 10)  # Up to 1.5x for strong positive trends
                    else:
                        trend_factor = 1.0 / (1.0 - (trend / 20))  # Down to 0.67x for strong negative trends
            
            success_probability = min(0.9, max(0.1, base_success_prob * trend_factor))
            
            # Create project
            project = {
                'name': f"{focus} R&D Project",
                'focus': focus,
                'market_segments': segments,
                'start_year': context.get('year', 0),
                'duration': duration,
                'total_budget': budget,
                'annual_budget': budget / duration,
                'success_probability': success_probability,
                'progress': 0.0,  # 0-100%
                'expected_roi': generate_triangular(1.5, 3.0, 10.0),  # Expected return on investment
                'collaborators': []
            }
            
            new_projects.append(project)
        
        return new_projects
    
    def _decide_technology_acquisition(self, context: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Decide on technology acquisitions.
        
        Args:
            context: Contextual information for decision making
            
        Returns:
            List of technology acquisitions to pursue
        """
        acquisitions = []
        
        # Get available technologies from context
        available_technologies = context.get('available_technologies', [])
        research_entities = context.get('research_entities', [])
        commercial_players = context.get('commercial_players', [])
        
        # Filter technologies based on market segments and maturity
        relevant_technologies = [tech for tech in available_technologies 
                               if any(segment in tech.get('market_segments', []) for segment in self.market_segments)
                               and tech.get('maturity', 0) >= 0.5]  # Only consider mature technologies
        
        # Determine acquisition budget (typically 20-40% of R&D budget for acquisitions)
        r_and_d_budget = self.financial_metrics.get('r_and_d_budget', 0)
        acquisition_budget = r_and_d_budget * generate_triangular(0.2, 0.3, 0.4)
        
        # Adjust based on company size and strategy
        if self.company_size == 'startup':
            acquisition_budget *= 0.5  # Startups have limited acquisition capacity
        elif self.company_size == 'multinational':
            acquisition_budget *= 1.5  # Multinationals are more acquisition-focused
        
        # Determine number of acquisitions based on budget and company size
        if self.company_size == 'startup':
            max_acquisitions = 1
        elif self.company_size == 'sme':
            max_acquisitions = 2
        elif self.company_size == 'large':
            max_acquisitions = 3
        elif self.company_size == 'multinational':
            max_acquisitions = 5
        else:
            max_acquisitions = 1
        
        # Sort technologies by relevance and potential
        scored_technologies = []
        for tech in relevant_technologies:
            # Calculate relevance score
            segment_overlap = sum(1 for segment in tech.get('market_segments', []) if segment in self.market_segments)
            segment_score = segment_overlap / max(1, len(self.market_segments))
            
            # Calculate potential score
            maturity = tech.get('maturity', 0)
            commercial_potential = tech.get('commercial_potential', 0.5)
            potential_score = maturity * commercial_potential
            
            # Calculate overall score
            score = (segment_score * 0.4) + (potential_score * 0.6)
            
            scored_technologies.append((tech, score))
        
        # Sort by score (highest first)
        scored_technologies.sort(key=lambda x: x[1], reverse=True)
        
        # Select top technologies for acquisition
        for tech, score in scored_technologies[:max_acquisitions]:
            # Determine acquisition cost based on technology value and maturity
            base_cost = tech.get('value', 1000000) if 'value' in tech else 1000000
            maturity_factor = 1.0 + tech.get('maturity', 0.5)  # More mature = more expensive
            potential_factor = 1.0 + tech.get('commercial_potential', 0.5)  # More potential = more expensive
            
            acquisition_cost = base_cost * maturity_factor * potential_factor
            
            # Check if budget allows
            if acquisition_cost <= acquisition_budget:
                # Find the owner of the technology
                owner_id = tech.get('owner_id', '')
                owner_name = tech.get('owner_name', 'Unknown')
                owner_type = tech.get('owner_type', 'unknown')
                
                # If owner details not in technology, try to find from entities
                if not owner_id:
                    for entity in research_entities + commercial_players:
                        entity_techs = entity.get('technologies', [])
                        if any(t.get('id', '') == tech.get('id', '') for t in entity_techs):
                            owner_id = entity.get('id', '')
                            owner_name = entity.get('name', 'Unknown')
                            owner_type = entity.get('type', 'unknown')
                            break
                
                # Create acquisition
                acquisition = {
                    'technology_id': tech.get('id', ''),
                    'technology_name': tech.get('name', 'Unknown Technology'),
                    'owner_id': owner_id,
                    'owner_name': owner_name,
                    'owner_type': owner_type,
                    'acquisition_cost': acquisition_cost,
                    'acquisition_year': context.get('year', 0),
                    'market_segments': tech.get('market_segments', []),
                    'expected_roi': generate_triangular(1.2, 2.0, 5.0),  # Expected return on investment
                    'integration_time': random.randint(1, 2),  # 1-2 years to integrate
                    'success_probability': generate_triangular(0.7, 0.8, 0.9)  # 70-90% success probability
                }
                
                acquisitions.append(acquisition)
                acquisition_budget -= acquisition_cost
            
            # Stop if budget is exhausted
            if acquisition_budget <= 0:
                break
        
        return acquisitions
    
    def _decide_product_development(self, context: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Decide on product development initiatives.
        
        Args:
            context: Contextual information for decision making
            
        Returns:
            List of product development initiatives to pursue
        """
        new_products = []
        
        # Check technologies for product development opportunities
        mature_technologies = [tech for tech in self.technologies 
                             if tech.get('maturity', 0) >= 0.7]  # Only consider mature technologies
        
        # Also consider completed R&D projects
        completed_projects = [project for project in self.state.get('r_and_d_projects', []) 
                            if project.get('progress', 0) >= 100.0 and project.get('outcome', '') == 'success']
        
        # Combine technologies and completed projects as product sources
        product_sources = mature_technologies + completed_projects
        
        # Determine product development budget (typically 30-50% of R&D budget)
        r_and_d_budget = self.financial_metrics.get('r_and_d_budget', 0)
        product_budget = r_and_d_budget * generate_triangular(0.3, 0.4, 0.5)
        
        # Determine number of new products based on company size and budget
        if self.company_size == 'startup':
            max_products = 1
        elif self.company_size == 'sme':
            max_products = 2
        elif self.company_size == 'large':
            max_products = 3
        elif self.company_size == 'multinational':
            max_products = 5
        else:
            max_products = 1
        
        # Adjust based on current product development
        current_development = self.state.get('product_development', [])
        max_products = max(0, max_products - len(current_development))
        
        # Create new products from available sources
        for _ in range(min(max_products, len(product_sources))):
            # Select a source for product
            source = random.choice(product_sources)
            product_sources.remove(source)  # Don't select the same source twice
            
            # Determine product parameters
            if 'name' in source:  # It's a technology or project
                name = f"Product based on {source.get('name', 'Technology')}"
                segments = source.get('market_segments', [])
                if not segments and 'areas' in source:
                    # Convert research areas to market segments
                    segments = source.get('areas', [])
                source_type = 'technology' if 'maturity' in source else 'project'
                source_id = source.get('id', '')
            else:  # Fallback
                name = f"New Product in {random.choice(self.market_segments)}" if self.market_segments else 'New Product'
                segments = [random.choice(self.market_segments)] if self.market_segments else ['General']
                source_type = 'internal'
                source_id = ''
            
            # Determine development cost based on company size
            if self.company_size == 'startup':
                development_cost = generate_triangular(500000, 1000000, 3000000)  # 500k-3M
            elif self.company_size == 'sme':
                development_cost = generate_triangular(1000000, 3000000, 10000000)  # 1M-10M
            elif self.company_size == 'large':
                development_cost = generate_triangular(3000000, 10000000, 30000000)  # 3M-30M
            elif self.company_size == 'multinational':
                development_cost = generate_triangular(10000000, 30000000, 100000000)  # 10M-100M
            else:
                development_cost = 2000000  # Default 2M
            
            # Ensure cost doesn't exceed budget
            development_cost = min(development_cost, product_budget)
            product_budget -= development_cost
            
            # Create product
            product = {
                'name': name,
                'description': f"Product for {', '.join(segments)}",
                'market_segments': segments,
                'development_year': context.get('year', 0),
                'development_cost': development_cost,
                'development_time': random.randint(1, 3),  # 1-3 years to develop
                'progress': 0.0,  # 0-100%
                'expected_revenue': development_cost * generate_triangular(2.0, 5.0, 10.0),  # Expected revenue
                'expected_margin': generate_triangular(20, 40, 60),  # Expected profit margin 20-60%
                'source_type': source_type,
                'source_id': source_id,
                'regulatory_approval_needed': random.random() < 0.7,  # 70% chance of needing approval
                'regulatory_approval_time': random.randint(1, 3) if random.random() < 0.7 else 0,  # 1-3 years for approval
                'market_potential': generate_triangular(0.3, 0.6, 0.9)  # Market potential 30-90%
            }
            
            new_products.append(product)
        
        return new_products
    
    def _decide_partnerships(self, context: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Decide on partnership opportunities.
        
        Args:
            context: Contextual information for decision making
            
        Returns:
            List of partnership opportunities to pursue
        """
        new_partnerships = []
        
        # Get potential partners from context
        research_entities = context.get('research_entities', [])
        commercial_players = context.get('commercial_players', [])
        
        # Filter out self and current partners
        current_partnerships = self.partnerships
        current_partner_ids = [partnership.get('partner_id', '') for partnership in current_partnerships]
        
        potential_research_partners = [entity for entity in research_entities 
                                     if entity.get('id', '') != self.id and entity.get('id', '') not in current_partner_ids]
        
        potential_commercial_partners = [entity for entity in commercial_players 
                                       if entity.get('id', '') != self.id and entity.get('id', '') not in current_partner_ids]
        
        # Determine number of new partnerships based on company size
        if self.company_size == 'startup':
            max_partnerships = 2
        elif self.company_size == 'sme':
            max_partnerships = 3
        elif self.company_size == 'large':
            max_partnerships = 5
        elif self.company_size == 'multinational':
            max_partnerships = 8
        else:
            max_partnerships = 2
        
        # Adjust based on current partnerships
        max_partnerships = max(0, max_partnerships - len(current_partnerships))
        
        # Decide on research partnerships (typically 30-50% of partnerships)
        num_research_partnerships = int(max_partnerships * generate_triangular(0.3, 0.4, 0.5))
        
        # Create research partnerships
        for _ in range(min(num_research_partnerships, len(potential_research_partners))):
            # Select a research partner
            partner = random.choice(potential_research_partners)
            potential_research_partners.remove(partner)  # Don't select the same partner twice
            
            # Determine partnership parameters
            duration = random.randint(2, 5)  # 2-5 years
            
            # Find overlapping research areas/market segments
            partner_focus = partner.get('research_focus', [])
            overlapping_areas = [segment for segment in self.market_segments if segment in partner_focus]
            
            if not overlapping_areas:
                # If no overlap, pick one area from each
                if self.market_segments and partner_focus:
                    focus_area = f"{random.choice(self.market_segments)} + {random.choice(partner_focus)}"
                elif self.market_segments:
                    focus_area = random.choice(self.market_segments)
                elif partner_focus:
                    focus_area = random.choice(partner_focus)
                else:
                    focus_area = "Joint Research"
            else:
                focus_area = random.choice(overlapping_areas)
            
            # Determine investment based on company size
            if self.company_size == 'startup':
                investment = generate_triangular(100000, 300000, 1000000)  # 100k-1M
            elif self.company_size == 'sme':
                investment = generate_triangular(300000, 1000000, 3000000)  # 300k-3M
            elif self.company_size == 'large':
                investment = generate_triangular(1000000, 3000000, 10000000)  # 1M-10M
            elif self.company_size == 'multinational':
                investment = generate_triangular(3000000, 10000000, 30000000)  # 3M-30M
            else:
                investment = 500000  # Default 500k
            
            # Create partnership
            partnership = {
                'partner_id': partner.get('id', ''),
                'partner_name': partner.get('name', ''),
                'partner_type': 'research',
                'focus_area': focus_area,
                'start_year': context.get('year', 0),
                'duration': duration,
                'investment': investment,
                'expected_roi': generate_triangular(1.5, 3.0, 8.0),  # Expected return on investment
                'projects': [],  # Will be filled with joint projects
                'technologies': [],  # Will be filled with joint technologies
                'products': []  # Will be filled with joint products
            }
            
            new_partnerships.append(partnership)
        
        # Decide on commercial partnerships (remaining partnerships)
        num_commercial_partnerships = max_partnerships - num_research_partnerships
        
        # Create commercial partnerships
        for _ in range(min(num_commercial_partnerships, len(potential_commercial_partners))):
            # Select a commercial partner
            partner = random.choice(potential_commercial_partners)
            potential_commercial_partners.remove(partner)  # Don't select the same partner twice
            
            # Determine partnership parameters
            duration = random.randint(3, 7)  # 3-7 years for commercial partnerships
            
            # Find overlapping market segments
            partner_segments = partner.get('market_segments', [])
            overlapping_segments = [segment for segment in self.market_segments if segment in partner_segments]
            
            if not overlapping_segments:
                # If no overlap, pick one segment from each
                if self.market_segments and partner_segments:
                    focus_area = f"{random.choice(self.market_segments)} + {random.choice(partner_segments)}"
                elif self.market_segments:
                    focus_area = random.choice(self.market_segments)
                elif partner_segments:
                    focus_area = random.choice(partner_segments)
                else:
                    focus_area = "Market Collaboration"
            else:
                focus_area = random.choice(overlapping_segments)
            
            # Determine partnership type
            partnership_types = ['distribution', 'co-development', 'licensing', 'joint venture']
            partnership_type = random.choice(partnership_types)
            
            # Determine investment based on partnership type and company size
            if partnership_type == 'distribution':
                # Distribution partnerships typically involve lower upfront investment
                investment_factor = 0.5
            elif partnership_type == 'licensing':
                # Licensing partnerships involve moderate investment
                investment_factor = 0.8
            elif partnership_type == 'co-development':
                # Co-development partnerships involve higher investment
                investment_factor = 1.2
            elif partnership_type == 'joint venture':
                # Joint ventures involve the highest investment
                investment_factor = 2.0
            else:
                investment_factor = 1.0
            
            if self.company_size == 'startup':
                base_investment = generate_triangular(200000, 500000, 2000000)  # 200k-2M
            elif self.company_size == 'sme':
                base_investment = generate_triangular(500000, 2000000, 5000000)  # 500k-5M
            elif self.company_size == 'large':
                base_investment = generate_triangular(2000000, 5000000, 20000000)  # 2M-20M
            elif self.company_size == 'multinational':
                base_investment = generate_triangular(5000000, 20000000, 50000000)  # 5M-50M
            else:
                base_investment = 1000000  # Default 1M
            
            investment = base_investment * investment_factor
            
            # Create partnership
            partnership = {
                'partner_id': partner.get('id', ''),
                'partner_name': partner.get('name', ''),
                'partner_type': 'commercial',
                'partnership_type': partnership_type,
                'focus_area': focus_area,
                'start_year': context.get('year', 0),
                'duration': duration,
                'investment': investment,
                'expected_roi': generate_triangular(1.2, 2.5, 5.0),  # Expected return on investment
                'market_segments': [focus_area] if focus_area not in self.market_segments else [],
                'technologies': [],  # Will be filled with shared technologies
                'products': []  # Will be filled with joint products
            }
            
            new_partnerships.append(partnership)
        
        return new_partnerships
    
    def _decide_market_expansion(self, context: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Decide on market expansion initiatives.
        
        Args:
            context: Contextual information for decision making
            
        Returns:
            List of market expansion initiatives to pursue
        """
        expansion_initiatives = []
        
        # Get market data from context
        market_data = context.get('market_data', {})
        market_trends = context.get('market_trends', {})
        
        # Get available market segments not currently served
        all_segments = market_data.get('segments', [])
        unserved_segments = [segment for segment in all_segments if segment not in self.market_segments]
        
        # Get available regions not currently served
        current_regions = set()
        for segment, share_data in self.market_share.items():
            if isinstance(share_data, dict):
                current_regions.update(share_data.keys())
            # If share_data is a float, it represents aggregate share, so we cannot infer regions from it here.
            # We will rely on the agent's primary region or other attributes if needed.

        if not current_regions and self.region:
            current_regions.add(self.region)
        
        all_regions = market_data.get('regions', [])
        unserved_regions = [region for region in all_regions if region not in current_regions]
        
        # Determine expansion budget (typically 20-40% of marketing budget)
        marketing_budget = self.financial_metrics.get('marketing_budget', 0)
        expansion_budget = marketing_budget * generate_triangular(0.2, 0.3, 0.4)
        
        # Determine number of expansion initiatives based on company size
        if self.company_size == 'startup':
            max_initiatives = 1
        elif self.company_size == 'sme':
            max_initiatives = 2
        elif self.company_size == 'large':
            max_initiatives = 3
        elif self.company_size == 'multinational':
            max_initiatives = 5
        else:
            max_initiatives = 1
        
        # Adjust based on current expansion initiatives
        current_initiatives = self.state.get('market_expansion', [])
        max_initiatives = max(0, max_initiatives - len(current_initiatives))
        
        # Decide on segment expansion (typically 40-60% of initiatives)
        num_segment_initiatives = int(max_initiatives * generate_triangular(0.4, 0.5, 0.6))
        
        # Create segment expansion initiatives
        for _ in range(min(num_segment_initiatives, len(unserved_segments))):
            # Select a segment to expand into
            segment = random.choice(unserved_segments)
            unserved_segments.remove(segment)  # Don't select the same segment twice
            
            # Check market trend for this segment
            trend = market_trends.get(segment, 0)
            
            # Only expand into segments with positive or neutral trends
            if trend >= -2:  # Allow slightly negative trends
                # Determine expansion parameters
                time_to_market = random.randint(1, 3)  # 1-3 years
                
                # Determine investment based on company size and segment size
                segment_size = market_data.get('segment_sizes', {}).get(segment, 1000000)  # Default 1M
                
                if self.company_size == 'startup':
                    investment = generate_triangular(200000, 500000, 1000000)  # 200k-1M
                elif self.company_size == 'sme':
                    investment = generate_triangular(500000, 1000000, 3000000)  # 500k-3M
                elif self.company_size == 'large':
                    investment = generate_triangular(1000000, 3000000, 10000000)  # 1M-10M
                elif self.company_size == 'multinational':
                    investment = generate_triangular(3000000, 10000000, 30000000)  # 3M-30M
                else:
                    investment = 500000  # Default 500k
                
                # Adjust investment based on segment size
                investment = investment * (segment_size / 10000000)  # Normalize to 10M segment size
                
                # Ensure investment doesn't exceed budget
                investment = min(investment, expansion_budget)
                expansion_budget -= investment
                
                # Determine expected market share based on investment and company size
                base_market_share = 0.0
                if self.company_size == 'startup':
                    base_market_share = generate_triangular(0.01, 0.03, 0.1)  # 1-10%
                elif self.company_size == 'sme':
                    base_market_share = generate_triangular(0.03, 0.08, 0.2)  # 3-20%
                elif self.company_size == 'large':
                    base_market_share = generate_triangular(0.05, 0.15, 0.3)  # 5-30%
                elif self.company_size == 'multinational':
                    base_market_share = generate_triangular(0.1, 0.25, 0.4)  # 10-40%
                else:
                    base_market_share = 0.05  # Default 5%
                
                # Adjust based on investment relative to segment size
                investment_factor = min(2.0, max(0.5, investment / (segment_size * 0.1)))  # 10% of segment size as reference
                expected_market_share = base_market_share * investment_factor
                
                # Create initiative
                initiative = {
                    'type': 'segment_expansion',
                    'segment': segment,
                    'start_year': context.get('year', 0),
                    'time_to_market': time_to_market,
                    'investment': investment,
                    'progress': 0.0,  # 0-100%
                    'expected_market_share': expected_market_share,
                    'expected_revenue': segment_size * expected_market_share,
                    'regions': list(current_regions) if current_regions else ['Global']
                }
                
                expansion_initiatives.append(initiative)
        
        # Decide on regional expansion (remaining initiatives)
        num_region_initiatives = max_initiatives - num_segment_initiatives
        
        # Create regional expansion initiatives
        for _ in range(min(num_region_initiatives, len(unserved_regions))):
            # Select a region to expand into
            region = random.choice(unserved_regions)
            unserved_regions.remove(region)  # Don't select the same region twice
            
            # Check market trend for this region
            region_trend = market_trends.get(f"region_{region}", 0)
            
            # Only expand into regions with positive or neutral trends
            if region_trend >= -2:  # Allow slightly negative trends
                # Determine expansion parameters
                time_to_market = random.randint(1, 3)  # 1-3 years
                
                # Determine investment based on company size and region size
                region_size = market_data.get('region_sizes', {}).get(region, 10000000)  # Default 10M
                
                if self.company_size == 'startup':
                    investment = generate_triangular(300000, 1000000, 3000000)  # 300k-3M
                elif self.company_size == 'sme':
                    investment = generate_triangular(1000000, 3000000, 10000000)  # 1M-10M
                elif self.company_size == 'large':
                    investment = generate_triangular(3000000, 10000000, 30000000)  # 3M-30M
                elif self.company_size == 'multinational':
                    investment = generate_triangular(10000000, 30000000, 100000000)  # 10M-100M
                else:
                    investment = 2000000  # Default 2M
                
                # Adjust investment based on region size
                investment = investment * (region_size / 100000000)  # Normalize to 100M region size
                
                # Ensure investment doesn't exceed budget
                investment = min(investment, expansion_budget)
                expansion_budget -= investment
                
                # Determine target segments for this region
                target_segments = self.market_segments.copy() if self.market_segments else ['General']
                
                # Create initiative
                initiative = {
                    'type': 'region_expansion',
                    'region': region,
                    'start_year': context.get('year', 0),
                    'time_to_market': time_to_market,
                    'investment': investment,
                    'progress': 0.0,  # 0-100%
                    'target_segments': target_segments,
                    'expected_market_shares': {segment: generate_triangular(0.01, 0.05, 0.15) for segment in target_segments},
                    'expected_revenue': sum(market_data.get('segment_sizes', {}).get(segment, 1000000) * 
                                         generate_triangular(0.01, 0.05, 0.15) * 
                                         (region_size / market_data.get('total_market_size', 1000000000)) 
                                         for segment in target_segments)
                }
                
                expansion_initiatives.append(initiative)
        
        return expansion_initiatives
    
    def _decide_ip_strategy(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Decide on intellectual property strategy.
        
        Args:
            context: Contextual information for decision making
            
        Returns:
            Dictionary of IP strategy decisions
        """
        ip_strategy = {}
        
        # Determine patent applications
        patent_applications = []
        
        # Check completed R&D projects for patentable results
        r_and_d_projects = self.state.get('r_and_d_projects', [])
        completed_projects = [project for project in r_and_d_projects 
                            if project.get('progress', 0) >= 100.0 and project.get('outcome', '') == 'success']
        
        # Check technologies for patentable aspects
        patentable_technologies = [tech for tech in self.technologies 
                                 if tech.get('patented', False) == False]  # Only consider non-patented technologies
        
        # Combine sources for patent applications
        patent_sources = completed_projects + patentable_technologies
        
        # Determine number of patent applications based on company size
        if self.company_size == 'startup':
            max_patents = 2
        elif self.company_size == 'sme':
            max_patents = 5
        elif self.company_size == 'large':
            max_patents = 10
        elif self.company_size == 'multinational':
            max_patents = 20
        else:
            max_patents = 3
        
        # Create patent applications
        for source in patent_sources[:max_patents]:
            # Determine if source results are patentable
            patentability = generate_triangular(0.3, 0.5, 0.8)  # 30-80% chance of patentability
            
            # Adjust based on source type and focus area
            if 'focus' in source:  # It's a project
                if 'CRISPR' in source.get('focus', '') or 'Gene Editing' in source.get('focus', ''):
                    patentability *= 1.5  # Higher chance for CRISPR/gene editing
                
                if 'Synthetic Biology' in source.get('focus', ''):
                    patentability *= 1.3  # Higher chance for synthetic biology
            elif 'name' in source:  # It's a technology
                if 'CRISPR' in source.get('name', '') or 'Gene Editing' in source.get('name', ''):
                    patentability *= 1.5  # Higher chance for CRISPR/gene editing
                
                if 'Synthetic Biology' in source.get('name', ''):
                    patentability *= 1.3  # Higher chance for synthetic biology
            
            # Decide whether to apply for patent
            if random.random() < patentability:
                # Create patent application
                if 'focus' in source:  # It's a project
                    title = f"Patent for {source.get('name', 'R&D Project')}"
                    description = f"Patent based on R&D in {source.get('focus', 'Unknown Area')}"
                    areas = source.get('market_segments', [])
                    source_id = source.get('id', '')
                    source_type = 'project'
                elif 'name' in source:  # It's a technology
                    title = f"Patent for {source.get('name', 'Technology')}"
                    description = f"Patent covering technology in {', '.join(source.get('market_segments', []))}"
                    areas = source.get('market_segments', [])
                    source_id = source.get('id', '')
                    source_type = 'technology'
                else:  # Fallback
                    title = "Patent Application"
                    description = "General patent application"
                    areas = self.market_segments
                    source_id = ''
                    source_type = 'internal'
                
                patent = {
                    'title': title,
                    'description': description,
                    'areas': areas,
                    'application_year': context.get('year', 0),
                    'approval_probability': generate_triangular(0.5, 0.7, 0.9),  # 50-90% approval probability
                    'approval_time': random.randint(1, 3),  # 1-3 years for approval
                    'value': generate_triangular(500000, 2000000, 10000000),  # Value between 500k and 10M
                    'status': 'pending',
                    'source_type': source_type,
                    'source_id': source_id,
                    'cost': generate_triangular(50000, 100000, 300000)  # Cost between 50k and 300k
                }
                
                patent_applications.append(patent)
                
                # Mark technology as patented if it's a technology source
                if source_type == 'technology':
                    for tech in self.technologies:
                        if tech.get('id', '') == source_id:
                            tech['patented'] = True
                            break
        
        ip_strategy['patent_applications'] = patent_applications
        
        # Determine licensing strategy
        licensing_deals = []
        
        # Check approved patents and mature technologies for licensing opportunities
        approved_patents = [patent for patent in self.intellectual_property 
                          if patent.get('type', '') == 'patent' and patent.get('status', '') == 'approved']
        
        mature_technologies = [tech for tech in self.technologies 
                             if tech.get('maturity', 0) >= 0.8]  # Only consider very mature technologies
        
        # Determine number of licensing deals based on company size and IP portfolio
        max_licensing_deals = len(approved_patents) + len(mature_technologies)
        max_licensing_deals = min(max_licensing_deals, 5 if self.company_size == 'multinational' else 
                                3 if self.company_size == 'large' else 
                                2 if self.company_size == 'sme' else 1)
        
        # Create licensing deals
        for _ in range(max_licensing_deals):
            # Determine what to license (patent or technology)
            if approved_patents and (not mature_technologies or random.random() < 0.7):  # 70% chance to license patent if both available
                # License a patent
                patent = random.choice(approved_patents)
                approved_patents.remove(patent)  # Don't license the same patent twice
                
                license_type = 'patent'
                license_id = patent.get('id', '')
                license_name = patent.get('title', 'Patent')
                license_areas = patent.get('areas', [])
            elif mature_technologies:
                # License a technology
                tech = random.choice(mature_technologies)
                mature_technologies.remove(tech)  # Don't license the same technology twice
                
                license_type = 'technology'
                license_id = tech.get('id', '')
                license_name = tech.get('name', 'Technology')
                license_areas = tech.get('market_segments', [])
            else:
                # No more patents or technologies to license
                break
            
            # Determine licensing parameters
            duration = random.randint(5, 15)  # 5-15 years
            
            # Determine upfront payment based on license type and company size
            if license_type == 'patent':
                base_upfront = generate_triangular(500000, 2000000, 5000000)  # 500k-5M for patents
            else:  # technology
                base_upfront = generate_triangular(1000000, 3000000, 10000000)  # 1M-10M for technologies
            
            # Adjust based on company size of licensee (assumed to be proportional to our size)
            if self.company_size == 'startup':
                upfront_factor = 0.5  # Smaller companies get smaller deals
            elif self.company_size == 'sme':
                upfront_factor = 1.0  # Reference level
            elif self.company_size == 'large':
                upfront_factor = 2.0  # Larger companies get larger deals
            elif self.company_size == 'multinational':
                upfront_factor = 4.0  # Much larger deals for multinationals
            else:
                upfront_factor = 1.0
            
            upfront_payment = base_upfront * upfront_factor
            
            # Determine royalty rate
            royalty_rate = generate_triangular(0.02, 0.05, 0.1)  # 2-10% royalty rate
            
            # Create licensing deal
            deal = {
                'type': license_type,
                'asset_id': license_id,
                'asset_name': license_name,
                'start_year': context.get('year', 0),
                'duration': duration,
                'upfront_payment': upfront_payment,
                'royalty_rate': royalty_rate,
                'areas': license_areas,
                'expected_annual_revenue': upfront_payment * generate_triangular(0.1, 0.2, 0.5),  # 10-50% of upfront as annual revenue
                'status': 'pending',
                'licensee_type': random.choice(['commercial', 'research']),
                'exclusive': random.random() < 0.3  # 30% chance of exclusive license
            }
            
            licensing_deals.append(deal)
        
        ip_strategy['licensing_deals'] = licensing_deals
        
        # Determine IP acquisition strategy
        ip_acquisitions = []
        
        # Determine IP acquisition budget (typically 10-30% of R&D budget)
        r_and_d_budget = self.financial_metrics.get('r_and_d_budget', 0)
        ip_acquisition_budget = r_and_d_budget * generate_triangular(0.1, 0.2, 0.3)
        
        # Get available patents from context
        available_patents = context.get('available_patents', [])
        
        # Filter patents based on relevance to market segments
        relevant_patents = [patent for patent in available_patents 
                          if any(area in self.market_segments for area in patent.get('areas', []))]        
        
        # Determine number of acquisitions based on budget and company size
        if self.company_size == 'startup':
            max_acquisitions = 1
        elif self.company_size == 'sme':
            max_acquisitions = 2
        elif self.company_size == 'large':
            max_acquisitions = 3
        elif self.company_size == 'multinational':
            max_acquisitions = 5
        else:
            max_acquisitions = 1
        
        # Create IP acquisitions
        for patent in relevant_patents[:max_acquisitions]:
            # Determine acquisition cost
            acquisition_cost = patent.get('value', 1000000) * generate_triangular(0.8, 1.0, 1.5)  # 80-150% of patent value
            
            # Check if budget allows
            if acquisition_cost <= ip_acquisition_budget:
                # Create acquisition
                acquisition = {
                    'patent_id': patent.get('id', ''),
                    'patent_title': patent.get('title', 'Patent'),
                    'owner_id': patent.get('owner_id', ''),
                    'owner_name': patent.get('owner_name', 'Unknown'),
                    'acquisition_cost': acquisition_cost,
                    'acquisition_year': context.get('year', 0),
                    'areas': patent.get('areas', []),
                    'expected_value': acquisition_cost * generate_triangular(1.2, 2.0, 5.0),  # Expected value 1.2-5x cost
                    'status': 'pending'
                }
                
                ip_acquisitions.append(acquisition)
                ip_acquisition_budget -= acquisition_cost
            
            # Stop if budget is exhausted
            if ip_acquisition_budget <= 0:
                break
        
        ip_strategy['ip_acquisitions'] = ip_acquisitions
        
        return ip_strategy
    
    def _decide_investment_strategy(self, context: Dict[str, Any], expansion_initiatives: List[Dict], product_development_initiatives: List[Dict]) -> Dict[str, Any]:
        """Decide on investment and funding strategy.
        
        Args:
            context: Contextual information for decision making
            
        Returns:
            Dictionary of investment strategy decisions
        """
        investment_strategy = {}
        
        # Determine funding needs based on company size and growth plans
        if self.company_size == 'startup':
            # Startups often need external funding
            current_capital = self.resources.get('capital', 0)
            burn_rate = self.financial_metrics.get('burn_rate', 0)
            
            # Calculate runway in months
            runway = burn_rate > 0 and current_capital / burn_rate or 24
            
            if runway < 18:  # Less than 18 months runway
                # Need funding
                funding_needed = True
                funding_amount = burn_rate * 24  # Aim for 24 months runway
                funding_type = random.choice(['venture_capital', 'angel', 'strategic_investment', 'grant'])
            else:
                funding_needed = False
                funding_amount = 0
                funding_type = None
        elif self.company_size == 'sme':
            # SMEs may need funding for expansion
            expansion_initiatives = self.state.get('market_expansion', [])
            product_development = self.state.get('product_development', [])
            
            # Calculate total investment needed for initiatives
            total_investment_needed = sum(initiative.get('investment', 0) for initiative in expansion_initiatives) + \
                                    sum(product.get('development_cost', 0) for product in product_development)
            
            current_capital = self.resources.get('capital', 0)
            
            if total_investment_needed > current_capital * 0.5:  # If initiatives would use more than 50% of capital
                # Need funding
                funding_needed = True
                funding_amount = total_investment_needed - (current_capital * 0.3)  # Keep 30% of capital as reserve
                funding_type = random.choice(['bank_loan', 'private_equity', 'strategic_investment'])
            else:
                funding_needed = False
                funding_amount = 0
                funding_type = None
        elif self.company_size == 'large' or self.company_size == 'multinational':
            # Large companies typically self-fund but may issue bonds or equity
            funding_needed = random.random() < 0.3  # 30% chance of seeking funding in a given year
            
            if funding_needed:
                # Calculate funding amount based on revenue
                revenue = self.financial_metrics.get('revenue', 0)
                funding_amount = revenue * generate_triangular(0.1, 0.2, 0.5)  # 10-50% of revenue
                funding_type = random.choice(['bonds', 'equity', 'strategic_investment'])
            else:
                funding_amount = 0
                funding_type = None
        else:
            funding_needed = False
            funding_amount = 0
            funding_type = None
        
        investment_strategy['funding'] = {
            'needed': funding_needed,
            'amount': funding_amount,
            'type': funding_type,
            'purpose': 'expansion' if expansion_initiatives else 'product_development' if product_development_initiatives else 'general'
        }
        
        # Determine investment in other companies/startups
        investments_in_others = []
        
        # Only large and multinational companies typically invest in others
        if self.company_size in ['large', 'multinational']:
            # Determine investment budget (typically 5-15% of capital)
            current_capital = self.resources.get('capital', 0)
            investment_budget = current_capital * generate_triangular(0.05, 0.1, 0.15)
            
            # Get potential investment targets from context
            startups = [entity for entity in context.get('commercial_players', []) 
                      if entity.get('company_size', '') == 'startup' and entity.get('id', '') != self.id]
            
            # Filter startups based on relevance to market segments
            relevant_startups = [startup for startup in startups 
                               if any(segment in self.market_segments for segment in startup.get('market_segments', []))]
            
            # Determine number of investments based on budget and company size
            if self.company_size == 'large':
                max_investments = 2
            elif self.company_size == 'multinational':
                max_investments = 5
            else:
                max_investments = 0
            
            # Create investments
            for startup in relevant_startups[:max_investments]:
                # Determine investment amount
                startup_valuation = startup.get('financial_metrics', {}).get('valuation', 5000000)  # Default 5M
                investment_amount = startup_valuation * generate_triangular(0.05, 0.1, 0.2)  # 5-20% stake
                
                # Check if budget allows
                if investment_amount <= investment_budget:
                    # Create investment
                    investment = {
                        'target_id': startup.get('id', ''),
                        'target_name': startup.get('name', 'Startup'),
                        'investment_amount': investment_amount,
                        'investment_year': context.get('year', 0),
                        'equity_stake': investment_amount / startup_valuation,
                        'expected_roi': generate_triangular(1.5, 3.0, 10.0),  # Expected return on investment
                        'market_segments': startup.get('market_segments', []),
                        'technologies': startup.get('technologies', []),
                        'status': 'pending'
                    }
                    
                    investments_in_others.append(investment)
                    investment_budget -= investment_amount
                
                # Stop if budget is exhausted
                if investment_budget <= 0:
                    break
        
        investment_strategy['investments_in_others'] = investments_in_others
        
        return investment_strategy
    
    def _update_r_and_d_projects(self, actions: Dict[str, Any], context: Dict[str, Any]) -> None:
        """Update R&D projects based on actions and context.
        
        Args:
            actions: Actions taken by the agent
            context: Contextual information
        """
        # Get current projects
        current_projects = self.state.get('r_and_d_projects', [])
        
        # Add new projects from actions
        new_projects = actions.get('r_and_d_projects', [])
        current_projects.extend(new_projects)
        
        # Update progress of existing projects
        for project in current_projects:
            if project.get('progress', 0) < 100.0:  # Only update incomplete projects
                # Calculate progress increment
                duration = project.get('duration', 1)
                base_increment = 100.0 / duration  # Base progress per year
                
                # Adjust based on innovation capacity
                capacity_factor = self.innovation_capacity / 50.0  # 1.0 at capacity 50
                
                # Adjust based on resources allocated
                resource_factor = 1.0  # Default
                
                # Calculate actual increment
                progress_increment = base_increment * capacity_factor * resource_factor
                
                # Update progress
                project['progress'] = min(100.0, project.get('progress', 0) + progress_increment)
                
                # If project completed, determine outcome
                if project['progress'] >= 100.0:
                    success_probability = project.get('success_probability', 0.5)
                    if random.random() < success_probability:
                        project['outcome'] = 'success'
                        
                        # Create technology from successful project
                        technology = {
                            'name': f"Technology from {project.get('name', 'R&D Project')}",
                            'description': f"Technology developed from R&D in {project.get('focus', 'Unknown Area')}",
                            'market_segments': project.get('market_segments', []),
                            'maturity': generate_triangular(0.5, 0.7, 0.9),  # 50-90% maturity
                            'commercial_potential': generate_triangular(0.5, 0.7, 0.9),  # 50-90% commercial potential
                            'development_year': context.get('year', 0),
                            'development_cost': project.get('total_budget', 0),
                            'patented': False,
                            'value': project.get('total_budget', 0) * project.get('expected_roi', 2.0)
                        }
                        
                        self.technologies.append(technology)
                    else:
                        project['outcome'] = 'failure'
        
        # Remove completed projects older than 5 years
        current_year = context.get('year', 0)
        current_projects = [project for project in current_projects 
                          if project.get('progress', 0) < 100.0 or 
                          current_year - project.get('start_year', 0) <= 5]
        
        # Update state
        self.state['r_and_d_projects'] = current_projects
    
    def _update_technologies(self, actions: Dict[str, Any], context: Dict[str, Any]) -> None:
        """Update technologies based on actions and context.
        
        Args:
            actions: Actions taken by the agent
            context: Contextual information
        """
        # Process technology acquisitions
        acquisitions = actions.get('technology_acquisition', [])
        
        for acquisition in acquisitions:
            if acquisition.get('status', '') == 'pending':
                # Determine if acquisition is successful
                success_probability = acquisition.get('success_probability', 0.8)
                
                if random.random() < success_probability:
                    # Acquisition successful
                    acquisition['status'] = 'completed'
                    
                    # Add technology to portfolio
                    technology = {
                        'name': acquisition.get('technology_name', 'Acquired Technology'),
                        'description': f"Technology acquired from {acquisition.get('owner_name', 'Unknown')}",
                        'market_segments': acquisition.get('market_segments', []),
                        'maturity': generate_triangular(0.7, 0.8, 0.9),  # 70-90% maturity for acquired tech
                        'commercial_potential': generate_triangular(0.6, 0.8, 0.9),  # 60-90% commercial potential
                        'acquisition_year': context.get('year', 0),
                        'acquisition_cost': acquisition.get('acquisition_cost', 0),
                        'patented': random.random() < 0.5,  # 50% chance of being patented
                        'value': acquisition.get('acquisition_cost', 0) * acquisition.get('expected_roi', 2.0),
                        'integration_progress': 0.0  # 0-100%
                    }
                    
                    self.technologies.append(technology)
                    
                    # Deduct cost from capital
                    self.resources['capital'] = max(0, self.resources.get('capital', 0) - acquisition.get('acquisition_cost', 0))
                else:
                    # Acquisition failed
                    acquisition['status'] = 'failed'
        
        # Update integration progress of acquired technologies
        for tech in self.technologies:
            if 'integration_progress' in tech and tech['integration_progress'] < 100.0:
                # Calculate progress increment
                integration_time = tech.get('integration_time', 1)
                base_increment = 100.0 / integration_time  # Base progress per year
                
                # Update progress
                tech['integration_progress'] = min(100.0, tech.get('integration_progress', 0) + base_increment)
                
                # If integration completed, update maturity and commercial potential
                if tech['integration_progress'] >= 100.0:
                    tech['maturity'] = min(1.0, tech.get('maturity', 0.8) + 0.1)  # Increase maturity
                    tech['commercial_potential'] = min(1.0, tech.get('commercial_potential', 0.8) + 0.1)  # Increase potential
        
        # Update maturity of existing technologies
        for tech in self.technologies:
            # Technologies mature over time
            if tech.get('maturity', 0) < 1.0:
                maturity_increment = generate_triangular(0.05, 0.1, 0.15)  # 5-15% maturity increase per year
                tech['maturity'] = min(1.0, tech.get('maturity', 0) + maturity_increment)
            
            # Update value based on maturity and commercial potential
            base_value = tech.get('value', 0) or tech.get('development_cost', 0) or tech.get('acquisition_cost', 0) or 1000000
            maturity_factor = 1.0 + tech.get('maturity', 0.5)  # More mature = more valuable
            potential_factor = 1.0 + tech.get('commercial_potential', 0.5)  # More potential = more valuable
            
            tech['value'] = base_value * maturity_factor * potential_factor
    
    def _update_products(self, actions: Dict[str, Any], context: Dict[str, Any]) -> None:
        """Update products based on actions and context.
        
        Args:
            actions: Actions taken by the agent
            context: Contextual information
        """
        # Get current products under development
        current_development = self.state.get('product_development', [])
        
        # Add new products from actions
        new_products = actions.get('product_development', [])
        current_development.extend(new_products)
        
        # Update progress of products under development
        for product in current_development:
            if product.get('progress', 0) < 100.0:  # Only update incomplete products
                # Calculate progress increment
                development_time = product.get('development_time') or 1
                base_increment = 100.0 / development_time  # Base progress per year
                
                # Adjust based on innovation capacity
                capacity_factor = self.innovation_capacity / 50.0  # 1.0 at capacity 50
                
                # Calculate actual increment
                progress_increment = base_increment * capacity_factor
                
                # Update progress
                product['progress'] = min(100.0, product.get('progress', 0) + progress_increment)
                
                # If development completed, move to regulatory approval if needed
                if product['progress'] >= 100.0:
                    if product.get('regulatory_approval_needed', False) and product.get('regulatory_status', '') != 'approved':
                        product['regulatory_status'] = 'pending'
                        product['regulatory_progress'] = 0.0
                    else:
                        # No approval needed or already approved, move to market
                        self._launch_product(product, context)
                        product['status'] = 'launched'
        
        # Update regulatory approval progress
        for product in current_development:
            if product.get('regulatory_status', '') == 'pending' and product.get('regulatory_progress', 0) < 100.0:
                # Calculate progress increment
                approval_time = product.get('regulatory_approval_time') or 1
                base_increment = 100.0 / approval_time  # Base progress per year
                
                # Update progress
                product['regulatory_progress'] = min(100.0, product.get('regulatory_progress', 0) + base_increment)
                
                # If approval completed, determine outcome
                if product['regulatory_progress'] >= 100.0:
                    # Determine if approval is successful (70-90% chance)
                    if random.random() < generate_triangular(0.7, 0.8, 0.9):
                        product['regulatory_status'] = 'approved'
                        
                        # Launch product
                        self._launch_product(product, context)
                        product['status'] = 'launched'
                    else:
                        product['regulatory_status'] = 'rejected'
        
        # Remove launched or rejected products from development
        current_development = [product for product in current_development 
                             if product.get('status', '') != 'launched' and product.get('regulatory_status', '') != 'rejected']
        
        # Update state
        self.state['product_development'] = current_development
        
        # Update existing products in market
        for product in self.products:
            # Update product lifecycle
            lifecycle_stage = product.get('lifecycle_stage', 'introduction')
            years_in_market = context.get('year', 0) - product.get('launch_year', context.get('year', 0))
            
            # Update lifecycle stage based on years in market
            if lifecycle_stage == 'introduction' and years_in_market >= 2:
                product['lifecycle_stage'] = 'growth'
            elif lifecycle_stage == 'growth' and years_in_market >= 5:
                product['lifecycle_stage'] = 'maturity'
            elif lifecycle_stage == 'maturity' and years_in_market >= 10:
                product['lifecycle_stage'] = 'decline'
            
            # Update revenue based on lifecycle stage
            base_revenue = product.get('annual_revenue', product.get('expected_revenue', 0))
            
            if lifecycle_stage == 'introduction':
                revenue_factor = generate_triangular(0.5, 0.7, 1.0)  # 50-100% of expected revenue
            elif lifecycle_stage == 'growth':
                revenue_factor = generate_triangular(1.0, 1.5, 2.0)  # 100-200% of expected revenue
            elif lifecycle_stage == 'maturity':
                revenue_factor = generate_triangular(0.8, 1.0, 1.2)  # 80-120% of expected revenue
            elif lifecycle_stage == 'decline':
                revenue_factor = generate_triangular(0.3, 0.5, 0.7)  # 30-70% of expected revenue
            else:
                revenue_factor = 1.0
            
            # Adjust based on market trends
            market_trends = context.get('market_trends', {})
            for segment in product.get('market_segments', []):
                if segment in market_trends:
                    trend = market_trends[segment]
                    if trend > 0:
                        revenue_factor *= 1.0 + (trend / 20)  # Up to 1.5x for strong positive trends
                    else:
                        revenue_factor *= 1.0 / (1.0 - (trend / 40))  # Down to 0.75x for strong negative trends
            
            product['annual_revenue'] = base_revenue * revenue_factor
            
            # Update profit based on revenue and margin
            margin = product.get('profit_margin', product.get('expected_margin', 30)) / 100.0
            product['annual_profit'] = product['annual_revenue'] * margin
    
    def _launch_product(self, product: Dict[str, Any], context: Dict[str, Any]) -> None:
        """Launch a product to market.
        
        Args:
            product: Product to launch
            context: Contextual information
        """
        # Create market-ready product
        market_product = {
            'name': product.get('name', 'New Product'),
            'description': product.get('description', ''),
            'market_segments': product.get('market_segments', []),
            'launch_year': context.get('year', 0),
            'development_cost': product.get('development_cost', 0),
            'expected_revenue': product.get('expected_revenue', 0),
            'annual_revenue': product.get('expected_revenue', 0) * generate_triangular(0.5, 0.7, 0.9),  # Initial revenue 50-90% of expected
            'profit_margin': product.get('expected_margin', 30),
            'annual_profit': product.get('expected_revenue', 0) * generate_triangular(0.5, 0.7, 0.9) * (product.get('expected_margin', 30) / 100.0),
            'lifecycle_stage': 'introduction',
            'market_share': {},
            'source_type': product.get('source_type', ''),
            'source_id': product.get('source_id', '')
        }
        
        # Calculate initial market share
        market_data = context.get('market_data', {})
        for segment in product.get('market_segments', []):
            segment_size = market_data.get('segment_sizes', {}).get(segment, 0)
            if segment_size > 0:
                # Calculate market share based on expected revenue and segment size
                market_share = min(0.3, market_product['annual_revenue'] / segment_size)  # Cap at 30% initial share
                market_product['market_share'][segment] = market_share
        
        # Add to products portfolio
        self.products.append(market_product)

        # Register product with the market model
        market_model = context.get('market_model')
        if market_model:
            product_id = market_product.get('id', f"product_{uuid.uuid4().hex[:8]}")
            market_model.register_product(product_id, market_product)
    
    def _update_partnerships(self, actions: Dict[str, Any], context: Dict[str, Any]) -> None:
        """Update partnerships based on actions and context.
        
        Args:
            actions: Actions taken by the agent
            context: Contextual information
        """
        # Process new partnerships
        new_partnerships = actions.get('partnerships', [])
        
        for partnership in new_partnerships:
            # Determine if partnership is accepted (80-95% chance)
            if random.random() < generate_triangular(0.8, 0.9, 0.95):
                # Partnership accepted
                partnership['status'] = 'active'
                
                # Add to partnerships
                self.partnerships.append(partnership)
                
                # Deduct investment from capital
                self.resources['capital'] = max(0, self.resources.get('capital', 0) - partnership.get('investment', 0))
            else:
                # Partnership rejected
                partnership['status'] = 'rejected'
        
        # Update existing partnerships
        current_year = context.get('year', 0)
        active_partnerships = []
        
        for partnership in self.partnerships:
            if partnership.get('status', '') == 'active':
                # Check if partnership has expired
                start_year = partnership.get('start_year', 0)
                duration = partnership.get('duration', 5)
                
                if current_year - start_year >= duration:
                    # Partnership expired
                    partnership['status'] = 'completed'
                else:
                    # Partnership still active
                    active_partnerships.append(partnership)
                    
                    # Update partnership outcomes
                    if partnership.get('partner_type', '') == 'research':
                        # Research partnerships may generate technologies
                        if random.random() < 0.3:  # 30% chance per year
                            # Create joint technology
                            technology = {
                                'name': f"Joint Technology with {partnership.get('partner_name', 'Partner')}",
                                'description': f"Technology developed in partnership with {partnership.get('partner_name', 'Partner')}",
                                'market_segments': [partnership.get('focus_area', 'General')],
                                'maturity': generate_triangular(0.4, 0.6, 0.8),  # 40-80% maturity
                                'commercial_potential': generate_triangular(0.5, 0.7, 0.9),  # 50-90% commercial potential
                                'development_year': current_year,
                                'development_cost': partnership.get('investment', 0) / duration,  # Portion of investment
                                'patented': random.random() < 0.4,  # 40% chance of being patented
                                'value': partnership.get('investment', 0) * generate_triangular(0.5, 1.0, 2.0),
                                'joint_development': True,
                                'partner_id': partnership.get('partner_id', ''),
                                'partner_name': partnership.get('partner_name', '')
                            }
                            
                            self.technologies.append(technology)
                            partnership['technologies'].append(technology['name'])
                    elif partnership.get('partner_type', '') == 'commercial':
                        # Commercial partnerships may generate revenue
                        partnership_type = partnership.get('partnership_type', '')
                        
                        if partnership_type == 'distribution':
                            # Distribution partnerships generate revenue from existing products
                            for product in self.products:
                                if partnership.get('focus_area', '') in product.get('market_segments', []):
                                    # Increase product revenue by 10-30%
                                    revenue_boost = product.get('annual_revenue', 0) * generate_triangular(0.1, 0.2, 0.3)
                                    product['annual_revenue'] += revenue_boost
                                    product['annual_profit'] += revenue_boost * (product.get('profit_margin', 30) / 100.0)
                        elif partnership_type == 'co-development':
                            # Co-development partnerships may create joint products
                            if random.random() < 0.4:  # 40% chance per year
                                # Create joint product development
                                product = {
                                    'name': f"Joint Product with {partnership.get('partner_name', 'Partner')}",
                                    'description': f"Product co-developed with {partnership.get('partner_name', 'Partner')}",
                                    'market_segments': [partnership.get('focus_area', 'General')],
                                    'development_year': current_year,
                                    'development_cost': partnership.get('investment', 0) / 2,  # Half of investment
                                    'development_time': random.randint(1, 2),  # 1-2 years to develop
                                    'progress': 0.0,  # 0-100%
                                    'expected_revenue': partnership.get('investment', 0) * generate_triangular(2.0, 4.0, 8.0),
                                    'expected_margin': generate_triangular(30, 45, 60),  # 30-60% margin
                                    'regulatory_approval_needed': random.random() < 0.6,  # 60% chance of needing approval
                                    'regulatory_approval_time': random.randint(1, 2) if random.random() < 0.6 else 0,
                                    'market_potential': generate_triangular(0.5, 0.7, 0.9),  # 50-90% potential
                                    'joint_development': True,
                                    'partner_id': partnership.get('partner_id', ''),
                                    'partner_name': partnership.get('partner_name', '')
                                }
                                
                                self.state['product_development'].append(product)
                                partnership['products'].append(product['name'])
                        elif partnership_type == 'licensing':
                            # Licensing partnerships generate revenue from IP
                            annual_revenue = partnership.get('investment', 0) * generate_triangular(0.2, 0.3, 0.5)  # 20-50% of investment as annual revenue
                            
                            # Add to financial metrics
                            self.financial_metrics['revenue'] += annual_revenue
                            self.financial_metrics['profit'] += annual_revenue * 0.8  # 80% margin on licensing
                        elif partnership_type == 'joint_venture':
                            # Joint ventures may create new market opportunities
                            if partnership.get('focus_area', '') not in self.market_segments:
                                self.market_segments.append(partnership.get('focus_area', ''))
                            
                            # Generate revenue
                            annual_revenue = partnership.get('investment', 0) * generate_triangular(0.3, 0.5, 0.8)  # 30-80% of investment as annual revenue
                            
                            # Add to financial metrics
                            self.financial_metrics['revenue'] += annual_revenue
                            self.financial_metrics['profit'] += annual_revenue * 0.4  # 40% margin on joint ventures
        
        # Update partnerships list
        self.partnerships = active_partnerships
    
    def _update_market_presence(self, actions: Dict[str, Any], context: Dict[str, Any]) -> None:
        """Update market presence based on actions and context.
        
        Args:
            actions: Actions taken by the agent
            context: Contextual information
        """
        # Process market expansion initiatives
        expansion_initiatives = self.state.get('market_expansion', [])
        new_initiatives = actions.get('market_expansion', [])
        expansion_initiatives.extend(new_initiatives)
        
        # Update progress of expansion initiatives
        completed_initiatives = []
        active_initiatives = []
        
        for initiative in expansion_initiatives:
            if initiative.get('progress', 0) < 100.0:  # Only update incomplete initiatives
                # Calculate progress increment
                time_to_market = initiative.get('time_to_market', 1)
                base_increment = 100.0 / time_to_market  # Base progress per year
                
                # Update progress
                initiative['progress'] = min(100.0, initiative.get('progress', 0) + base_increment)
                
                # If initiative completed, update market presence
                if initiative['progress'] >= 100.0:
                    completed_initiatives.append(initiative)
                    
                    if initiative.get('type', '') == 'segment_expansion':
                        # Add new segment to market segments
                        segment = initiative.get('segment', '')
                        if segment and segment not in self.market_segments:
                            self.market_segments.append(segment)
                        
                        # Update market share
                        expected_share = initiative.get('expected_market_share', 0.05)  # Default 5%
                        
                        if segment not in self.market_share:
                            self.market_share[segment] = {}
                        
                        for region in initiative.get('regions', ['Global']):
                            self.market_share[segment][region] = expected_share
                    elif initiative.get('type', '') == 'region_expansion':
                        # Add new region to market share
                        region = initiative.get('region', '')
                        if region:
                            for segment in initiative.get('target_segments', []):
                                if segment not in self.market_share:
                                    self.market_share[segment] = {}
                                
                                expected_share = initiative.get('expected_market_shares', {}).get(segment, 0.05)  # Default 5%
                                self.market_share[segment][region] = expected_share
                else:
                    active_initiatives.append(initiative)
        
        # Update state with active initiatives
        self.state['market_expansion'] = active_initiatives
        
        # Update market share based on products and competition
        market_data = context.get('market_data', {})
        competition = context.get('competition', {})
        
        for segment, share_data in self.market_share.items():
            # Determine market share change based on products and competition
            relevant_products = [product for product in self.products
                               if segment in product.get('market_segments', [])]

            if isinstance(share_data, dict):
                for region, share in share_data.items():
                    competitive_intensity = competition.get(segment, {}).get(region, 0.5)
                    share_change = self._calculate_share_change(relevant_products, competitive_intensity)
                    share_data[region] = max(0.01, min(1, share + share_change)) # Clamp
            elif isinstance(share_data, (int, float)):
                competitive_intensity = competition.get(segment, {}).get(self.region, 0.5)
                share_change = self._calculate_share_change(relevant_products, competitive_intensity)
                self.market_share[segment] = max(0.01, min(1, share_data + share_change)) # Clamp
    
    def _update_intellectual_property(self, actions: Dict[str, Any], context: Dict[str, Any]) -> None:
        """Update intellectual property based on actions and context.
        
        Args:
            actions: Actions taken by the agent
            context: Contextual information
        """
        # Process IP strategy actions
        ip_strategy = actions.get('ip_strategy', {})
        
        # Process patent applications
        patent_applications = ip_strategy.get('patent_applications', [])
        
        for application in patent_applications:
            # Add to intellectual property portfolio as pending patent
            patent = application.copy()
            patent['type'] = 'patent'
            patent['id'] = f"patent_{len(self.intellectual_property) + 1}"
            
            self.intellectual_property.append(patent)
            
            # Deduct cost from capital
            self.resources['capital'] = max(0, self.resources.get('capital', 0) - patent.get('cost', 0))
        
        # Process licensing deals
        licensing_deals = ip_strategy.get('licensing_deals', [])
        
        for deal in licensing_deals:
            # Add to intellectual property portfolio as licensing deal
            license = deal.copy()
            license['type'] = 'license'
            license['id'] = f"license_{len(self.intellectual_property) + 1}"
            
            self.intellectual_property.append(license)
            
            # Add upfront payment to capital
            self.resources['capital'] += license.get('upfront_payment', 0)
            
            # Add to revenue
            self.financial_metrics['revenue'] += license.get('upfront_payment', 0)
            self.financial_metrics['profit'] += license.get('upfront_payment', 0) * 0.9  # 90% margin on licensing
        
        # Process IP acquisitions
        ip_acquisitions = ip_strategy.get('ip_acquisitions', [])
        
        for acquisition in ip_acquisitions:
            # Determine if acquisition is successful (90% chance)
            if random.random() < 0.9:
                # Acquisition successful
                acquisition['status'] = 'completed'
                
                # Add to intellectual property portfolio
                patent = acquisition.copy()
                patent['type'] = 'patent'
                patent['id'] = f"patent_{len(self.intellectual_property) + 1}"
                patent['status'] = 'approved'  # Acquired patents are already approved
                
                self.intellectual_property.append(patent)
                
                # Deduct cost from capital
                self.resources['capital'] = max(0, self.resources.get('capital', 0) - acquisition.get('acquisition_cost', 0))
            else:
                # Acquisition failed
                acquisition['status'] = 'failed'
        
        # Update status of pending patents
        for ip in self.intellectual_property:
            if ip.get('type', '') == 'patent' and ip.get('status', '') == 'pending':
                # Check if approval time has passed
                application_year = ip.get('application_year', 0)
                approval_time = ip.get('approval_time', 2)
                current_year = context.get('year', 0)
                
                if current_year - application_year >= approval_time:
                    # Determine if patent is approved
                    approval_probability = ip.get('approval_probability', 0.7)
                    
                    if random.random() < approval_probability:
                        ip['status'] = 'approved'
                    else:
                        ip['status'] = 'rejected'
        
        # Update value of approved patents
        for ip in self.intellectual_property:
            if ip.get('type', '') == 'patent' and ip.get('status', '') == 'approved':
                # Patents appreciate in early years, then depreciate
                application_year = ip.get('application_year', 0)
                current_year = context.get('year', 0)
                years_since_application = current_year - application_year
                
                if years_since_application <= 5:  # First 5 years
                    # Appreciate by 5-15% per year
                    value_change = ip.get('value', 0) * generate_triangular(0.05, 0.1, 0.15)
                    ip['value'] = ip.get('value', 0) + value_change
                elif years_since_application <= 15:  # Years 6-15
                    # Stable value
                    pass
                else:  # After 15 years
                    # Depreciate by 10-20% per year
                    value_change = ip.get('value', 0) * generate_triangular(0.1, 0.15, 0.2)
                    ip['value'] = max(0, ip.get('value', 0) - value_change)
        
        # Update revenue from active licenses
        for ip in self.intellectual_property:
            if ip.get('type', '') == 'license' and ip.get('status', '') == 'active':
                # Generate annual revenue
                expected_annual_revenue = ip.get('expected_annual_revenue', 0)
                actual_revenue = expected_annual_revenue * generate_triangular(0.8, 1.0, 1.2)  # 80-120% of expected
                
                # Add to financial metrics
                self.financial_metrics['revenue'] += actual_revenue
                self.financial_metrics['profit'] += actual_revenue * 0.9  # 90% margin on licensing
                
                # Check if license has expired
                start_year = ip.get('start_year', 0)
                duration = ip.get('duration', 10)
                current_year = context.get('year', 0)
                
                if current_year - start_year >= duration:
                    ip['status'] = 'expired'
    
    def _update_financials(self, actions: Dict[str, Any], context: Dict[str, Any]) -> None:
        """Update financial metrics based on actions and context.
        
        Args:
            actions: Actions taken by the agent
            context: Contextual information
        """
        # Calculate revenue from products
        product_revenue = sum(product.get('annual_revenue', 0) for product in self.products)
        
        # Calculate revenue from licensing
        licensing_revenue = sum(ip.get('expected_annual_revenue', 0) * generate_triangular(0.8, 1.0, 1.2) 
                             for ip in self.intellectual_property 
                             if ip.get('type', '') == 'license' and ip.get('status', '') == 'active')
        
        # Calculate revenue from partnerships
        partnership_revenue = 0
        for partnership in self.partnerships:
            if partnership.get('status', '') == 'active':
                if partnership.get('partner_type', '') == 'commercial':
                    partnership_type = partnership.get('partnership_type', '')
                    
                    if partnership_type == 'joint_venture':
                        partnership_revenue += partnership.get('investment', 0) * generate_triangular(0.3, 0.5, 0.8)
                    elif partnership_type == 'licensing':
                        partnership_revenue += partnership.get('investment', 0) * generate_triangular(0.2, 0.3, 0.5)
        
        # Calculate total revenue
        total_revenue = product_revenue + licensing_revenue + partnership_revenue
        
        # Update revenue
        self.financial_metrics['revenue'] = total_revenue
        
        # Calculate profit from products
        product_profit = sum(product.get('annual_profit', 0) for product in self.products)
        
        # Calculate profit from licensing (90% margin)
        licensing_profit = licensing_revenue * 0.9
        
        # Calculate profit from partnerships (varies by type)
        partnership_profit = 0
        for partnership in self.partnerships:
            if partnership.get('status', '') == 'active':
                if partnership.get('partner_type', '') == 'commercial':
                    partnership_type = partnership.get('partnership_type', '')
                    
                    if partnership_type == 'joint_venture':
                        partnership_profit += partnership.get('investment', 0) * generate_triangular(0.3, 0.5, 0.8) * 0.4  # 40% margin
                    elif partnership_type == 'licensing':
                        partnership_profit += partnership.get('investment', 0) * generate_triangular(0.2, 0.3, 0.5) * 0.9  # 90% margin
        
        # Calculate R&D expenses
        r_and_d_budget = self.financial_metrics.get('r_and_d_budget', 0)
        
        # Calculate marketing expenses
        marketing_budget = self.financial_metrics.get('marketing_budget', 0)
        
        # Calculate other expenses (typically 20-40% of revenue)
        other_expenses = total_revenue * generate_triangular(0.2, 0.3, 0.4)
        
        # Calculate total profit
        total_profit = product_profit + licensing_profit + partnership_profit - r_and_d_budget - marketing_budget - other_expenses
        
        # Update profit
        self.financial_metrics['profit'] = total_profit
        
        # Update profit margin
        if total_revenue > 0:
            self.financial_metrics['profit_margin'] = (total_profit / total_revenue) * 100
        else:
            self.financial_metrics['profit_margin'] = 0
        
        # Update capital based on profit
        self.resources['capital'] += total_profit
        
        # Process investment strategy
        investment_strategy = actions.get('investment_strategy', {})
        
        # Process funding
        funding = investment_strategy.get('funding', {})
        
        if funding.get('needed', False) and funding.get('amount', 0) > 0:
            # Determine if funding is successful (varies by type and company size)
            success_probability = 0.0
            
            if self.company_size == 'startup':
                if funding.get('type', '') == 'venture_capital':
                    success_probability = generate_triangular(0.2, 0.3, 0.5)  # 20-50% for VC
                elif funding.get('type', '') == 'angel':
                    success_probability = generate_triangular(0.3, 0.4, 0.6)  # 30-60% for angel
                elif funding.get('type', '') == 'strategic_investment':
                    success_probability = generate_triangular(0.4, 0.5, 0.7)  # 40-70% for strategic
                elif funding.get('type', '') == 'grant':
                    success_probability = generate_triangular(0.1, 0.2, 0.4)  # 10-40% for grants
            elif self.company_size == 'sme':
                if funding.get('type', '') == 'bank_loan':
                    success_probability = generate_triangular(0.5, 0.7, 0.8)  # 50-80% for loans
                elif funding.get('type', '') == 'private_equity':
                    success_probability = generate_triangular(0.3, 0.5, 0.7)  # 30-70% for PE
                elif funding.get('type', '') == 'strategic_investment':
                    success_probability = generate_triangular(0.4, 0.6, 0.8)  # 40-80% for strategic
            elif self.company_size in ['large', 'multinational']:
                if funding.get('type', '') == 'bonds':
                    success_probability = generate_triangular(0.7, 0.8, 0.9)  # 70-90% for bonds
                elif funding.get('type', '') == 'equity':
                    success_probability = generate_triangular(0.6, 0.8, 0.9)  # 60-90% for equity
                elif funding.get('type', '') == 'strategic_investment':
                    success_probability = generate_triangular(0.5, 0.7, 0.9)  # 50-90% for strategic
            
            if random.random() < success_probability:
                # Funding successful
                funding['status'] = 'approved'
                
                # Add to capital
                self.resources['capital'] += funding.get('amount', 0)
                
                # Update valuation if equity-based funding
                if funding.get('type', '') in ['venture_capital', 'angel', 'private_equity', 'equity']:
                    # Calculate equity percentage
                    current_valuation = self.financial_metrics.get('valuation', 0)
                    funding_amount = funding.get('amount', 0)
                    
                    if current_valuation > 0:
                        equity_percentage = funding_amount / (current_valuation + funding_amount)
                        
                        # Update valuation (typically increases by 20-50% with funding)
                        valuation_increase = current_valuation * generate_triangular(0.2, 0.3, 0.5)
                        self.financial_metrics['valuation'] = current_valuation + valuation_increase
                        
                        # Record equity dilution
                        funding['equity_percentage'] = equity_percentage
            else:
                # Funding failed
                funding['status'] = 'rejected'
        
        # Process investments in other companies
        investments = investment_strategy.get('investments_in_others', [])
        
        for investment in investments:
            if investment.get('status', '') == 'pending':
                # Determine if investment is accepted (80% chance)
                if random.random() < 0.8:
                    # Investment accepted
                    investment['status'] = 'completed'
                    
                    # Deduct from capital
                    self.resources['capital'] = max(0, self.resources.get('capital', 0) - investment.get('investment_amount', 0))
                else:
                    # Investment rejected
                    investment['status'] = 'rejected'
        
        # Recalculate derived financial metrics
        self._calculate_derived_financials()
    
    def _update_resources(self, context: Dict[str, Any]) -> None:
        """Update resources based on context and financial metrics.
        
        Args:
            context: Contextual information
        """
        # Update employees based on revenue growth and company size
        current_employees = self.resources.get('employees', 0)
        revenue = self.financial_metrics.get('revenue', 0)
        
        # Calculate target employees based on revenue
        if self.company_size == 'startup':
            target_employees = int(revenue / 500000)  # 1 employee per 500k revenue
        elif self.company_size == 'sme':
            target_employees = int(revenue / 1000000)  # 1 employee per 1M revenue
        elif self.company_size == 'large':
            target_employees = int(revenue / 2000000)  # 1 employee per 2M revenue
        elif self.company_size == 'multinational':
            target_employees = int(revenue / 3000000)  # 1 employee per 3M revenue
        else:
            target_employees = int(revenue / 1000000)  # Default 1 employee per 1M revenue
        
        # Limit growth/reduction rate
        max_growth = current_employees * 0.3  # Max 30% growth per year
        max_reduction = current_employees * 0.2  # Max 20% reduction per year
        
        employee_change = target_employees - current_employees
        
        if employee_change > 0:
            employee_change = min(employee_change, max_growth)
        elif employee_change < 0:
            employee_change = max(employee_change, -max_reduction)
        
        # Update employees
        self.resources['employees'] = max(5, current_employees + int(employee_change))  # Minimum 5 employees
        
        # Update other resources based on company performance
        profit = self.financial_metrics.get('profit', 0)
        
        if profit > 0:
            # Company is profitable, may acquire more resources
            if 'facilities' in self.resources:
                # Expand facilities if profitable
                self.resources['facilities'] += profit * 0.05  # 5% of profit to facilities
            else:
                # Initialize facilities based on company size
                if self.company_size == 'startup':
                    self.resources['facilities'] = 1  # Small office
                elif self.company_size == 'sme':
                    self.resources['facilities'] = 3  # Medium facilities
                elif self.company_size == 'large':
                    self.resources['facilities'] = 10  # Large facilities
                elif self.company_size == 'multinational':
                    self.resources['facilities'] = 30  # Multiple large facilities
                else:
                    self.resources['facilities'] = 2  # Default medium facilities
            
            if 'equipment' in self.resources:
                # Upgrade equipment if profitable
                self.resources['equipment'] += profit * 0.03  # 3% of profit to equipment
            else:
                # Initialize equipment based on company size
                if self.company_size == 'startup':
                    self.resources['equipment'] = 500000  # Basic equipment
                elif self.company_size == 'sme':
                    self.resources['equipment'] = 2000000  # Standard equipment
                elif self.company_size == 'large':
                    self.resources['equipment'] = 10000000  # Advanced equipment
                elif self.company_size == 'multinational':
                    self.resources['equipment'] = 50000000  # State-of-the-art equipment
                else:
                    self.resources['equipment'] = 1000000  # Default standard equipment

    def _calculate_share_change(self, relevant_products: List[Dict], competitive_intensity: float) -> float:
        """Calculate the change in market share based on product strength and competition."""
        if relevant_products:
            # Calculate product strength
            total_revenue = sum(p.get('annual_revenue', 0) for p in relevant_products)
            avg_margin = sum(p.get('profit_margin', 30) for p in relevant_products) / len(relevant_products)
            product_strength = total_revenue * (avg_margin / 100.0) / 1000000  # Normalize

            # Calculate market share change
            base_change = generate_triangular(-0.02, 0.01, 0.05)
            strength_factor = min(2.0, max(0.5, product_strength / 10.0))
            competition_factor = 1.0 - (competitive_intensity * 0.5)
            share_change = base_change * strength_factor * competition_factor
        else:
            # No products in this segment, market share declines
            share_change = -0.1  # 10% decline

        return share_change