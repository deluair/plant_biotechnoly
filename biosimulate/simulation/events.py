#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Event management for the BIOSIMULATE project.

This module implements the event management system that schedules and
processes events throughout the simulation, such as regulatory changes,
technology breakthroughs, and market disruptions.
"""

import logging
import random
from typing import Dict, List, Any, Optional, Callable

from biosimulate.simulation.config import SimulationConfig


class Event:
    """Represents a scheduled event in the simulation.
    
    Attributes:
        year: Year when the event occurs
        event_type: Type of event
        description: Human-readable description of the event
        params: Additional parameters for the event
        handler: Function to call when the event occurs
    """
    
    def __init__(self, year: int, event_type: str, description: str, 
                params: Dict[str, Any] = None, handler: Callable = None):
        """Initialize an event.
        
        Args:
            year: Year when the event occurs
            event_type: Type of event
            description: Human-readable description of the event
            params: Additional parameters for the event
            handler: Function to call when the event occurs
        """
        self.year = year
        self.event_type = event_type
        self.description = description
        self.params = params or {}
        self.handler = handler
    
    def __str__(self) -> str:
        """Get a string representation of the event."""
        return f"Event({self.year}, {self.event_type}, {self.description})"


class EventManager:
    """Manages events throughout the simulation.
    
    This class schedules and processes events that occur during the simulation,
    such as regulatory changes, technology breakthroughs, and market disruptions.
    
    Attributes:
        config: Simulation configuration
        logger: Logger instance
        events: Dictionary of events by year
    """
    
    def __init__(self, config: SimulationConfig):
        """Initialize the event manager.
        
        Args:
            config: Simulation configuration
        """
        self.config = config
        self.logger = logging.getLogger(__name__)
        self.events = {}
        
        # Schedule events based on the scenario
        self._schedule_events()
        
        self.logger.info(f"Initialized event manager with {sum(len(events) for events in self.events.values())} events")
    
    def _schedule_events(self) -> None:
        """Schedule events based on the scenario."""
        # Schedule common events that occur in all scenarios
        self._schedule_common_events()
        
        # Schedule scenario-specific events
        if self.config.scenario == 'baseline':
            self._schedule_baseline_events()
        elif self.config.scenario == 'regulatory_harmonization':
            self._schedule_regulatory_harmonization_events()
        elif self.config.scenario == 'climate_crisis':
            self._schedule_climate_crisis_events()
        elif self.config.scenario == 'tech_breakthrough':
            self._schedule_tech_breakthrough_events()
        elif self.config.scenario == 'market_disruption':
            self._schedule_market_disruption_events()
    
    def _schedule_common_events(self) -> None:
        """Schedule common events that occur in all scenarios."""
        # Schedule regular technology improvements
        for year in range(self.config.start_year + 1, self.config.end_year + 1):
            # Annual CRISPR efficiency improvements
            self.schedule_event(
                Event(
                    year=year,
                    event_type='technology_improvement',
                    description=f"Annual CRISPR efficiency improvement in {year}",
                    params={
                        'technology': 'crispr',
                        'improvement_type': 'efficiency',
                        'improvement_value': 0.02  # 2% improvement
                    }
                )
            )
            
            # Annual breeding technology improvements
            self.schedule_event(
                Event(
                    year=year,
                    event_type='technology_improvement',
                    description=f"Annual breeding technology improvement in {year}",
                    params={
                        'technology': 'breeding',
                        'improvement_type': 'cycle_time',
                        'improvement_value': 0.03  # 3% improvement
                    }
                )
            )
        
        # Schedule periodic market reports
        for year in range(self.config.start_year, self.config.end_year + 1):
            self.schedule_event(
                Event(
                    year=year,
                    event_type='market_report',
                    description=f"Annual market report for {year}",
                    params={
                        'report_type': 'annual',
                        'year': year
                    }
                )
            )
        
        # Schedule periodic regulatory reviews
        for year in range(self.config.start_year, self.config.end_year + 1, 2):  # Every 2 years
            self.schedule_event(
                Event(
                    year=year,
                    event_type='regulatory_review',
                    description=f"Biennial regulatory review in {year}",
                    params={
                        'review_type': 'biennial',
                        'regions': ['usa', 'eu', 'asia_pacific', 'latin_america']
                    }
                )
            )
    
    def _schedule_baseline_events(self) -> None:
        """Schedule events for the baseline scenario."""
        # Moderate technology breakthroughs
        self.schedule_event(
            Event(
                year=self.config.start_year + 3,  # 2028
                event_type='technology_breakthrough',
                description="Moderate CRISPR delivery system breakthrough",
                params={
                    'technology': 'crispr',
                    'breakthrough_type': 'delivery',
                    'impact_level': 'moderate',
                    'success_rate_improvement': 0.1  # 10 percentage points
                }
            )
        )
        
        self.schedule_event(
            Event(
                year=self.config.start_year + 6,  # 2031
                event_type='technology_breakthrough',
                description="Moderate synthetic biology cost reduction",
                params={
                    'technology': 'synthetic_biology',
                    'breakthrough_type': 'cost',
                    'impact_level': 'moderate',
                    'cost_reduction': 0.15  # 15% cost reduction
                }
            )
        )
        
        # Gradual regulatory changes
        self.schedule_event(
            Event(
                year=self.config.start_year + 4,  # 2029
                event_type='regulatory_change',
                description="Minor EU regulatory framework update",
                params={
                    'region': 'eu',
                    'change_type': 'framework_update',
                    'impact_level': 'minor',
                    'approval_time_change': -0.5  # 6 months faster
                }
            )
        )
        
        # Market developments
        self.schedule_event(
            Event(
                year=self.config.start_year + 2,  # 2027
                event_type='market_development',
                description="New premium market segment emerges for sustainable crops",
                params={
                    'development_type': 'new_segment',
                    'segment': 'sustainable_premium',
                    'initial_size': 0.05,  # 5% of total market
                    'growth_rate': 0.1  # 10% annual growth
                }
            )
        )
    
    def _schedule_regulatory_harmonization_events(self) -> None:
        """Schedule events for the regulatory harmonization scenario."""
        # Major regulatory harmonization initiatives
        self.schedule_event(
            Event(
                year=self.config.start_year + 1,  # 2026
                event_type='regulatory_change',
                description="US-EU Regulatory Cooperation Initiative launched",
                params={
                    'regions': ['usa', 'eu'],
                    'change_type': 'cooperation_initiative',
                    'impact_level': 'major',
                    'approval_time_change': -1.0  # 1 year faster
                }
            )
        )
        
        self.schedule_event(
            Event(
                year=self.config.start_year + 3,  # 2028
                event_type='regulatory_change',
                description="Global Gene Editing Standards Framework adopted",
                params={
                    'regions': ['global'],
                    'change_type': 'standards_framework',
                    'impact_level': 'major',
                    'compliance_cost_reduction': 0.2  # 20% cost reduction
                }
            )
        )
        
        self.schedule_event(
            Event(
                year=self.config.start_year + 5,  # 2030
                event_type='regulatory_change',
                description="EU adopts product-based regulation for gene editing",
                params={
                    'region': 'eu',
                    'change_type': 'regulatory_approach',
                    'impact_level': 'transformative',
                    'approval_time_change': -3.0  # 3 years faster
                }
            )
        )
        
        # Market responses to harmonization
        self.schedule_event(
            Event(
                year=self.config.start_year + 2,  # 2027
                event_type='market_development',
                description="Surge in cross-border biotech investments",
                params={
                    'development_type': 'investment_surge',
                    'investment_increase': 0.3,  # 30% increase
                    'regions': ['global']
                }
            )
        )
        
        self.schedule_event(
            Event(
                year=self.config.start_year + 4,  # 2029
                event_type='market_development',
                description="Wave of international biotech mergers and acquisitions",
                params={
                    'development_type': 'ma_activity',
                    'activity_level': 'high',
                    'market_concentration_change': 0.1  # 10% increase
                }
            )
        )
    
    def _schedule_climate_crisis_events(self) -> None:
        """Schedule events for the climate crisis scenario."""
        # Climate crisis events
        self.schedule_event(
            Event(
                year=self.config.start_year + 1,  # 2026
                event_type='climate_event',
                description="Severe drought affects major agricultural regions",
                params={
                    'event_type': 'drought',
                    'regions': ['north_america', 'europe'],
                    'severity': 'high',
                    'yield_impact': -0.2  # 20% yield reduction
                }
            )
        )
        
        self.schedule_event(
            Event(
                year=self.config.start_year + 3,  # 2028
                event_type='climate_event',
                description="Extreme heat waves disrupt global crop production",
                params={
                    'event_type': 'heat_wave',
                    'regions': ['global'],
                    'severity': 'extreme',
                    'yield_impact': -0.15  # 15% yield reduction
                }
            )
        )
        
        self.schedule_event(
            Event(
                year=self.config.start_year + 5,  # 2030
                event_type='climate_event',
                description="Catastrophic flooding in major agricultural regions",
                params={
                    'event_type': 'flooding',
                    'regions': ['asia_pacific', 'latin_america'],
                    'severity': 'catastrophic',
                    'yield_impact': -0.25  # 25% yield reduction
                }
            )
        )
        
        # Policy responses
        self.schedule_event(
            Event(
                year=self.config.start_year + 2,  # 2027
                event_type='policy_change',
                description="Global Climate Resilience Initiative for Agriculture",
                params={
                    'policy_type': 'resilience_initiative',
                    'regions': ['global'],
                    'funding_increase': 0.5  # 50% funding increase
                }
            )
        )
        
        self.schedule_event(
            Event(
                year=self.config.start_year + 4,  # 2029
                event_type='regulatory_change',
                description="Emergency approval pathways for climate-resilient crops",
                params={
                    'regions': ['global'],
                    'change_type': 'emergency_pathway',
                    'impact_level': 'major',
                    'approval_time_change': -2.0  # 2 years faster
                }
            )
        )
        
        # Technology responses
        self.schedule_event(
            Event(
                year=self.config.start_year + 2,  # 2027
                event_type='technology_breakthrough',
                description="Breakthrough in drought-tolerance traits",
                params={
                    'technology': 'crispr',
                    'breakthrough_type': 'drought_tolerance',
                    'impact_level': 'major',
                    'yield_protection': 0.3  # 30% yield protection
                }
            )
        )
    
    def _schedule_tech_breakthrough_events(self) -> None:
        """Schedule events for the technology breakthrough scenario."""
        # Major technology breakthroughs
        self.schedule_event(
            Event(
                year=self.config.start_year + 1,  # 2026
                event_type='technology_breakthrough',
                description="Revolutionary CRISPR delivery system breakthrough",
                params={
                    'technology': 'crispr',
                    'breakthrough_type': 'delivery',
                    'impact_level': 'revolutionary',
                    'success_rate_improvement': 0.3  # 30 percentage points
                }
            )
        )
        
        self.schedule_event(
            Event(
                year=self.config.start_year + 2,  # 2027
                event_type='technology_breakthrough',
                description="Major breakthrough in off-target effect elimination",
                params={
                    'technology': 'crispr',
                    'breakthrough_type': 'precision',
                    'impact_level': 'major',
                    'precision_improvement': 0.08  # 8 percentage points
                }
            )
        )
        
        self.schedule_event(
            Event(
                year=self.config.start_year + 3,  # 2028
                event_type='technology_breakthrough',
                description="AI-accelerated breeding platform breakthrough",
                params={
                    'technology': 'breeding',
                    'breakthrough_type': 'ai_acceleration',
                    'impact_level': 'revolutionary',
                    'cycle_time_reduction': 0.5  # 50% reduction
                }
            )
        )
        
        self.schedule_event(
            Event(
                year=self.config.start_year + 4,  # 2029
                event_type='technology_breakthrough',
                description="Synthetic biology metabolic pathway engineering breakthrough",
                params={
                    'technology': 'synthetic_biology',
                    'breakthrough_type': 'metabolic_engineering',
                    'impact_level': 'major',
                    'efficiency_improvement': 0.4  # 40% improvement
                }
            )
        )
        
        # Market and regulatory responses
        self.schedule_event(
            Event(
                year=self.config.start_year + 2,  # 2027
                event_type='market_development',
                description="Venture capital funding surge for biotech startups",
                params={
                    'development_type': 'funding_surge',
                    'funding_increase': 0.8,  # 80% increase
                    'target': 'startups'
                }
            )
        )
        
        self.schedule_event(
            Event(
                year=self.config.start_year + 3,  # 2028
                event_type='regulatory_change',
                description="Regulatory frameworks updated for breakthrough technologies",
                params={
                    'regions': ['usa', 'eu', 'asia_pacific'],
                    'change_type': 'framework_update',
                    'impact_level': 'moderate',
                    'approval_time_change': -1.0  # 1 year faster
                }
            )
        )
    
    def _schedule_market_disruption_events(self) -> None:
        """Schedule events for the market disruption scenario."""
        # Market disruption events
        self.schedule_event(
            Event(
                year=self.config.start_year + 1,  # 2026
                event_type='market_disruption',
                description="Major tech company enters agricultural biotechnology market",
                params={
                    'disruption_type': 'new_entrant',
                    'entrant_type': 'tech_company',
                    'market_share_impact': 0.05,  # 5% market share
                    'investment_level': 'massive'  # $5B+ investment
                }
            )
        )
        
        self.schedule_event(
            Event(
                year=self.config.start_year + 2,  # 2027
                event_type='market_disruption',
                description="Alternative protein industry growth accelerates",
                params={
                    'disruption_type': 'alternative_protein',
                    'growth_rate': 0.3,  # 30% annual growth
                    'land_use_impact': -0.05  # 5% reduction in crop land
                }
            )
        )
        
        self.schedule_event(
            Event(
                year=self.config.start_year + 3,  # 2028
                event_type='market_disruption',
                description="Global trade war impacts agricultural markets",
                params={
                    'disruption_type': 'trade_war',
                    'regions': ['global'],
                    'tariff_increase': 0.2,  # 20% tariff increase
                    'trade_volume_impact': -0.15  # 15% reduction
                }
            )
        )
        
        self.schedule_event(
            Event(
                year=self.config.start_year + 4,  # 2029
                event_type='market_disruption',
                description="Major biotech patent invalidation shakes industry",
                params={
                    'disruption_type': 'patent_invalidation',
                    'technology': 'crispr',
                    'market_impact': 'severe',
                    'licensing_revenue_impact': -0.3  # 30% reduction
                }
            )
        )
        
        # Industry responses
        self.schedule_event(
            Event(
                year=self.config.start_year + 2,  # 2027
                event_type='market_development',
                description="Wave of defensive mergers in response to disruption",
                params={
                    'development_type': 'ma_activity',
                    'activity_level': 'very_high',
                    'market_concentration_change': 0.2  # 20% increase
                }
            )
        )
        
        self.schedule_event(
            Event(
                year=self.config.start_year + 3,  # 2028
                event_type='market_development',
                description="Industry-wide open innovation initiative launched",
                params={
                    'development_type': 'open_innovation',
                    'participation_rate': 0.6,  # 60% of companies
                    'rd_efficiency_impact': 0.15  # 15% improvement
                }
            )
        )
    
    def schedule_event(self, event: Event) -> None:
        """Schedule an event to occur at a specific year.
        
        Args:
            event: Event to schedule
        """
        if event.year not in self.events:
            self.events[event.year] = []
        
        self.events[event.year].append(event)
        self.logger.debug(f"Scheduled event: {event}")
    
    def process_events(self, year: int) -> List[Event]:
        """Process all events scheduled for a specific year.
        
        Args:
            year: Year to process events for
            
        Returns:
            List of events that were processed
        """
        if year not in self.events:
            return []
        
        events = self.events[year]
        self.logger.info(f"Processing {len(events)} events for year {year}")
        
        for event in events:
            self.logger.info(f"Event: {event.description}")
            
            # Call the event handler if one is provided
            if event.handler is not None:
                event.handler(event)
        
        return events
    
    def get_all_events(self) -> Dict[int, List[Event]]:
        """Get all scheduled events.
        
        Returns:
            Dictionary of events by year
        """
        return self.events
    
    def get_events_for_year(self, year: int) -> List[Event]:
        """Get all events scheduled for a specific year.
        
        Args:
            year: Year to get events for
            
        Returns:
            List of events scheduled for the year
        """
        return self.events.get(year, [])