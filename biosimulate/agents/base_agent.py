#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Base agent class for the BIOSIMULATE project.

This module defines the BaseAgent class that all specific agent types will inherit from.
"""

import uuid
import logging
from typing import Dict, List, Any, Optional, Set, Tuple
from dataclasses import dataclass, field

logger = logging.getLogger(__name__)


@dataclass
class BaseAgent:
    """Base class for all agents in the simulation.
    
    Attributes:
        id (str): Unique identifier for the agent
        name (str): Name of the agent
        type (str): Type of the agent (e.g., 'research', 'commercial', 'regulatory', 'market')
        region (str): Geographic region where the agent is based
        attributes (Dict): Dictionary of agent-specific attributes
        connections (Set): Set of agent IDs this agent is connected to
        resources (Dict): Dictionary of resources the agent possesses
        state (Dict): Current state of the agent
        history (List): History of agent states and actions
    """
    
    name: str
    type: str
    region: str
    attributes: Dict[str, Any] = field(default_factory=dict)
    resources: Dict[str, Any] = field(default_factory=dict)
    state: Dict[str, Any] = field(default_factory=dict)
    connections: Set[str] = field(default_factory=set)
    history: List[Dict[str, Any]] = field(default_factory=list)
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    
    def __post_init__(self):
        """Initialize additional attributes after dataclass initialization."""
        # Set default state values if not provided
        if 'active' not in self.state:
            self.state['active'] = True
        
        # Log agent creation
        logger.debug(f"Created agent: {self.type} - {self.name} in {self.region}")
    
    def step(self, year: int, agents: Dict[str, 'BaseAgent'], technology_pipeline: 'TechnologyPipeline', regulatory_framework: 'RegulatoryFramework', market_model: 'MarketModel') -> Dict[str, Any]:
        """Advance the agent's state by one time step.

        Args:
            year: The current simulation year.
            agents: Dictionary of all agents in the simulation.
            technology_pipeline: The technology pipeline model.
            regulatory_framework: The regulatory framework model.
            market_model: The market model.

        Returns:
            A dictionary containing any actions or results from this step.
        """
        raise NotImplementedError("Subclasses must implement the step method.")
    
    def _make_decisions(self, year: int, context: Dict[str, Any]) -> Dict[str, Any]:
        """Make decisions based on current state and context.
        
        Args:
            year: Current simulation year
            context: Contextual information for decision making
            
        Returns:
            Dictionary of decisions/actions
        """
        # This method should be overridden by subclasses
        return {}
    
    def _update_state(self, year: int, actions: Dict[str, Any], context: Dict[str, Any]) -> None:
        """Update agent state based on actions and context.
        
        Args:
            year: Current simulation year
            actions: Actions taken by the agent
            context: Contextual information
        """
        # This method should be overridden by subclasses
        pass
    
    def _record_history(self, year: int, actions: Dict[str, Any]) -> None:
        """Record current state and actions in history.
        
        Args:
            year: Current simulation year
            actions: Actions taken by the agent
        """
        record = {
            'year': year,
            'state': self.state.copy(),
            'actions': actions,
            'resources': self.resources.copy()
        }
        self.history.append(record)
    
    def add_connection(self, agent_id: str) -> None:
        """Add a connection to another agent.
        
        Args:
            agent_id: ID of the agent to connect with
        """
        self.connections.add(agent_id)
        logger.debug(f"Agent {self.id} connected with {agent_id}")
    
    def remove_connection(self, agent_id: str) -> None:
        """Remove a connection to another agent.
        
        Args:
            agent_id: ID of the agent to disconnect from
        """
        if agent_id in self.connections:
            self.connections.remove(agent_id)
            logger.debug(f"Agent {self.id} disconnected from {agent_id}")
    
    def has_connection(self, agent_id: str) -> bool:
        """Check if this agent is connected to another agent.
        
        Args:
            agent_id: ID of the agent to check connection with
            
        Returns:
            True if connected, False otherwise
        """
        return agent_id in self.connections
    
    def add_resource(self, resource_type: str, amount: Any) -> None:
        """Add a resource to the agent's resources.
        
        Args:
            resource_type: Type of resource
            amount: Amount of resource to add
        """
        if resource_type in self.resources:
            # Handle different resource types appropriately
            if isinstance(self.resources[resource_type], (int, float)) and isinstance(amount, (int, float)):
                self.resources[resource_type] += amount
            elif isinstance(self.resources[resource_type], list) and isinstance(amount, list):
                self.resources[resource_type].extend(amount)
            elif isinstance(self.resources[resource_type], dict) and isinstance(amount, dict):
                self.resources[resource_type].update(amount)
            else:
                # For other types, just replace
                self.resources[resource_type] = amount
        else:
            self.resources[resource_type] = amount
    
    def remove_resource(self, resource_type: str, amount: Any = None) -> Any:
        """Remove a resource from the agent's resources.
        
        Args:
            resource_type: Type of resource
            amount: Amount of resource to remove (if None, removes all)
            
        Returns:
            The amount removed, or None if resource doesn't exist
        """
        if resource_type not in self.resources:
            return None
        
        if amount is None:
            # Remove all of this resource
            removed = self.resources[resource_type]
            del self.resources[resource_type]
            return removed
        
        # Handle different resource types appropriately
        if isinstance(self.resources[resource_type], (int, float)) and isinstance(amount, (int, float)):
            if self.resources[resource_type] >= amount:
                self.resources[resource_type] -= amount
                if self.resources[resource_type] == 0:
                    del self.resources[resource_type]
                return amount
            else:
                available = self.resources[resource_type]
                del self.resources[resource_type]
                return available
        else:
            # For other types, just remove all if requested
            removed = self.resources[resource_type]
            del self.resources[resource_type]
            return removed
    
    def get_resource(self, resource_type: str) -> Any:
        """Get the current amount of a resource.
        
        Args:
            resource_type: Type of resource
            
        Returns:
            The current amount of the resource, or None if it doesn't exist
        """
        return self.resources.get(resource_type)
    
    def set_state(self, key: str, value: Any) -> None:
        """Set a state variable.
        
        Args:
            key: State variable name
            value: State variable value
        """
        self.state[key] = value
    
    def get_state(self, key: str, default: Any = None) -> Any:
        """Get a state variable.
        
        Args:
            key: State variable name
            default: Default value if state variable doesn't exist
            
        Returns:
            The state variable value, or default if it doesn't exist
        """
        return self.state.get(key, default)
    
    def is_active(self) -> bool:
        """Check if the agent is active.
        
        Returns:
            True if active, False otherwise
        """
        return self.state.get('active', True)
    
    def deactivate(self) -> None:
        """Deactivate the agent."""
        self.state['active'] = False
        logger.info(f"Agent {self.name} ({self.id}) deactivated")
    
    def activate(self) -> None:
        """Activate the agent."""
        self.state['active'] = True
        logger.info(f"Agent {self.name} ({self.id}) activated")
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert agent to dictionary representation.
        
        Returns:
            Dictionary representation of the agent
        """
        return {
            'id': self.id,
            'name': self.name,
            'type': self.type,
            'region': self.region,
            'attributes': self.attributes,
            'resources': self.resources,
            'state': self.state,
            'connections': list(self.connections),
            # Don't include full history to keep the dict size manageable
            'history_length': len(self.history)
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'BaseAgent':
        """Create an agent from dictionary representation.
        
        Args:
            data: Dictionary representation of the agent
            
        Returns:
            BaseAgent instance
        """
        # Extract the required fields for initialization
        agent = cls(
            name=data['name'],
            type=data['type'],
            region=data['region'],
            attributes=data.get('attributes', {}),
            resources=data.get('resources', {}),
            state=data.get('state', {}),
            id=data.get('id', str(uuid.uuid4()))
        )
        
        # Set connections
        agent.connections = set(data.get('connections', []))
        
        return agent