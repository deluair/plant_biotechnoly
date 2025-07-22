#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Agent Factory module for the BIOSIMULATE project.

This module provides factory functions for creating different types of agents
in the plant biotechnology industry ecosystem simulation.
"""

import uuid
import random
from typing import Dict, Any, List, Optional, Union, Type

from biosimulate.agents.base_agent import BaseAgent
from biosimulate.agents.research_entity import ResearchEntity
from biosimulate.agents.commercial_player import CommercialPlayer
from biosimulate.agents.regulatory_body import RegulatoryBody
from biosimulate.agents.market_participant import MarketParticipant
from biosimulate.simulation.config import SimulationConfig


class AgentFactory:
    """Factory class for creating different types of agents in the simulation.
    
    This class provides methods for creating various types of agents with
    appropriate parameters based on the simulation configuration.
    """
    
    def __init__(self, config: SimulationConfig):
        """Initialize the agent factory.
        
        Args:
            config: Simulation configuration
        """
        self.config = config
    
    def create_university_lab(self, funding_level: str, research_focus: str, **kwargs) -> ResearchEntity:
        """Create a university research lab agent.
        
        Args:
            funding_level: Funding level ('high', 'medium', 'low')
            research_focus: Research focus area
            **kwargs: Additional parameters
            
        Returns:
            A ResearchEntity instance representing a university lab
        """
        return create_research_entity(
            name=f"University Lab - {research_focus.title()}",
            region=kwargs.get('region', 'global'),
            research_focus=[research_focus],
            research_capacity={
                'high': 80,
                'medium': 60,
                'low': 40
            }.get(funding_level, 50),
            **kwargs
        )
    
    def create_government_institute(self, country: str, budget: float, **kwargs) -> ResearchEntity:
        """Create a government research institute agent.
        
        Args:
            country: Country where the institute is located
            budget: Research budget in millions
            **kwargs: Additional parameters
            
        Returns:
            A ResearchEntity instance representing a government institute
        """
        return create_research_entity(
            name=f"{country.upper()} Government Research Institute",
            region=country,
            research_focus=['breeding', 'gene_editing'] if budget > 50 else ['breeding'],
            research_capacity=min(int(budget * 0.8), 100),
            funding_sources={'government': budget * 1000000},
            **kwargs
        )

    def create_private_rd_company(self, company_size: str, specialization: str, **kwargs) -> ResearchEntity:
        """Create a private R&D company agent.

        Args:
            company_size: Size of the company ('large', 'medium', 'small')
            specialization: Specialization area
            **kwargs: Additional parameters

        Returns:
            A ResearchEntity instance representing a private R&D company
        """
        return create_research_entity(
            name=f"{specialization.title()} R&D Solutions",
            region=kwargs.get('region', 'global'),
            research_focus=[specialization],
            research_capacity={
                'large': 90,
                'medium': 70,
                'small': 50
            }.get(company_size, 60),
            funding_sources={'corporate': 5000000, 'contracts': 2000000},
            **kwargs
        )

    def create_biotech_corporation(self, tier: int, revenue: float, **kwargs) -> CommercialPlayer:
        """Create a biotech corporation agent.

        Args:
            tier: Tier of the corporation (1, 2, or 3)
            revenue: Annual revenue in billions
            **kwargs: Additional parameters

        Returns:
            A CommercialPlayer instance representing a biotech corporation
        """
        return create_commercial_player(
            name=f"Tier {tier} Biotech Corp",
            region=kwargs.get('region', 'global'),
            company_size={
                1: 'large',
                2: 'medium',
                3: 'small'
            }.get(tier, 'medium'),
            market_segments=['grain_crops', 'oilseed_crops'],
            r_and_d_investment=revenue * 0.15,  # 15% of revenue
            **kwargs
        )

    def create_startup(self, focus_area: str, funding: float, **kwargs) -> CommercialPlayer:
        """Create a startup company agent.

        Args:
            focus_area: Focus area of the startup
            funding: Funding raised in millions
            **kwargs: Additional parameters

        Returns:
            A CommercialPlayer instance representing a startup
        """
        return create_commercial_player(
            name=f"{focus_area.title()} Tech Startup",
            region=kwargs.get('region', 'global'),
            company_size='small',
            market_segments=[focus_area],
            r_and_d_investment=funding * 0.5,  # 50% of funding
            **kwargs
        )

    def create_seed_company(self, company_size: str, market_focus: List[str], **kwargs) -> CommercialPlayer:
        """Create a seed company agent.

        Args:
            company_size: Size of the company ('large', 'medium', 'small')
            market_focus: List of market segments to focus on
            **kwargs: Additional parameters

        Returns:
            A CommercialPlayer instance representing a seed company
        """
        return create_commercial_player(
            name=f"{company_size.title()} Seed Company",
            region=kwargs.get('region', 'global'),
            company_size=company_size,
            market_segments=market_focus,
            r_and_d_investment={
                'large': 50000000,
                'medium': 10000000,
                'small': 2000000
            }.get(company_size, 5000000),
            **kwargs
        )

    def create_regulatory_agency(self, region: str, **kwargs) -> RegulatoryBody:
        """Create a regional regulatory agency agent.

        Args:
            region: The region the agency governs
            **kwargs: Additional parameters

        Returns:
            A RegulatoryBody instance
        """
        return create_regulatory_body(
            name=f"{region.upper()} Regulatory Agency",
            region=region,
            jurisdiction=region,
            **kwargs
        )

    def create_harmonization_body(self, name: str, **kwargs) -> RegulatoryBody:
        """Create an international harmonization body agent.

        Args:
            name: Name of the harmonization body
            **kwargs: Additional parameters

        Returns:
            A RegulatoryBody instance
        """
        return create_regulatory_body(
            name=name.replace('_', ' ').title(),
            region='international',
            jurisdiction='international',
            **kwargs
        )

    def create_farmer(self, region: str, size: str, crop_type: str, **kwargs) -> MarketParticipant:
        """Create a farmer agent.

        Args:
            region: Geographic region of the farmer
            size: Size of the farm ('large', 'medium', 'small')
            crop_type: Type of crop grown
            **kwargs: Additional parameters

        Returns:
            A MarketParticipant instance representing a farmer
        """
        return create_market_participant(
            participant_type='farmer',
            name=f"{size.title()} Farmer - {region}",
            region=region,
            size=size,
            market_segments=[crop_type],
            **kwargs
        )

    def create_food_processor(self, size: str, biotech_policy: str, **kwargs) -> MarketParticipant:
        """Create a food processor agent.

        Args:
            size: Size of the company ('large', 'medium', 'small')
            biotech_policy: Policy on biotech products
            **kwargs: Additional parameters

        Returns:
            A MarketParticipant instance representing a food processor
        """
        return create_market_participant(
            participant_type='food_processor',
            name=f"{size.title()} Food Processor",
            region=kwargs.get('region', 'global'),
            size=size,
            market_segments=['processed_foods'],
            biotech_adoption_policy=biotech_policy,
            **kwargs
        )

    def create_consumer_segment(self, region: str, biotech_attitude: str, size: float, **kwargs) -> MarketParticipant:
        """Create a consumer segment agent.

        Args:
            region: Geographic region
            biotech_attitude: Attitude towards biotech ('positive', 'neutral', 'negative')
            size: Size of the segment (percentage)
            **kwargs: Additional parameters

        Returns:
            A MarketParticipant instance representing a consumer segment
        """
        return create_market_participant(
            participant_type='consumer_segment',
            name=f"{biotech_attitude.title()} Consumers - {region}",
            region=region,
            size=size,
            market_segments=['end_consumer'],
            biotech_adoption_policy=biotech_attitude,
            **kwargs
        )

def create_agent(agent_type: str, **kwargs) -> BaseAgent:
    """Create an agent of the specified type with the given parameters.
    
    Args:
        agent_type: Type of agent to create ('research_entity', 'commercial_player',
                   'regulatory_body', or 'market_participant')
        **kwargs: Parameters to pass to the agent constructor
    
    Returns:
        An instance of the specified agent type
    
    Raises:
        ValueError: If the agent type is not recognized
    """
    # Generate a unique ID if not provided
    if 'id' not in kwargs:
        kwargs['id'] = str(uuid.uuid4())
    
    # Create the appropriate agent type
    if agent_type.lower() == 'research_entity':
        return create_research_entity(**kwargs)
    elif agent_type.lower() == 'commercial_player':
        return create_commercial_player(**kwargs)
    elif agent_type.lower() == 'regulatory_body':
        return create_regulatory_body(**kwargs)
    elif agent_type.lower() == 'market_participant':
        return create_market_participant(**kwargs)
    else:
        raise ValueError(f"Unknown agent type: {agent_type}")


def create_research_entity(
    name: str,
    region: str,
    research_focus: List[str],
    research_capacity: int = 50,
    publication_rate: float = 5.0,
    collaboration_tendency: int = 50,
    funding_sources: Dict[str, float] = None,
    patents: List[Dict[str, Any]] = None,
    technologies: List[Dict[str, Any]] = None,
    reputation: int = 50,
    attributes: Dict[str, Any] = None,
    resources: Dict[str, Any] = None,
    state: Dict[str, Any] = None,
    connections: Dict[str, Dict[str, Any]] = None,
    history: List[Dict[str, Any]] = None,
    **kwargs
) -> ResearchEntity:
    """Create a research entity agent.
    
    Args:
        name: Name of the research entity
        region: Geographic region of the research entity
        research_focus: List of research areas the entity focuses on
        research_capacity: Research capacity (0-100)
        publication_rate: Average number of publications per year
        collaboration_tendency: Tendency to collaborate (0-100)
        funding_sources: Dictionary of funding sources and amounts
        patents: List of patents held by the research entity
        technologies: List of technologies developed by the research entity
        reputation: Reputation score (0-100)
        attributes: Additional attributes for the agent
        resources: Resources available to the agent
        state: Initial state of the agent
        connections: Connections to other agents
        history: Historical data for the agent
        **kwargs: Additional parameters
    
    Returns:
        A ResearchEntity instance
    """
    # Initialize default values
    if funding_sources is None:
        funding_sources = {"government": 1000000, "industry": 500000, "grants": 750000}
    
    if patents is None:
        patents = []
    
    if technologies is None:
        technologies = []
    
    # Create and return the research entity
    return ResearchEntity(
        id=kwargs.get('id', str(uuid.uuid4())),
        name=name,
        type="research_entity",
        region=region,
        research_focus=research_focus,
        research_capacity=research_capacity,
        publication_rate=publication_rate,
        collaboration_tendency=collaboration_tendency,
        funding_sources=funding_sources,
        patents=patents,
        technologies=technologies,
        reputation=reputation,
        attributes=attributes or {},
        resources=resources or {},
        state=state or {},
        connections=connections or {},
        history=history or []
    )


def create_commercial_player(
    name: str,
    region: str,
    company_size: str,
    market_segments: List[str],
    technologies: Dict[str, Dict[str, Any]] = None,
    products: Dict[str, Dict[str, Any]] = None,
    r_and_d_investment: float = 0.1,
    innovation_capacity: int = 50,
    market_share: Dict[str, float] = None,
    partnerships: Dict[str, Dict[str, Any]] = None,
    intellectual_property: Dict[str, Dict[str, Any]] = None,
    financial_metrics: Dict[str, float] = None,
    attributes: Dict[str, Any] = None,
    resources: Dict[str, Any] = None,
    state: Dict[str, Any] = None,
    connections: Dict[str, Dict[str, Any]] = None,
    history: List[Dict[str, Any]] = None,
    **kwargs
) -> CommercialPlayer:
    """Create a commercial player agent.
    
    Args:
        name: Name of the commercial player
        region: Geographic region of the commercial player
        company_size: Size of the company ('sme', 'large', or 'multinational')
        market_segments: List of market segments the company operates in
        technologies: Dictionary of technologies owned by the company
        products: Dictionary of products offered by the company
        r_and_d_investment: Percentage of revenue invested in R&D (0.0-1.0)
        innovation_capacity: Innovation capacity (0-100)
        market_share: Dictionary of market segments and market share percentages
        partnerships: Dictionary of partnerships with other entities
        intellectual_property: Dictionary of intellectual property assets
        financial_metrics: Dictionary of financial metrics
        attributes: Additional attributes for the agent
        resources: Resources available to the agent
        state: Initial state of the agent
        connections: Connections to other agents
        history: Historical data for the agent
        **kwargs: Additional parameters
    
    Returns:
        A CommercialPlayer instance
    """
    # Initialize default values
    if technologies is None:
        technologies = []
    
    if products is None:
        products = []
    
    if market_share is None:
        market_share = {segment: 0.0 for segment in market_segments}
    
    if partnerships is None:
        partnerships = []
    
    if intellectual_property is None:
        intellectual_property = []
    
    if financial_metrics is None:
        # Set default financial metrics based on company size
        if company_size.lower() == 'sme':
            financial_metrics = {
                "revenue": 5000000,
                "profit": 500000,
                "capital": 2000000
            }
        elif company_size.lower() == 'large':
            financial_metrics = {
                "revenue": 100000000,
                "profit": 15000000,
                "capital": 50000000
            }
        elif company_size.lower() == 'multinational':
            financial_metrics = {
                "revenue": 1000000000,
                "profit": 200000000,
                "capital": 500000000
            }
        else:
            financial_metrics = {
                "revenue": 0,
                "profit": 0,
                "capital": 0
            }
    
    # Create and return the commercial player
    return CommercialPlayer(
        id=kwargs.get('id', str(uuid.uuid4())),
        name=name,
        type="commercial_player",
        region=region,
        company_size=company_size,
        market_segments=market_segments,
        technologies=technologies,
        products=products,
        r_and_d_investment=r_and_d_investment,
        innovation_capacity=innovation_capacity,
        market_share=market_share,
        partnerships=partnerships,
        intellectual_property=intellectual_property,
        financial_metrics=financial_metrics,
        attributes=attributes or {},
        resources=resources or {},
        state=state or {},
        connections=connections or {},
        history=history or []
    )


def create_regulatory_body(
    name: str,
    region: str,
    jurisdiction: str,
    regulatory_framework: Dict[str, Any] = None,
    approval_processes: Dict[str, Dict[str, Any]] = None,
    standards: Dict[str, Dict[str, Any]] = None,
    enforcement_capacity: int = 70,
    transparency: int = 70,
    risk_tolerance: int = 50,
    political_influence: int = 50,
    pending_applications: List[Dict[str, Any]] = None,
    approved_applications: List[Dict[str, Any]] = None,
    rejected_applications: List[Dict[str, Any]] = None,
    annual_reviews: List[Dict[str, Any]] = None,
    attributes: Dict[str, Any] = None,
    resources: Dict[str, Any] = None,
    state: Dict[str, Any] = None,
    connections: Dict[str, Dict[str, Any]] = None,
    history: List[Dict[str, Any]] = None,
    **kwargs
) -> RegulatoryBody:
    """Create a regulatory body agent.
    
    Args:
        name: Name of the regulatory body
        region: Geographic region of the regulatory body
        jurisdiction: Jurisdiction of the regulatory body
        regulatory_framework: Dictionary describing the regulatory framework
        approval_processes: Dictionary of approval processes
        standards: Dictionary of standards
        enforcement_capacity: Enforcement capacity (0-100)
        transparency: Transparency level (0-100)
        risk_tolerance: Risk tolerance level (0-100)
        political_influence: Political influence level (0-100)
        pending_applications: List of pending applications
        approved_applications: List of approved applications
        rejected_applications: List of rejected applications
        annual_reviews: List of annual reviews
        attributes: Additional attributes for the agent
        resources: Resources available to the agent
        state: Initial state of the agent
        connections: Connections to other agents
        history: Historical data for the agent
        **kwargs: Additional parameters
    
    Returns:
        A RegulatoryBody instance
    """
    # Initialize default values
    if pending_applications is None:
        pending_applications = []
    
    if approved_applications is None:
        approved_applications = []
    
    if rejected_applications is None:
        rejected_applications = []
    
    if annual_reviews is None:
        annual_reviews = []
    
    # Create and return the regulatory body
    return RegulatoryBody(
        id=kwargs.get('id', str(uuid.uuid4())),
        name=name,
        type="regulatory_body",
        region=region,
        jurisdiction=jurisdiction,
        regulatory_framework=regulatory_framework,
        approval_processes=approval_processes,
        standards=standards,
        enforcement_capacity=enforcement_capacity,
        transparency=transparency,
        risk_tolerance=risk_tolerance,
        political_influence=political_influence,
        pending_applications=pending_applications,
        approved_applications=approved_applications,
        rejected_applications=rejected_applications,
        annual_reviews=annual_reviews,
        attributes=attributes or {},
        resources=resources or {},
        state=state or {},
        connections=connections or {},
        history=history or []
    )


def create_market_participant(
    name: str,
    region: str,
    participant_type: str,
    size: str,
    market_segments: List[str] = None,
    technology_adoption: Dict[str, Dict[str, Any]] = None,
    preferences: Dict[str, float] = None,
    risk_aversion: int = 50,
    price_sensitivity: int = 50,
    innovation_openness: int = 50,
    sustainability_focus: int = 50,
    knowledge_level: int = 50,
    social_influence: int = 50,
    economic_status: int = 50,
    satisfaction: int = 50,
    product_portfolio: Dict[str, Dict[str, Any]] = None,
    purchase_history: List[Dict[str, Any]] = None,
    relationships: Dict[str, Dict[str, Any]] = None,
    attributes: Dict[str, Any] = None,
    resources: Dict[str, Any] = None,
    state: Dict[str, Any] = None,
    connections: Dict[str, Dict[str, Any]] = None,
    history: List[Dict[str, Any]] = None,
    **kwargs
) -> MarketParticipant:
    """Create a market participant agent.
    
    Args:
        name: Name of the market participant
        region: Geographic region of the market participant
        participant_type: Type of market participant ('farmer', 'distributor', 'retailer', 'consumer', 'processor')
        size: Size of the market participant ('small', 'medium', 'large')
        market_segments: List of market segments the participant operates in
        technology_adoption: Dictionary of technologies adopted by the participant
        preferences: Dictionary of preferences for different attributes
        risk_aversion: Risk aversion level (0-100)
        price_sensitivity: Price sensitivity level (0-100)
        innovation_openness: Innovation openness level (0-100)
        sustainability_focus: Sustainability focus level (0-100)
        knowledge_level: Knowledge level (0-100)
        social_influence: Social influence level (0-100)
        economic_status: Economic status level (0-100)
        satisfaction: Satisfaction level (0-100)
        product_portfolio: Dictionary of products in the participant's portfolio
        purchase_history: List of purchase history
        relationships: Dictionary of relationships with other entities
        attributes: Additional attributes for the agent
        resources: Resources available to the agent
        state: Initial state of the agent
        connections: Connections to other agents
        history: Historical data for the agent
        **kwargs: Additional parameters
    
    Returns:
        A MarketParticipant instance
    """
    # Initialize default values
    if market_segments is None:
        market_segments = []
    
    if technology_adoption is None:
        technology_adoption = {}
    
    if preferences is None:
        preferences = {}
    
    if product_portfolio is None:
        product_portfolio = {}
    
    if purchase_history is None:
        purchase_history = []
    
    if relationships is None:
        relationships = {}
    
    # Create and return the market participant
    return MarketParticipant(
        id=kwargs.get('id', str(uuid.uuid4())),
        name=name,
        type="market_participant",
        region=region,
        participant_type=participant_type,
        size=size,
        market_segments=market_segments,
        technology_adoption=technology_adoption,
        preferences=preferences,
        risk_aversion=risk_aversion,
        price_sensitivity=price_sensitivity,
        innovation_openness=innovation_openness,
        sustainability_focus=sustainability_focus,
        knowledge_level=knowledge_level,
        social_influence=social_influence,
        economic_status=economic_status,
        satisfaction=satisfaction,
        product_portfolio=product_portfolio,
        purchase_history=purchase_history,
        relationships=relationships,
        attributes=attributes or {},
        resources=resources or {},
        state=state or {},
        connections=connections or {},
        history=history or []
    )


def create_agent_population(
    config: Dict[str, Any],
    agent_counts: Dict[str, int]
) -> Dict[str, List[BaseAgent]]:
    """Create a population of agents based on configuration and counts.
    
    Args:
        config: Configuration dictionary with agent templates
        agent_counts: Dictionary specifying how many of each agent type to create
    
    Returns:
        Dictionary of agent lists by type
    """
    population = {
        "research_entity": [],
        "commercial_player": [],
        "regulatory_body": [],
        "market_participant": []
    }
    
    # Create research entities
    research_templates = config.get("research_entity_templates", [])
    for _ in range(agent_counts.get("research_entity", 0)):
        template = random.choice(research_templates) if research_templates else {}
        agent = create_research_entity(**template)
        population["research_entity"].append(agent)
    
    # Create commercial players
    commercial_templates = config.get("commercial_player_templates", [])
    for _ in range(agent_counts.get("commercial_player", 0)):
        template = random.choice(commercial_templates) if commercial_templates else {}
        agent = create_commercial_player(**template)
        population["commercial_player"].append(agent)
    
    # Create regulatory bodies
    regulatory_templates = config.get("regulatory_body_templates", [])
    for _ in range(agent_counts.get("regulatory_body", 0)):
        template = random.choice(regulatory_templates) if regulatory_templates else {}
        agent = create_regulatory_body(**template)
        population["regulatory_body"].append(agent)
    
    # Create market participants
    market_templates = config.get("market_participant_templates", [])
    for _ in range(agent_counts.get("market_participant", 0)):
        template = random.choice(market_templates) if market_templates else {}
        agent = create_market_participant(**template)
        population["market_participant"].append(agent)
    
    return population