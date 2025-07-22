#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Research entity agent class for the BIOSIMULATE project.

This module defines the ResearchEntity class that represents research institutions,
universities, and public/private research organizations in the simulation.
"""

import logging
import random
from typing import Dict, List, Any, Optional, Set, Tuple
from dataclasses import dataclass, field

from biosimulate.agents.base_agent import BaseAgent
from biosimulate.utils.data_generator import generate_normal, generate_triangular

logger = logging.getLogger(__name__)


@dataclass
class ResearchEntity(BaseAgent):
    """Class representing research institutions in the simulation.
    
    Attributes:
        research_focus (List[str]): List of research areas the entity focuses on
        research_capacity (float): Capacity for conducting research (0-100)
        publication_rate (float): Rate of publishing research findings (papers per year)
        collaboration_tendency (float): Tendency to collaborate with other entities (0-1)
        funding_sources (Dict[str, float]): Sources of funding and their amounts
        patents (List[Dict]): List of patents held by the entity
        technologies (List[Dict]): List of technologies developed by the entity
        reputation (float): Reputation score (0-100)
    """
    
    research_focus: List[str] = field(default_factory=list)
    research_capacity: float = 50.0
    publication_rate: float = 5.0
    collaboration_tendency: float = 0.5
    funding_sources: Dict[str, float] = field(default_factory=dict)
    patents: List[Dict] = field(default_factory=list)
    technologies: List[Dict] = field(default_factory=list)
    reputation: float = 50.0
    
    def __post_init__(self):
        """Initialize additional attributes after dataclass initialization."""
        super().__post_init__()
        
        # Set type to 'research' if not specified
        if self.type != 'research':
            self.type = 'research'
            logger.warning(f"Agent type overridden to 'research' for {self.name}")
        
        # Initialize resources if not provided
        if 'funding' not in self.resources:
            self.resources['funding'] = 1000000.0  # Initial funding in currency units
        
        if 'researchers' not in self.resources:
            self.resources['researchers'] = int(self.research_capacity / 10)  # Number of researchers
        
        if 'equipment' not in self.resources:
            self.resources['equipment'] = int(self.research_capacity / 5)  # Research equipment units
        
        # Initialize state variables if not provided
        if 'current_projects' not in self.state:
            self.state['current_projects'] = []  # List of current research projects
        
        if 'publications' not in self.state:
            self.state['publications'] = []  # List of publications
        
        if 'collaborations' not in self.state:
            self.state['collaborations'] = []  # List of current collaborations
    
    def step(self, year: int, context: Dict[str, Any]) -> Dict[str, Any]:
        """Advance the research entity by one time step (year).
        
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
        
        # Decide on research projects to pursue
        actions['research_projects'] = self._decide_research_projects(context)
        
        # Decide on collaboration opportunities
        actions['collaborations'] = self._decide_collaborations(context)
        
        # Decide on patent applications
        actions['patent_applications'] = self._decide_patent_applications(context)
        
        # Decide on technology development
        actions['technology_development'] = self._decide_technology_development(context)
        
        # Decide on funding applications
        actions['funding_applications'] = self._decide_funding_applications(context)
        
        # Decide on publications
        actions['publications'] = self._decide_publications(context)
        
        return actions
    
    def _update_state(self, year: int, actions: Dict[str, Any], context: Dict[str, Any]) -> None:
        """Update agent state based on actions and context.
        
        Args:
            year: Current simulation year
            actions: Actions taken by the agent
            context: Contextual information
        """
        # Update current projects
        self._update_projects(actions, context)
        
        # Update collaborations
        self._update_collaborations(actions, context)
        
        # Update patents
        self._update_patents(actions, context)
        
        # Update technologies
        self._update_technologies(actions, context)
        
        # Update funding
        self._update_funding(actions, context)
        
        # Update publications
        self._update_publications(actions, context)
        
        # Update reputation
        self._update_reputation(context)
        
        # Update resources
        self._update_resources(context)
    
    def _decide_research_projects(self, context: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Decide on research projects to pursue.
        
        Args:
            context: Contextual information for decision making
            
        Returns:
            List of research projects to pursue
        """
        new_projects = []
        
        # Get available technologies and research areas from context
        available_technologies = context.get('available_technologies', [])
        research_areas = context.get('research_areas', [])
        
        # Filter technologies based on research focus
        relevant_technologies = [tech for tech in available_technologies 
                               if any(focus in tech.get('areas', []) for focus in self.research_focus)]
        
        # Determine number of new projects based on research capacity and current projects
        current_projects = self.state.get('current_projects', [])
        max_projects = max(1, int(self.research_capacity / 20))  # 1 project per 20 units of capacity
        num_new_projects = max(0, max_projects - len(current_projects))
        
        # Adjust based on available funding and researchers
        funding_factor = min(1.0, self.resources.get('funding', 0) / 500000)  # Need 500k per project
        researcher_factor = min(1.0, self.resources.get('researchers', 0) / 5)  # Need 5 researchers per project
        num_new_projects = int(num_new_projects * min(funding_factor, researcher_factor))
        
        # Create new projects
        for _ in range(num_new_projects):
            # Select a technology or research area to focus on
            if relevant_technologies and random.random() < 0.7:  # 70% chance to focus on relevant technology
                tech = random.choice(relevant_technologies)
                focus = tech.get('name', 'Unknown Technology')
                areas = tech.get('areas', [])
            else:  # Otherwise, select from research focus areas
                focus = random.choice(self.research_focus) if self.research_focus else 'General Research'
                areas = [focus]
            
            # Determine project parameters
            duration = random.randint(1, 3)  # 1-3 years
            cost = generate_triangular(300000, 500000, 1000000)  # Cost between 300k and 1M
            success_probability = generate_triangular(0.3, 0.5, 0.8)  # 30-80% success probability
            
            # Create project
            project = {
                'name': f"{focus} Research Project",
                'focus': focus,
                'areas': areas,
                'start_year': context.get('year', 0),
                'duration': duration,
                'cost': cost,
                'annual_cost': cost / duration,
                'success_probability': success_probability,
                'progress': 0.0,  # 0-100%
                'researchers_assigned': max(1, int(cost / 200000)),  # 1 researcher per 200k
                'collaborators': []
            }
            
            new_projects.append(project)
        
        return new_projects
    
    def _decide_collaborations(self, context: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Decide on collaboration opportunities.
        
        Args:
            context: Contextual information for decision making
            
        Returns:
            List of collaboration opportunities to pursue
        """
        new_collaborations = []
        
        # Only consider collaborations if tendency is high enough
        if random.random() > self.collaboration_tendency:
            return new_collaborations
        
        # Get potential collaborators from context
        potential_collaborators = context.get('research_entities', [])
        potential_collaborators += context.get('commercial_players', [])
        
        # Filter out self and current collaborators
        current_collaborations = self.state.get('collaborations', [])
        current_collaborator_ids = [collab.get('entity_id') for collab in current_collaborations]
        potential_collaborators = [entity for entity in potential_collaborators 
                                 if entity.get('id') != self.id and entity.get('id') not in current_collaborator_ids]
        
        # Determine number of new collaborations based on capacity and current collaborations
        max_collaborations = max(1, int(self.research_capacity / 25))  # 1 collaboration per 25 units of capacity
        num_new_collaborations = max(0, max_collaborations - len(current_collaborations))
        
        # Adjust based on collaboration tendency
        num_new_collaborations = int(num_new_collaborations * self.collaboration_tendency)
        
        # Create new collaborations
        for _ in range(min(num_new_collaborations, len(potential_collaborators))):
            # Select a collaborator
            collaborator = random.choice(potential_collaborators)
            potential_collaborators.remove(collaborator)  # Don't select the same collaborator twice
            
            # Determine collaboration parameters
            duration = random.randint(1, 5)  # 1-5 years
            
            # Find overlapping research areas
            collaborator_focus = collaborator.get('research_focus', [])
            if not collaborator_focus and collaborator.get('type') == 'commercial':
                collaborator_focus = collaborator.get('market_segments', [])
            
            overlapping_areas = [area for area in self.research_focus if area in collaborator_focus]
            if not overlapping_areas and (self.research_focus and collaborator_focus):
                # If no overlap, pick one area from each
                focus_area = f"{random.choice(self.research_focus)} + {random.choice(collaborator_focus)}"
            elif overlapping_areas:
                focus_area = random.choice(overlapping_areas)
            else:
                focus_area = "Joint Research"
            
            # Create collaboration
            collaboration = {
                'entity_id': collaborator.get('id'),
                'entity_name': collaborator.get('name'),
                'entity_type': collaborator.get('type'),
                'focus_area': focus_area,
                'start_year': context.get('year', 0),
                'duration': duration,
                'strength': generate_triangular(0.3, 0.6, 0.9),  # 30-90% collaboration strength
                'projects': [],  # Will be filled with joint projects
                'publications': [],  # Will be filled with joint publications
                'patents': []  # Will be filled with joint patents
            }
            
            new_collaborations.append(collaboration)
        
        return new_collaborations
    
    def _decide_patent_applications(self, context: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Decide on patent applications.
        
        Args:
            context: Contextual information for decision making
            
        Returns:
            List of patent applications to submit
        """
        new_patent_applications = []
        
        # Check completed projects for patentable results
        current_projects = self.state.get('current_projects', [])
        completed_projects = [project for project in current_projects 
                            if project.get('progress', 0) >= 100.0]
        
        for project in completed_projects:
            # Determine if project results are patentable\            
            patentability = generate_triangular(0.1, 0.3, 0.7)  # 10-70% chance of patentability
            
            # Adjust based on project success and focus area
            if 'CRISPR' in project.get('focus', '') or 'Gene Editing' in project.get('focus', ''):
                patentability *= 1.5  # Higher chance for CRISPR/gene editing
            
            if 'Synthetic Biology' in project.get('focus', ''):
                patentability *= 1.3  # Higher chance for synthetic biology
            
            # Decide whether to apply for patent
            if random.random() < patentability:
                # Create patent application
                patent = {
                    'title': f"Patent for {project.get('name', 'Research Project')}",
                    'description': f"Patent based on research in {project.get('focus', 'Unknown Area')}",
                    'areas': project.get('areas', []),
                    'application_year': context.get('year', 0),
                    'approval_probability': generate_triangular(0.4, 0.6, 0.8),  # 40-80% approval probability
                    'approval_time': random.randint(1, 3),  # 1-3 years for approval
                    'value': generate_triangular(100000, 500000, 2000000),  # Value between 100k and 2M
                    'status': 'pending',
                    'project_id': project.get('id', ''),
                    'collaborators': project.get('collaborators', [])
                }
                
                new_patent_applications.append(patent)
        
        return new_patent_applications
    
    def _decide_technology_development(self, context: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Decide on technology development initiatives.
        
        Args:
            context: Contextual information for decision making
            
        Returns:
            List of technology development initiatives to pursue
        """
        new_technologies = []
        
        # Check patents for technology development opportunities
        approved_patents = [patent for patent in self.patents 
                          if patent.get('status', '') == 'approved']
        
        # Also consider completed projects with high progress
        current_projects = self.state.get('current_projects', [])
        promising_projects = [project for project in current_projects 
                            if project.get('progress', 0) >= 90.0]
        
        # Combine patents and promising projects as technology sources
        tech_sources = approved_patents + promising_projects
        
        # Determine number of new technologies based on capacity and resources
        max_technologies = max(1, int(self.research_capacity / 30))  # 1 technology per 30 units of capacity
        current_technologies = self.technologies
        num_new_technologies = max(0, max_technologies - len(current_technologies))
        
        # Adjust based on available funding and researchers
        funding_factor = min(1.0, self.resources.get('funding', 0) / 1000000)  # Need 1M per technology
        researcher_factor = min(1.0, self.resources.get('researchers', 0) / 10)  # Need 10 researchers per technology
        num_new_technologies = int(num_new_technologies * min(funding_factor, researcher_factor))
        
        # Create new technologies from available sources
        for _ in range(min(num_new_technologies, len(tech_sources))):
            # Select a source for technology
            source = random.choice(tech_sources)
            tech_sources.remove(source)  # Don't select the same source twice
            
            # Determine technology parameters
            if 'title' in source:  # It's a patent
                name = f"Technology based on {source.get('title', 'Patent')}"
                areas = source.get('areas', [])
                source_type = 'patent'
                source_id = source.get('id', '')
            else:  # It's a project
                name = f"Technology from {source.get('name', 'Project')}"
                areas = source.get('areas', [])
                source_type = 'project'
                source_id = source.get('id', '')
            
            # Create technology
            technology = {
                'name': name,
                'description': f"Technology developed in {', '.join(areas)}",
                'areas': areas,
                'development_year': context.get('year', 0),
                'development_cost': generate_triangular(500000, 1000000, 2000000),  # Cost between 500k and 2M
                'maturity': generate_triangular(0.1, 0.3, 0.5),  # Initial maturity 10-50%
                'commercial_potential': generate_triangular(0.3, 0.5, 0.8),  # 30-80% commercial potential
                'source_type': source_type,
                'source_id': source_id,
                'collaborators': source.get('collaborators', [])
            }
            
            new_technologies.append(technology)
        
        return new_technologies
    
    def _decide_funding_applications(self, context: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Decide on funding applications.
        
        Args:
            context: Contextual information for decision making
            
        Returns:
            List of funding applications to submit
        """
        funding_applications = []
        
        # Get available funding sources from context
        available_funding = context.get('funding_opportunities', [])
        
        # Filter funding sources based on eligibility
        eligible_funding = []
        for funding in available_funding:
            # Check if entity type matches
            entity_types = funding.get('eligible_entities', [])
            if 'research' in entity_types or 'all' in entity_types:
                # Check if research areas match
                funding_areas = funding.get('research_areas', [])
                if not funding_areas or any(area in self.research_focus for area in funding_areas):
                    eligible_funding.append(funding)
        
        # Determine number of applications based on capacity and current funding
        max_applications = max(1, int(self.research_capacity / 15))  # 1 application per 15 units of capacity
        
        # Adjust based on current funding level
        current_funding = self.resources.get('funding', 0)
        funding_need_factor = max(0.1, min(1.0, 2000000 / current_funding))  # Higher need if funding is low
        num_applications = int(max_applications * funding_need_factor)
        
        # Create funding applications
        for _ in range(min(num_applications, len(eligible_funding))):
            # Select a funding opportunity
            funding = random.choice(eligible_funding)
            eligible_funding.remove(funding)  # Don't select the same opportunity twice
            
            # Determine application parameters
            amount_requested = min(funding.get('max_amount', 1000000), 
                                 max(funding.get('min_amount', 100000), 
                                     generate_triangular(200000, 500000, 1000000)))  # Request between 200k and 1M
            
            # Calculate success probability based on reputation and alignment
            base_success_prob = funding.get('base_success_rate', 0.3)
            reputation_factor = self.reputation / 100  # 0-1 based on reputation
            
            # Calculate alignment with funding priorities
            funding_priorities = funding.get('priorities', [])
            if funding_priorities:
                alignment = sum(1 for focus in self.research_focus if focus in funding_priorities) / len(funding_priorities)
            else:
                alignment = 0.5  # Neutral alignment if no priorities specified
            
            success_probability = base_success_prob * (0.5 + 0.5 * reputation_factor) * (0.5 + 0.5 * alignment)
            success_probability = min(0.9, max(0.1, success_probability))  # Clamp between 10-90%
            
            # Create application
            application = {
                'funding_id': funding.get('id', ''),
                'funding_name': funding.get('name', 'Funding Opportunity'),
                'funding_source': funding.get('source', 'Unknown'),
                'amount_requested': amount_requested,
                'application_year': context.get('year', 0),
                'success_probability': success_probability,
                'decision_time': random.randint(0, 1),  # 0-1 years for decision
                'status': 'pending',
                'research_areas': [area for area in self.research_focus if area in funding.get('research_areas', self.research_focus)]
            }
            
            funding_applications.append(application)
        
        return funding_applications
    
    def _decide_publications(self, context: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Decide on publications to produce.
        
        Args:
            context: Contextual information for decision making
            
        Returns:
            List of publications to produce
        """
        new_publications = []
        
        # Determine number of publications based on publication rate and research capacity
        base_publications = self.publication_rate
        capacity_factor = self.research_capacity / 50  # Normalize to 1.0 at capacity 50
        num_publications = int(base_publications * capacity_factor)
        
        # Adjust based on current projects and their progress
        current_projects = self.state.get('current_projects', [])
        project_factor = min(2.0, max(0.5, len(current_projects) / 3))  # More projects = more publications, up to 2x
        
        # Calculate average project progress
        if current_projects:
            avg_progress = sum(project.get('progress', 0) for project in current_projects) / len(current_projects)
            progress_factor = min(1.5, max(0.5, avg_progress / 50))  # Higher progress = more publications, up to 1.5x
        else:
            progress_factor = 0.5  # Reduced publications if no active projects
        
        num_publications = int(num_publications * project_factor * progress_factor)
        
        # Create publications
        for _ in range(num_publications):
            # Select a research area to publish in
            if current_projects and random.random() < 0.8:  # 80% chance to publish from current project
                project = random.choice(current_projects)
                area = project.get('focus', random.choice(self.research_focus) if self.research_focus else 'General Research')
                project_id = project.get('id', '')
                collaborators = project.get('collaborators', [])
            else:  # Otherwise, select from research focus areas
                area = random.choice(self.research_focus) if self.research_focus else 'General Research'
                project_id = ''
                collaborators = []
            
            # Determine publication parameters
            impact_factor = generate_triangular(0.5, 2.0, 10.0)  # Impact factor between 0.5 and 10
            
            # Adjust impact factor based on reputation
            reputation_factor = self.reputation / 50  # Normalize to 1.0 at reputation 50
            impact_factor *= reputation_factor
            
            # Create publication
            publication = {
                'title': f"Research on {area}",
                'area': area,
                'year': context.get('year', 0),
                'impact_factor': impact_factor,
                'citations': 0,  # Will accumulate over time
                'project_id': project_id,
                'collaborators': collaborators
            }
            
            new_publications.append(publication)
        
        return new_publications
    
    def _update_projects(self, actions: Dict[str, Any], context: Dict[str, Any]) -> None:
        """Update research projects based on actions and context.
        
        Args:
            actions: Actions taken by the agent
            context: Contextual information
        """
        current_projects = self.state.get('current_projects', [])
        
        # Add new projects
        new_projects = actions.get('research_projects', [])
        for project in new_projects:
            # Assign unique ID to project
            if 'id' not in project:
                project['id'] = f"project_{len(current_projects) + 1}_{self.id[-8:]}"
            
            # Deduct initial costs
            initial_cost = project.get('annual_cost', 0)
            self.resources['funding'] = max(0, self.resources.get('funding', 0) - initial_cost)
            
            # Assign researchers
            researchers_needed = project.get('researchers_assigned', 0)
            self.resources['researchers'] = max(0, self.resources.get('researchers', 0) - researchers_needed)
            
            current_projects.append(project)
        
        # Update existing projects
        updated_projects = []
        for project in current_projects:
            # Update progress based on resources and time
            progress_increment = 100.0 / project.get('duration', 1)  # Progress per year based on duration
            
            # Adjust progress based on researchers assigned and funding
            researcher_factor = min(1.2, max(0.5, project.get('researchers_assigned', 0) / 5))  # More researchers = faster progress, up to 1.2x
            funding_factor = min(1.2, max(0.5, self.resources.get('funding', 0) / 500000))  # More funding = faster progress, up to 1.2x
            
            progress_increment *= researcher_factor * funding_factor
            
            # Update progress
            project['progress'] = min(100.0, project.get('progress', 0) + progress_increment)
            
            # Deduct annual costs if project is still ongoing
            if project.get('progress', 0) < 100.0:
                annual_cost = project.get('annual_cost', 0)
                self.resources['funding'] = max(0, self.resources.get('funding', 0) - annual_cost)
                updated_projects.append(project)
            else:
                # Project completed, release researchers
                researchers_released = project.get('researchers_assigned', 0)
                self.resources['researchers'] = self.resources.get('researchers', 0) + researchers_released
                
                # Determine project outcome
                success_probability = project.get('success_probability', 0.5)
                if random.random() < success_probability:
                    # Project successful
                    project['outcome'] = 'success'
                    project['results'] = {
                        'quality': generate_triangular(0.5, 0.8, 1.0),  # Quality between 50-100%
                        'innovation': generate_triangular(0.3, 0.6, 0.9),  # Innovation between 30-90%
                        'commercial_potential': generate_triangular(0.2, 0.5, 0.8)  # Commercial potential between 20-80%
                    }
                    
                    # Add to completed projects
                    if 'completed_projects' not in self.state:
                        self.state['completed_projects'] = []
                    self.state['completed_projects'].append(project)
                else:
                    # Project failed
                    project['outcome'] = 'failure'
                    project['results'] = {
                        'quality': generate_triangular(0.1, 0.3, 0.5),  # Quality between 10-50%
                        'innovation': generate_triangular(0.1, 0.2, 0.4),  # Innovation between 10-40%
                        'commercial_potential': generate_triangular(0.0, 0.1, 0.3)  # Commercial potential between 0-30%
                    }
                    
                    # Add to failed projects
                    if 'failed_projects' not in self.state:
                        self.state['failed_projects'] = []
                    self.state['failed_projects'].append(project)
        
        # Update current projects
        self.state['current_projects'] = updated_projects
    
    def _update_collaborations(self, actions: Dict[str, Any], context: Dict[str, Any]) -> None:
        """Update collaborations based on actions and context.
        
        Args:
            actions: Actions taken by the agent
            context: Contextual information
        """
        current_collaborations = self.state.get('collaborations', [])
        
        # Add new collaborations
        new_collaborations = actions.get('collaborations', [])
        for collaboration in new_collaborations:
            # Assign unique ID to collaboration
            if 'id' not in collaboration:
                collaboration['id'] = f"collab_{len(current_collaborations) + 1}_{self.id[-8:]}"
            
            # Add connection to collaborator
            self.add_connection(collaboration.get('entity_id', ''))
            
            current_collaborations.append(collaboration)
        
        # Update existing collaborations
        updated_collaborations = []
        for collaboration in current_collaborations:
            # Check if collaboration has expired
            start_year = collaboration.get('start_year', 0)
            duration = collaboration.get('duration', 1)
            current_year = context.get('year', 0)
            
            if current_year - start_year < duration:
                # Collaboration still active
                updated_collaborations.append(collaboration)
            else:
                # Collaboration expired, remove connection
                self.remove_connection(collaboration.get('entity_id', ''))
                
                # Add to past collaborations
                if 'past_collaborations' not in self.state:
                    self.state['past_collaborations'] = []
                self.state['past_collaborations'].append(collaboration)
        
        # Update current collaborations
        self.state['collaborations'] = updated_collaborations
    
    def _update_patents(self, actions: Dict[str, Any], context: Dict[str, Any]) -> None:
        """Update patents based on actions and context.
        
        Args:
            actions: Actions taken by the agent
            context: Contextual information
        """
        # Add new patent applications
        new_patents = actions.get('patent_applications', [])
        for patent in new_patents:
            # Assign unique ID to patent
            if 'id' not in patent:
                patent['id'] = f"patent_{len(self.patents) + 1}_{self.id[-8:]}"
            
            self.patents.append(patent)
        
        # Update existing patents
        updated_patents = []
        for patent in self.patents:
            # Check if patent decision time has arrived
            if patent.get('status', '') == 'pending':
                application_year = patent.get('application_year', 0)
                approval_time = patent.get('approval_time', 1)
                current_year = context.get('year', 0)
                
                if current_year - application_year >= approval_time:
                    # Decision time has arrived
                    approval_probability = patent.get('approval_probability', 0.5)
                    if random.random() < approval_probability:
                        # Patent approved
                        patent['status'] = 'approved'
                        patent['approval_year'] = current_year
                        patent['expiration_year'] = current_year + 20  # Patents typically last 20 years
                    else:
                        # Patent rejected
                        patent['status'] = 'rejected'
                        patent['rejection_year'] = current_year
            
            # Check if patent has expired
            if patent.get('status', '') == 'approved':
                expiration_year = patent.get('expiration_year', 0)
                current_year = context.get('year', 0)
                
                if current_year >= expiration_year:
                    # Patent expired
                    patent['status'] = 'expired'
                    patent['expiration_year'] = current_year
            
            updated_patents.append(patent)
        
        # Update patents
        self.patents = updated_patents
    
    def _update_technologies(self, actions: Dict[str, Any], context: Dict[str, Any]) -> None:
        """Update technologies based on actions and context.
        
        Args:
            actions: Actions taken by the agent
            context: Contextual information
        """
        # Add new technologies
        new_technologies = actions.get('technology_development', [])
        for technology in new_technologies:
            # Assign unique ID to technology
            if 'id' not in technology:
                technology['id'] = f"tech_{len(self.technologies) + 1}_{self.id[-8:]}"
            
            # Deduct development costs
            development_cost = technology.get('development_cost', 0)
            self.resources['funding'] = max(0, self.resources.get('funding', 0) - development_cost)
            
            self.technologies.append(technology)
        
        # Update existing technologies
        updated_technologies = []
        for technology in self.technologies:
            # Update technology maturity over time
            maturity_increment = generate_triangular(0.05, 0.1, 0.2)  # 5-20% maturity increase per year
            
            # Adjust based on research capacity and funding
            capacity_factor = min(1.5, max(0.5, self.research_capacity / 50))  # More capacity = faster maturity, up to 1.5x
            funding_factor = min(1.5, max(0.5, self.resources.get('funding', 0) / 500000))  # More funding = faster maturity, up to 1.5x
            
            maturity_increment *= capacity_factor * funding_factor
            
            # Update maturity
            technology['maturity'] = min(1.0, technology.get('maturity', 0) + maturity_increment)
            
            # Update commercial potential based on maturity
            if technology.get('maturity', 0) > 0.7 and 'commercial_readiness' not in technology:
                # Technology is mature enough for commercialization
                technology['commercial_readiness'] = True
                technology['commercialization_year'] = context.get('year', 0)
            
            updated_technologies.append(technology)
        
        # Update technologies
        self.technologies = updated_technologies
    
    def _update_funding(self, actions: Dict[str, Any], context: Dict[str, Any]) -> None:
        """Update funding based on actions and context.
        
        Args:
            actions: Actions taken by the agent
            context: Contextual information
        """
        # Process funding applications
        funding_applications = actions.get('funding_applications', [])
        if 'funding_applications' not in self.state:
            self.state['funding_applications'] = []
        
        for application in funding_applications:
            self.state['funding_applications'].append(application)
        
        # Update existing applications
        updated_applications = []
        for application in self.state.get('funding_applications', []):
            # Check if decision time has arrived
            if application.get('status', '') == 'pending':
                application_year = application.get('application_year', 0)
                decision_time = application.get('decision_time', 0)
                current_year = context.get('year', 0)
                
                if current_year - application_year >= decision_time:
                    # Decision time has arrived
                    success_probability = application.get('success_probability', 0.5)
                    if random.random() < success_probability:
                        # Application approved
                        application['status'] = 'approved'
                        application['approval_year'] = current_year
                        
                        # Add funding
                        amount = application.get('amount_requested', 0)
                        self.resources['funding'] = self.resources.get('funding', 0) + amount
                        
                        # Update funding sources
                        source = application.get('funding_source', 'Unknown')
                        if source in self.funding_sources:
                            self.funding_sources[source] += amount
                        else:
                            self.funding_sources[source] = amount
                    else:
                        # Application rejected
                        application['status'] = 'rejected'
                        application['rejection_year'] = current_year
            
            updated_applications.append(application)
        
        # Update funding applications
        self.state['funding_applications'] = updated_applications
        
        # Add base funding (e.g., institutional funding)
        base_funding = self.attributes.get('base_annual_funding', 200000)  # Default 200k per year
        self.resources['funding'] = self.resources.get('funding', 0) + base_funding
        
        # Update funding sources
        if 'Institution' in self.funding_sources:
            self.funding_sources['Institution'] += base_funding
        else:
            self.funding_sources['Institution'] = base_funding
    
    def _update_publications(self, actions: Dict[str, Any], context: Dict[str, Any]) -> None:
        """Update publications based on actions and context.
        
        Args:
            actions: Actions taken by the agent
            context: Contextual information
        """
        # Add new publications
        new_publications = actions.get('publications', [])
        if 'publications' not in self.state:
            self.state['publications'] = []
        
        for publication in new_publications:
            # Assign unique ID to publication
            if 'id' not in publication:
                publication['id'] = f"pub_{len(self.state['publications']) + 1}_{self.id[-8:]}"
            
            self.state['publications'].append(publication)
        
        # Update existing publications (e.g., accumulate citations)
        for publication in self.state.get('publications', []):
            # Calculate new citations based on impact factor and age
            impact_factor = publication.get('impact_factor', 1.0)
            age = context.get('year', 0) - publication.get('year', 0)
            
            if age <= 5:  # Citations typically peak in the first 5 years
                # Citations follow a curve that peaks around year 2-3
                citation_factor = (age * (5 - age) / 6) + 0.5  # Peaks at 2.5 years with value ~1.5
                new_citations = int(impact_factor * citation_factor * random.triangular(0.5, 1.0, 2.0))
            else:  # Older publications receive fewer citations
                new_citations = int(impact_factor * 0.5 * (0.9 ** (age - 5)) * random.triangular(0, 0.5, 1.0))
            
            publication['citations'] = publication.get('citations', 0) + new_citations
    
    def _update_reputation(self, context: Dict[str, Any]) -> None:
        """Update reputation based on research outputs and context.
        
        Args:
            context: Contextual information
        """
        # Calculate reputation factors
        
        # 1. Publication impact
        publications = self.state.get('publications', [])
        recent_publications = [pub for pub in publications 
                             if context.get('year', 0) - pub.get('year', 0) <= 5]  # Consider last 5 years
        
        if recent_publications:
            total_impact = sum(pub.get('impact_factor', 0) * (pub.get('citations', 0) + 1) 
                             for pub in recent_publications)
            avg_impact = total_impact / len(recent_publications)
            publication_factor = min(2.0, max(0.5, avg_impact / 5))  # Normalize to 1.0 at impact 5
        else:
            publication_factor = 0.8  # Slight decrease if no recent publications
        
        # 2. Patent success
        patents = self.patents
        approved_patents = [patent for patent in patents 
                          if patent.get('status', '') == 'approved']        
        patent_factor = min(1.5, max(0.8, len(approved_patents) / 5 + 0.8))  # Normalize to 1.0 at 5 patents
        
        # 3. Technology development
        technologies = self.technologies
        mature_technologies = [tech for tech in technologies 
                             if tech.get('maturity', 0) >= 0.7]        
        technology_factor = min(1.5, max(0.8, len(mature_technologies) / 3 + 0.8))  # Normalize to 1.0 at 3 mature technologies
        
        # 4. Funding success
        funding_applications = self.state.get('funding_applications', [])
        approved_applications = [app for app in funding_applications 
                               if app.get('status', '') == 'approved']
        
        if funding_applications:
            funding_success_rate = len(approved_applications) / len(funding_applications)
            funding_factor = min(1.5, max(0.7, funding_success_rate * 1.5))  # Normalize to 1.0 at 67% success rate
        else:
            funding_factor = 0.9  # Slight decrease if no funding applications
        
        # 5. Collaboration network
        collaborations = self.state.get('collaborations', [])
        collaboration_factor = min(1.3, max(0.9, len(collaborations) / 5 + 0.9))  # Normalize to 1.0 at 5 collaborations
        
        # Calculate overall reputation change
        reputation_change = self.reputation * (
            0.3 * (publication_factor - 1) +  # 30% weight
            0.2 * (patent_factor - 1) +       # 20% weight
            0.2 * (technology_factor - 1) +   # 20% weight
            0.15 * (funding_factor - 1) +     # 15% weight
            0.15 * (collaboration_factor - 1)  # 15% weight
        )
        
        # Apply change with some random variation
        reputation_change *= random.triangular(0.8, 1.0, 1.2)
        
        # Update reputation
        self.reputation = min(100.0, max(1.0, self.reputation + reputation_change))
    
    def _update_resources(self, context: Dict[str, Any]) -> None:
        """Update resources based on context.
        
        Args:
            context: Contextual information
        """
        # Update researchers (hiring/attrition)
        current_researchers = self.resources.get('researchers', 0)
        
        # Determine researcher changes
        attrition_rate = 0.05  # 5% annual attrition
        growth_rate = 0.1  # 10% annual growth potential
        
        # Adjust based on funding and reputation
        funding_factor = min(1.5, max(0.5, self.resources.get('funding', 0) / 1000000))  # Normalize to 1.0 at 1M funding
        reputation_factor = min(1.5, max(0.5, self.reputation / 50))  # Normalize to 1.0 at reputation 50
        
        # Calculate researcher changes
        researchers_lost = int(current_researchers * attrition_rate * random.triangular(0.5, 1.0, 1.5))
        researchers_gained = int(current_researchers * growth_rate * funding_factor * reputation_factor * random.triangular(0.5, 1.0, 1.5))
        
        # Update researchers
        self.resources['researchers'] = max(1, current_researchers - researchers_lost + researchers_gained)
        
        # Update equipment
        current_equipment = self.resources.get('equipment', 0)
        
        # Equipment depreciation and new purchases
        depreciation_rate = 0.1  # 10% annual depreciation
        equipment_lost = int(current_equipment * depreciation_rate)
        
        # New equipment based on funding
        equipment_budget = self.resources.get('funding', 0) * 0.05  # 5% of funding goes to equipment
        equipment_gained = int(equipment_budget / 50000)  # Each equipment unit costs 50k
        
        # Deduct equipment budget from funding
        self.resources['funding'] = max(0, self.resources.get('funding', 0) - equipment_budget)
        
        # Update equipment
        self.resources['equipment'] = max(1, current_equipment - equipment_lost + equipment_gained)