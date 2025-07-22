#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Regulatory Framework module for the BIOSIMULATE project.

This module implements the regulatory framework that governs the approval
and regulation of plant biotechnology products in the simulation.
"""

import logging
import random
import uuid
from typing import Dict, List, Any, Optional

from biosimulate.simulation.config import SimulationConfig


class RegulatoryFramework:
    """Regulatory framework for plant biotechnology products.
    
    This class manages the regulatory framework for plant biotechnology products
    in the simulation, including regional regulations, approval processes, and
    policy changes.
    
    Attributes:
        config: Simulation configuration
        regions: Dictionary of regulatory regions and their parameters
        regional_frameworks: Dictionary of regional regulatory frameworks with policies and stringency
        applications: Dictionary of regulatory applications
        approvals: Dictionary of approved products
    """
    
    def __init__(self, config: SimulationConfig):
        """Initialize the regulatory framework.
        
        Args:
            config: Simulation configuration
        """
        self.config = config
        self.logger = logging.getLogger(__name__)
        
        # Initialize regulatory regions
        self.regions = self._initialize_regions()
        
        # Initialize regional frameworks with policies and stringency levels
        self.regional_frameworks = self._initialize_regional_frameworks()
        
        # Initialize regulations
        self.regulations = self._initialize_regulations()
        
        # Initialize application and approval tracking
        self.applications = {}
        self.approvals = {}
        self.approval_history = []
        
        # Initialize approval process
        from biosimulate.regulatory.approval import ApprovalProcess
        self.approval_process = ApprovalProcess(config, self)
    
    def _initialize_regions(self) -> Dict[str, Dict[str, Any]]:
        """Initialize regulatory regions and their parameters.
        
        Returns:
            Dictionary of regulatory regions and their parameters
        """
        # Default regulatory parameters if not in config
        regulatory_params = getattr(self.config, 'params', {}).get('regulatory', {})
        approval_time_mean = regulatory_params.get('approval_time_mean', 3.0)  # Default: 3 years
        approval_time_std = regulatory_params.get('approval_time_std', 1.0)   # Default: 1 year std dev
        
        regions = {
            "usa": {
                "name": "United States",
                "approval_time_mean": approval_time_mean,
                "approval_time_std": approval_time_std,
                "approval_probability": 0.8,
                "data_requirements": {
                    "safety": 0.7,
                    "efficacy": 0.6,
                    "environmental": 0.5
                },
                "regulatory_agencies": ["fda", "usda", "epa"]
            },
            "eu": {
                "name": "European Union",
                "approval_time_mean": approval_time_mean * 1.5,
                "approval_time_std": approval_time_std * 1.2,
                "approval_probability": 0.6,
                "data_requirements": {
                    "safety": 0.9,
                    "efficacy": 0.7,
                    "environmental": 0.8
                },
                "regulatory_agencies": ["efsa", "ec"]
            },
            "china": {
                "name": "China",
                "approval_time_mean": approval_time_mean * 1.2,
                "approval_time_std": approval_time_std * 1.1,
                "approval_probability": 0.7,
                "data_requirements": {
                    "safety": 0.8,
                    "efficacy": 0.8,
                    "environmental": 0.6
                },
                "regulatory_agencies": ["moa"]
            },
            "brazil": {
                "name": "Brazil",
                "approval_time_mean": approval_time_mean * 1.1,
                "approval_time_std": approval_time_std * 1.0,
                "approval_probability": 0.75,
                "data_requirements": {
                    "safety": 0.7,
                    "efficacy": 0.7,
                    "environmental": 0.7
                },
                "regulatory_agencies": ["ctnbio"]
            },
            "india": {
                "name": "India",
                "approval_time_mean": approval_time_mean * 1.3,
                "approval_time_std": approval_time_std * 1.2,
                "approval_probability": 0.65,
                "data_requirements": {
                    "safety": 0.8,
                    "efficacy": 0.7,
                    "environmental": 0.7
                },
                "regulatory_agencies": ["geac"]
            }
        }
        
        return regions
        
    def _initialize_regional_frameworks(self) -> Dict[str, Dict[str, Any]]:
        """Initialize regional regulatory frameworks with policies and stringency levels.
        
        Returns:
            Dictionary of regional regulatory frameworks
        """
        frameworks = {
            "north_america": {
                "name": "North America",
                "regions": ["usa", "canada"],
                "stringency": 0.6,
                "policies": {
                    "gene_editing": {
                        "stringency": 0.5,
                        "approval_time_modifier": 0.9
                    },
                    "transgenics": {
                        "stringency": 0.7,
                        "approval_time_modifier": 1.2
                    }
                }
            },
            "europe": {
                "name": "Europe",
                "regions": ["eu"],
                "stringency": 0.8,
                "policies": {
                    "gene_editing": {
                        "stringency": 0.8,
                        "approval_time_modifier": 1.5
                    },
                    "transgenics": {
                        "stringency": 0.9,
                        "approval_time_modifier": 2.0
                    }
                }
            },
            "asia": {
                "name": "Asia",
                "regions": ["china", "india", "japan"],
                "stringency": 0.7,
                "policies": {
                    "gene_editing": {
                        "stringency": 0.6,
                        "approval_time_modifier": 1.1
                    },
                    "transgenics": {
                        "stringency": 0.8,
                        "approval_time_modifier": 1.4
                    }
                }
            }
        }
        
        return frameworks
        
    def process_year(self, current_year: int, agents: Dict[str, Any], technology_pipeline: Any) -> Dict[str, Any]:
        """Process regulatory activities for a year.

        Args:
            current_year: Current simulation year
            agents: Dictionary of agent instances by ID
            technology_pipeline: Technology pipeline instance

        Returns:
            Dictionary containing regulatory metrics for the year
        """
        # Process regulatory applications
        application_results = self.approval_process.process_applications(current_year)

        # Update regulatory metrics
        metrics = {
            "applications_submitted": len(application_results["applications_submitted"]),
            "applications_under_review": len(application_results["applications_under_review"]),
            "applications_approved": len(application_results["applications_approved"]),
            "applications_rejected": len(application_results["applications_rejected"])
        }

        return metrics

    def _initialize_regulations(self) -> Dict[str, Dict[str, Any]]:
        """Initialize regulations for different technology types.
        
        Returns:
            Dictionary of regulations by technology type
        """
        regulations = {
            "gene_editing": {
                "name": "Gene Editing Technologies",
                "description": "Regulations for CRISPR, TALENs, and other gene editing technologies",
                "stringency": 0.6,
                "data_requirements": {
                    "safety": 0.7,
                    "efficacy": 0.6,
                    "environmental": 0.7
                },
                "regional_variations": {
                    "north_america": -0.1,  # Less stringent
                    "europe": 0.2,         # More stringent
                    "asia": 0.0            # Average
                }
            },
            "transgenics": {
                "name": "Transgenic Technologies",
                "description": "Regulations for transgenic plant technologies",
                "stringency": 0.8,
                "data_requirements": {
                    "safety": 0.8,
                    "efficacy": 0.7,
                    "environmental": 0.9
                },
                "regional_variations": {
                    "north_america": -0.05,  # Slightly less stringent
                    "europe": 0.15,         # More stringent
                    "asia": 0.05           # Slightly more stringent
                }
            },
            "breeding": {
                "name": "Traditional Breeding",
                "description": "Regulations for traditional and marker-assisted breeding",
                "stringency": 0.3,
                "data_requirements": {
                    "safety": 0.4,
                    "efficacy": 0.5,
                    "environmental": 0.3
                },
                "regional_variations": {
                    "north_america": -0.05,  # Slightly less stringent
                    "europe": 0.1,          # More stringent
                    "asia": -0.05           # Slightly less stringent
                }
            }
        }
        
        return regulations
    
    def register_application(self, application: Dict[str, Any]) -> Dict[str, Any]:
        """Register a new regulatory application.
        
        Args:
            application: Dictionary containing application attributes
        
        Returns:
            Dictionary with success status and application ID
        """
        application_id = application.get('id')
        if not application_id:
            application_id = f"app_{str(uuid.uuid4())[:8]}"
            application['id'] = application_id
        
        self.applications[application_id] = application
        self.logger.info(f"Registered application: {application.get('product_name', 'Unknown')} (ID: {application_id})")
        
        return {
            "success": True,
            "application_id": application_id,
            "message": f"Application {application_id} registered successfully"
        }
    
    def get_application(self, application_id: str) -> Optional[Dict[str, Any]]:
        """Get an application by ID.
        
        Args:
            application_id: ID of the application to retrieve
        
        Returns:
            Application dictionary or None if not found
        """
        return self.applications.get(application_id)
    
    def get_approval(self, approval_id: str) -> Optional[Dict[str, Any]]:
        """Get an approval by ID.
        
        Args:
            approval_id: ID of the approval to retrieve
        
        Returns:
            Approval dictionary or None if not found
        """
        return self.approvals.get(approval_id)
    
    def get_approvals(self, region: Optional[str] = None, product_type: Optional[str] = None) -> List[Dict[str, Any]]:
        """Get approved products, optionally filtered by region or product type.
        
        Args:
            region: Optional region filter
            product_type: Optional product type filter
        
        Returns:
            List of approval dictionaries
        """
        approvals = list(self.approvals.values())
        
        if region:
            approvals = [a for a in approvals if a["region"] == region]
        
        if product_type:
            # Get applications for the approvals to check product type
            approvals = [
                a for a in approvals 
                if self.applications.get(a["application_id"], {}).get("product_type") == product_type
            ]
        
        return approvals
        
    def update_regulations(self, events: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Update regulations based on events and policy changes.
        
        Args:
            events: List of regulatory events and policy changes
            
        Returns:
            Dictionary with success status and update information
        """
        updates = []
        
        for event in events:
            event_type = event.get("type")
            region = event.get("region")
            
            if event_type == "policy_change" and region in self.regional_frameworks:
                framework = self.regional_frameworks[region]
                policy_area = event.get("policy_area")
                direction = event.get("direction")
                magnitude = event.get("magnitude", 0.1)
                
                # Update regional stringency
                if direction == "more_stringent":
                    framework["stringency"] = min(1.0, framework["stringency"] + magnitude)
                elif direction == "more_permissive":
                    framework["stringency"] = max(0.0, framework["stringency"] - magnitude)
                
                # Update policy-specific stringency if applicable
                if policy_area in framework["policies"]:
                    policy = framework["policies"][policy_area]
                    if direction == "more_stringent":
                        policy["stringency"] = min(1.0, policy["stringency"] + magnitude)
                        policy["approval_time_modifier"] = min(3.0, policy["approval_time_modifier"] + magnitude/2)
                    elif direction == "more_permissive":
                        policy["stringency"] = max(0.0, policy["stringency"] - magnitude)
                        policy["approval_time_modifier"] = max(0.5, policy["approval_time_modifier"] - magnitude/2)
                
                updates.append({
                    "region": region,
                    "policy_area": policy_area,
                    "direction": direction,
                    "magnitude": magnitude,
                    "new_stringency": framework["stringency"]
                })
        
        return {
            "success": True,
            "regulations_updated": len(updates),
            "updates": updates
        }
        
    def process_applications(self, current_year: int, agents: Dict[str, Any]) -> Dict[str, Any]:
        """Process regulatory applications for the current year.
        
        Args:
            current_year: Current simulation year
            agents: Dictionary of agents in the simulation
            
        Returns:
            Dictionary with processing results
        """
        # Initialize results
        results = {
            "applications_processed": 0,
            "applications_approved": [],
            "applications_rejected": [],
            "applications_pending": [],
            "approvals": [],
            "rejections": []
        }
        
        # Process each application
        for app_id, application in self.applications.items():
            if application["status"] == "pending":
                # Update application status based on technology, traits, and regional frameworks
                technology = application.get("technology")
                traits = application.get("traits", [])
                target_regions = application.get("target_regions", [])
                data_package = application.get("data_package", {})
                
                # Calculate approval probability for each target region
                regional_results = {}
                any_approved = False
                all_rejected = True
                
                for region in target_regions:
                    if region in self.regional_frameworks:
                        framework = self.regional_frameworks[region]
                        
                        # Base approval probability
                        base_prob = 0.7  # Default
                        
                        # Adjust based on technology regulations
                        if technology in self.regulations:
                            tech_reg = self.regulations[technology]
                            stringency = tech_reg["stringency"]
                            
                            # Apply regional variation
                            if region in tech_reg["regional_variations"]:
                                stringency += tech_reg["regional_variations"][region]
                            
                            # Higher stringency = lower approval probability
                            base_prob *= (1 - stringency * 0.5)
                        
                        # Adjust based on data package quality
                        data_factor = 1.0
                        if technology in self.regulations:
                            for data_type, requirement in self.regulations[technology]["data_requirements"].items():
                                if data_type in data_package:
                                    quality = data_package[data_type]
                                    factor = quality / requirement
                                    data_factor *= factor
                        
                        # Calculate final probability
                        final_prob = min(0.95, max(0.05, base_prob * data_factor))
                        
                        # Make approval decision
                        approved = random.random() < final_prob
                        
                        regional_results[region] = {
                            "approved": approved,
                            "probability": final_prob,
                            "data_factor": data_factor
                        }
                        
                        if approved:
                            any_approved = True
                            all_rejected = False
                        else:
                            all_rejected = all_rejected and True
                
                # Update application status
                if any_approved:
                    application["status"] = "approved"
                    application["approval_year"] = current_year
                    application["regional_results"] = regional_results
                    
                    # Create approval record
                    approval_id = f"appr_{str(uuid.uuid4())[:8]}"
                    approval = {
                        "id": approval_id,
                        "application_id": app_id,
                        "product_id": application["product_id"],
                        "company_id": application["company_id"],
                        "technology": technology,
                        "traits": traits,
                        "approval_year": current_year,
                        "regional_results": regional_results
                    }
                    
                    self.approvals[approval_id] = approval
                    self.approval_history.append(approval)
                    results["applications_approved"].append(app_id)
                    results["approvals"].append(approval)
                    
                elif all_rejected:
                    application["status"] = "rejected"
                    application["rejection_year"] = current_year
                    application["regional_results"] = regional_results
                    results["applications_rejected"].append(app_id)
                    results["rejections"].append({
                        "application_id": app_id,
                        "product_id": application["product_id"],
                        "company_id": application["company_id"],
                        "technology": technology,
                        "traits": traits,
                        "rejection_year": current_year,
                        "regional_results": regional_results
                    })
                    
                else:
                    # Some regions still pending
                    application["regional_results"] = regional_results
                    results["applications_pending"].append(app_id)
                
                results["applications_processed"] += 1
        
        return results