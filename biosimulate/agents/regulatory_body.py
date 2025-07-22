"""Regulatory Body Agent Module.

This module defines the RegulatoryBody class, which represents regulatory agencies
in the plant biotechnology industry ecosystem simulation.
"""

from dataclasses import dataclass, field
from typing import Dict, List, Any, Optional
import random
import logging

from biosimulate.agents.base_agent import BaseAgent
from biosimulate.utils.data_generator import generate_triangular, generate_normal


@dataclass
class RegulatoryBody(BaseAgent):
    """Represents a regulatory agency in the plant biotechnology industry.
    
    This class models regulatory bodies that oversee approval processes, set standards,
    and enforce regulations in the plant biotechnology industry.
    
    Attributes:
        jurisdiction: Geographic jurisdiction of the regulatory body
        regulatory_framework: The regulatory framework applied by this body
        approval_processes: Dictionary of approval processes and their parameters
        standards: List of standards enforced by this regulatory body
        enforcement_capacity: Capacity to enforce regulations (0-100)
        transparency: Level of transparency in decision-making (0-100)
        risk_tolerance: Tolerance for risk in approvals (0-100, higher = more tolerant)
        political_influence: Level of political influence on decisions (0-100)
        pending_applications: List of applications pending review
        approved_applications: List of approved applications
        rejected_applications: List of rejected applications
        annual_reviews: List of annual reviews conducted
    """
    
    # Regulatory body specific attributes
    jurisdiction: str = field(default="Global")
    regulatory_framework: Dict[str, Any] = field(default_factory=dict)
    approval_processes: Dict[str, Dict[str, Any]] = field(default_factory=dict)
    standards: Optional[List[Dict[str, Any]]] = field(default=None)
    enforcement_capacity: float = field(default=50.0)
    transparency: float = field(default=50.0)
    risk_tolerance: float = field(default=50.0)
    political_influence: float = field(default=50.0)
    pending_applications: List[Dict[str, Any]] = field(default_factory=list)
    approved_applications: List[Dict[str, Any]] = field(default_factory=list)
    rejected_applications: List[Dict[str, Any]] = field(default_factory=list)
    annual_reviews: List[Dict[str, Any]] = field(default_factory=list)
    
    def __post_init__(self):
        """Initialize the regulatory body with default values based on type."""
        super().__post_init__()
        
        # Set agent type
        self.type = "regulatory_body"
        
        # Initialize regulatory framework based on jurisdiction
        self._initialize_regulatory_framework()
        
        # Initialize approval processes
        self._initialize_approval_processes()
        
        # Initialize standards
        self.standards = []
        self._initialize_standards()
    
    def _initialize_regulatory_framework(self):
        """Initialize the regulatory framework based on jurisdiction."""
        # Default framework structure
        self.regulatory_framework = {
            "name": f"{self.jurisdiction} Plant Biotechnology Regulatory Framework",
            "established_year": random.randint(1980, 2010),
            "last_updated_year": random.randint(2010, 2022),
            "key_principles": [
                "Science-based assessment",
                "Precautionary principle",
                "Transparency",
                "Case-by-case evaluation"
            ],
            "regulated_areas": [
                "Genetically modified organisms",
                "Novel breeding techniques",
                "Biopesticides",
                "Biofertilizers",
                "Plant growth regulators"
            ],
            "risk_assessment_methodology": {
                "environmental_risk": True,
                "food_safety": True,
                "socioeconomic_impact": self.jurisdiction in ["EU", "Africa", "Asia"],
                "coexistence": self.jurisdiction in ["EU", "Africa", "Asia"]
            },
            "labeling_requirements": self.jurisdiction != "USA",
            "post_market_monitoring": self.jurisdiction in ["EU", "Japan", "Australia"],
            "international_alignment": {
                "codex_alimentarius": True,
                "cartagena_protocol": self.jurisdiction != "USA",
                "oecd_guidelines": self.jurisdiction in ["USA", "EU", "Japan", "Australia", "Canada"]
            }
        }
        
        # Adjust framework based on jurisdiction
        if self.jurisdiction == "USA":
            self.regulatory_framework["approach"] = "product-based"
            self.regulatory_framework["key_agencies"] = ["FDA", "EPA", "USDA"]
            self.risk_tolerance = 70.0
            self.political_influence = 60.0
        elif self.jurisdiction == "EU":
            self.regulatory_framework["approach"] = "process-based"
            self.regulatory_framework["key_agencies"] = ["EFSA", "European Commission"]
            self.risk_tolerance = 30.0
            self.political_influence = 70.0
        elif self.jurisdiction == "Japan":
            self.regulatory_framework["approach"] = "hybrid"
            self.regulatory_framework["key_agencies"] = ["MHLW", "MAFF"]
            self.risk_tolerance = 40.0
            self.political_influence = 50.0
        elif self.jurisdiction == "Brazil":
            self.regulatory_framework["approach"] = "hybrid"
            self.regulatory_framework["key_agencies"] = ["CTNBio", "ANVISA"]
            self.risk_tolerance = 60.0
            self.political_influence = 65.0
        elif self.jurisdiction == "China":
            self.regulatory_framework["approach"] = "process-based"
            self.regulatory_framework["key_agencies"] = ["MOA", "MEE"]
            self.risk_tolerance = 45.0
            self.political_influence = 90.0
        elif self.jurisdiction == "India":
            self.regulatory_framework["approach"] = "process-based"
            self.regulatory_framework["key_agencies"] = ["GEAC", "RCGM"]
            self.risk_tolerance = 50.0
            self.political_influence = 75.0
        elif self.jurisdiction == "Africa":
            self.regulatory_framework["approach"] = "regional-variation"
            self.regulatory_framework["key_agencies"] = ["ABNE", "National Biosafety Authorities"]
            self.risk_tolerance = 45.0
            self.political_influence = 80.0
        else:  # Global or other
            self.regulatory_framework["approach"] = "international-guidelines"
            self.regulatory_framework["key_agencies"] = ["FAO", "WHO", "OECD"]
            self.risk_tolerance = 50.0
            self.political_influence = 60.0
    
    def _initialize_approval_processes(self):
        """Initialize the approval processes for different product types."""
        # Common approval process structure
        base_process = {
            "stages": [
                "Application submission",
                "Completeness check",
                "Risk assessment",
                "Public consultation",
                "Decision making",
                "Post-approval monitoring"
            ],
            "required_documents": [
                "Technical dossier",
                "Risk assessment report",
                "Environmental impact assessment",
                "Socioeconomic impact assessment"
            ],
            "average_processing_time": 12,  # months
            "success_rate": 0.7,  # 70%
            "transparency_level": self.transparency / 100.0,
            "cost": 100000,  # base cost in currency units
            "appeals_process": True
        }
        
        # Initialize different approval processes
        self.approval_processes = {
            "gmo_crop": base_process.copy(),
            "biopesticide": base_process.copy(),
            "biofertilizer": base_process.copy(),
            "novel_breeding_technique": base_process.copy(),
            "plant_growth_regulator": base_process.copy()
        }
        
        # Customize processes based on product type and jurisdiction
        self.approval_processes["gmo_crop"].update({
            "average_processing_time": 24 if self.jurisdiction == "EU" else 18 if self.jurisdiction == "China" else 12,
            "success_rate": 0.5 if self.jurisdiction == "EU" else 0.6 if self.jurisdiction == "Japan" else 0.75,
            "cost": 250000,
            "public_consultation": self.jurisdiction in ["EU", "Japan", "Brazil", "India", "Africa"]
        })
        
        self.approval_processes["biopesticide"].update({
            "average_processing_time": 12,
            "success_rate": 0.8,
            "cost": 150000,
            "public_consultation": self.jurisdiction in ["EU", "Japan"]
        })
        
        self.approval_processes["biofertilizer"].update({
            "average_processing_time": 8,
            "success_rate": 0.85,
            "cost": 100000,
            "public_consultation": False
        })
        
        self.approval_processes["novel_breeding_technique"].update({
            "average_processing_time": 18 if self.jurisdiction == "EU" else 12 if self.jurisdiction == "Japan" else 6,
            "success_rate": 0.6 if self.jurisdiction == "EU" else 0.7 if self.jurisdiction == "Japan" else 0.9,
            "cost": 200000,
            "public_consultation": self.jurisdiction in ["EU", "Japan", "Brazil"]
        })
        
        self.approval_processes["plant_growth_regulator"].update({
            "average_processing_time": 10,
            "success_rate": 0.75,
            "cost": 120000,
            "public_consultation": self.jurisdiction in ["EU", "Japan"]
        })
    
    def _initialize_standards(self):
        """Initialize the standards enforced by this regulatory body."""
        # Common standards across jurisdictions
        common_standards = [
            {
                "name": "Environmental safety assessment",
                "description": "Standards for assessing environmental impacts of biotech products",
                "stringency": generate_triangular(40, 60, 80),
                "compliance_cost": generate_triangular(50000, 100000, 200000),
                "year_established": random.randint(1990, 2010)
            },
            {
                "name": "Food and feed safety assessment",
                "description": "Standards for assessing safety of biotech products for consumption",
                "stringency": generate_triangular(50, 70, 90),
                "compliance_cost": generate_triangular(75000, 150000, 250000),
                "year_established": random.randint(1990, 2010)
            },
            {
                "name": "Containment and field trial protocols",
                "description": "Standards for conducting confined field trials",
                "stringency": generate_triangular(60, 75, 90),
                "compliance_cost": generate_triangular(30000, 60000, 100000),
                "year_established": random.randint(1990, 2005)
            }
        ]
        
        # Add common standards
        self.standards.extend(common_standards)
        
        # Add jurisdiction-specific standards
        if self.jurisdiction == "EU":
            eu_standards = [
                {
                    "name": "Coexistence measures",
                    "description": "Standards for ensuring coexistence of GM and non-GM agriculture",
                    "stringency": generate_triangular(70, 85, 95),
                    "compliance_cost": generate_triangular(100000, 200000, 300000),
                    "year_established": random.randint(2000, 2015)
                },
                {
                    "name": "Socioeconomic impact assessment",
                    "description": "Standards for assessing socioeconomic impacts of biotech products",
                    "stringency": generate_triangular(60, 75, 90),
                    "compliance_cost": generate_triangular(50000, 100000, 150000),
                    "year_established": random.randint(2005, 2018)
                }
            ]
            self.standards.extend(eu_standards)
        
        elif self.jurisdiction == "USA":
            usa_standards = [
                {
                    "name": "Plant pest risk assessment",
                    "description": "Standards for assessing plant pest risks of biotech products",
                    "stringency": generate_triangular(50, 65, 80),
                    "compliance_cost": generate_triangular(40000, 80000, 120000),
                    "year_established": random.randint(1990, 2005)
                },
                {
                    "name": "Herbicide resistance management",
                    "description": "Standards for managing herbicide resistance in biotech crops",
                    "stringency": generate_triangular(40, 60, 75),
                    "compliance_cost": generate_triangular(30000, 60000, 90000),
                    "year_established": random.randint(2000, 2015)
                }
            ]
            self.standards.extend(usa_standards)
        
        elif self.jurisdiction in ["China", "India", "Brazil"]:
            developing_standards = [
                {
                    "name": "Technology sovereignty measures",
                    "description": "Standards for ensuring national control over biotech innovations",
                    "stringency": generate_triangular(60, 80, 95),
                    "compliance_cost": generate_triangular(50000, 100000, 200000),
                    "year_established": random.randint(2005, 2018)
                },
                {
                    "name": "Smallholder impact assessment",
                    "description": "Standards for assessing impacts on smallholder farmers",
                    "stringency": generate_triangular(50, 70, 85),
                    "compliance_cost": generate_triangular(40000, 80000, 120000),
                    "year_established": random.randint(2005, 2018)
                }
            ]
            self.standards.extend(developing_standards)
    
    def step(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Execute one step of the regulatory body's decision cycle.
        
        Args:
            context: Contextual information for the current simulation step
            
        Returns:
            Dict containing the actions taken by the regulatory body
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
            Dict containing the decisions made by the regulatory body
        """
        decisions = {}
        
        # Process pending applications
        decisions["application_decisions"] = self._decide_on_applications(context)
        
        # Update regulatory framework if needed
        decisions["framework_updates"] = self._decide_on_framework_updates(context)
        
        # Conduct annual reviews if appropriate
        decisions["annual_reviews"] = self._decide_on_annual_reviews(context)
        
        # Decide on enforcement actions
        decisions["enforcement_actions"] = self._decide_on_enforcement(context)
        
        # Decide on international cooperation
        decisions["international_cooperation"] = self._decide_on_international_cooperation(context)
        
        return decisions
    
    def _decide_on_applications(self, context: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Decide on pending applications.
        
        Args:
            context: Contextual information for the current simulation step
            
        Returns:
            List of application decisions
        """
        decisions = []
        
        # Process applications that have completed their review period
        current_year = context.get("year", 0)
        
        for application in self.pending_applications.copy():
            # Check if application has been in review long enough
            submission_year = application.get("submission_year", current_year)
            submission_month = application.get("submission_month", 1)
            
            # Calculate months in review
            months_in_review = (current_year - submission_year) * 12 + (context.get("month", 1) - submission_month)
            
            # Get the relevant approval process
            product_type = application.get("product_type", "gmo_crop")
            approval_process = self.approval_processes.get(product_type, {})
            
            # Get the average processing time for this type of application
            avg_processing_time = approval_process.get("average_processing_time", 12)
            
            # Adjust processing time based on application complexity and regulatory body efficiency
            complexity_factor = application.get("complexity", 1.0)
            efficiency_factor = self.enforcement_capacity / 50.0  # 1.0 at capacity 50
            
            adjusted_processing_time = avg_processing_time * complexity_factor / efficiency_factor
            
            # If application has been in review long enough, make a decision
            if months_in_review >= adjusted_processing_time:
                # Determine if application is approved
                base_success_rate = approval_process.get("success_rate", 0.7)
                
                # Adjust success rate based on application quality and regulatory body risk tolerance
                quality_factor = application.get("quality", 0.5)  # 0.0-1.0
                risk_factor = self.risk_tolerance / 50.0  # 1.0 at tolerance 50
                
                # Political influence can affect decisions
                political_factor = 1.0
                if application.get("political_support", False):
                    political_factor += (self.political_influence / 100.0) * 0.5  # Up to 50% boost
                elif application.get("political_opposition", False):
                    political_factor -= (self.political_influence / 100.0) * 0.5  # Up to 50% reduction
                
                adjusted_success_rate = base_success_rate * quality_factor * risk_factor * political_factor
                
                # Cap success rate between 0.05 and 0.95
                adjusted_success_rate = max(0.05, min(0.95, adjusted_success_rate))
                
                # Make decision
                if random.random() < adjusted_success_rate:
                    decision = "approved"
                else:
                    decision = "rejected"
                
                # Create decision record
                decision_record = {
                    "application_id": application.get("id", ""),
                    "applicant_id": application.get("applicant_id", ""),
                    "product_type": product_type,
                    "product_name": application.get("product_name", ""),
                    "decision": decision,
                    "decision_year": current_year,
                    "decision_month": context.get("month", 1),
                    "months_in_review": months_in_review,
                    "conditions": [],
                    "rationale": self._generate_decision_rationale(application, decision)
                }
                
                # Add conditions if approved
                if decision == "approved":
                    decision_record["conditions"] = self._generate_approval_conditions(application)
                    
                    # Move to approved applications
                    application["status"] = "approved"
                    application["approval_year"] = current_year
                    application["approval_month"] = context.get("month", 1)
                    application["conditions"] = decision_record["conditions"]
                    self.approved_applications.append(application)
                else:
                    # Move to rejected applications
                    application["status"] = "rejected"
                    application["rejection_year"] = current_year
                    application["rejection_month"] = context.get("month", 1)
                    application["rationale"] = decision_record["rationale"]
                    self.rejected_applications.append(application)
                
                # Remove from pending applications
                self.pending_applications.remove(application)
                
                # Add to decisions
                decisions.append(decision_record)
        
        return decisions
    
    def _generate_decision_rationale(self, application: Dict[str, Any], decision: str) -> str:
        """Generate a rationale for the decision on an application.
        
        Args:
            application: The application being decided on
            decision: The decision (approved or rejected)
            
        Returns:
            String containing the rationale for the decision
        """
        if decision == "approved":
            rationales = [
                "The application meets all safety and regulatory requirements.",
                "Scientific evidence supports the safety of this product.",
                "Risk assessment indicates acceptable levels of risk.",
                "Benefits outweigh potential risks based on current evidence.",
                "The product complies with all relevant standards and guidelines."
            ]
        else:  # rejected
            rationales = [
                "The application does not meet all safety requirements.",
                "Insufficient data provided to complete risk assessment.",
                "Unacceptable level of environmental risk identified.",
                "Potential adverse effects on non-target organisms.",
                "Inadequate containment measures proposed.",
                "Socioeconomic impact assessment indicates potential negative effects."
            ]
        
        return random.choice(rationales)
    
    def _generate_approval_conditions(self, application: Dict[str, Any]) -> List[str]:
        """Generate conditions for an approved application.
        
        Args:
            application: The approved application
            
        Returns:
            List of conditions for approval
        """
        product_type = application.get("product_type", "gmo_crop")
        
        common_conditions = [
            "Post-market monitoring for 5 years",
            "Annual reporting of any adverse effects",
            "Compliance with all relevant labeling requirements"
        ]
        
        specific_conditions = {
            "gmo_crop": [
                "Implementation of insect resistance management plan",
                "Maintenance of non-GM refuge areas",
                "Monitoring for gene flow to wild relatives",
                "Adherence to specified isolation distances"
            ],
            "biopesticide": [
                "Monitoring for effects on non-target organisms",
                "Adherence to application rate restrictions",
                "Worker safety protocols during application"
            ],
            "biofertilizer": [
                "Monitoring for soil microbial community effects",
                "Quality control measures during production"
            ],
            "novel_breeding_technique": [
                "Molecular characterization of final product",
                "Monitoring for off-target effects"
            ],
            "plant_growth_regulator": [
                "Residue monitoring in harvested products",
                "Environmental fate studies"
            ]
        }
        
        # Select 1-3 common conditions
        selected_conditions = random.sample(common_conditions, random.randint(1, min(3, len(common_conditions))))
        
        # Add 1-2 product-specific conditions if available
        if product_type in specific_conditions and specific_conditions[product_type]:
            product_conditions = random.sample(
                specific_conditions[product_type], 
                random.randint(1, min(2, len(specific_conditions[product_type])))
            )
            selected_conditions.extend(product_conditions)
        
        return selected_conditions
    
    def _decide_on_framework_updates(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Decide on updates to the regulatory framework.
        
        Args:
            context: Contextual information for the current simulation step
            
        Returns:
            Dict containing framework update decisions
        """
        updates = {"updated": False, "changes": []}
        
        # Check if framework needs updating (typically every 5-10 years)
        current_year = context.get("year", 0)
        last_updated = self.regulatory_framework.get("last_updated_year", current_year - 10)
        
        # Consider external factors that might trigger updates
        external_triggers = {
            "new_scientific_evidence": context.get("new_scientific_evidence", False),
            "international_agreement": context.get("new_international_agreement", False),
            "public_pressure": context.get("public_pressure_on_regulations", False),
            "industry_pressure": context.get("industry_pressure_on_regulations", False),
            "political_change": context.get("political_change", False),
            "technological_breakthrough": context.get("technological_breakthrough", False)
        }
        
        # Calculate probability of update
        years_since_update = current_year - last_updated
        base_probability = min(0.8, years_since_update / 10.0)  # Up to 80% after 10 years
        
        # Adjust based on external triggers
        trigger_factor = 1.0
        for trigger, present in external_triggers.items():
            if present:
                trigger_factor += 0.2  # Each trigger increases probability by 20%
        
        update_probability = base_probability * trigger_factor
        
        # Decide whether to update
        if random.random() < update_probability:
            updates["updated"] = True
            self.regulatory_framework["last_updated_year"] = current_year
            
            # Determine what aspects to update
            possible_changes = [
                "Add new regulated area",
                "Modify risk assessment methodology",
                "Update labeling requirements",
                "Revise approval process",
                "Adjust international alignment",
                "Update key principles"
            ]
            
            # Select 1-3 changes
            num_changes = random.randint(1, 3)
            selected_changes = random.sample(possible_changes, min(num_changes, len(possible_changes)))
            
            # Implement changes
            for change in selected_changes:
                if change == "Add new regulated area":
                    new_areas = [
                        "Gene editing technologies",
                        "RNA interference products",
                        "Synthetic biology applications",
                        "Microbiome-based products",
                        "Plant-based pharmaceuticals"
                    ]
                    # Filter out areas already regulated
                    new_areas = [area for area in new_areas if area not in self.regulatory_framework.get("regulated_areas", [])]
                    
                    if new_areas:
                        new_area = random.choice(new_areas)
                        self.regulatory_framework["regulated_areas"].append(new_area)
                        updates["changes"].append({
                            "type": "new_regulated_area",
                            "area": new_area,
                            "description": f"Added {new_area} to regulated areas"
                        })
                
                elif change == "Modify risk assessment methodology":
                    methodology = self.regulatory_framework.get("risk_assessment_methodology", {})
                    
                    # Possible modifications
                    modifications = [
                        {"aspect": "socioeconomic_impact", "value": not methodology.get("socioeconomic_impact", False)},
                        {"aspect": "coexistence", "value": not methodology.get("coexistence", False)},
                        {"aspect": "cumulative_effects", "value": not methodology.get("cumulative_effects", False)},
                        {"aspect": "long_term_monitoring", "value": not methodology.get("long_term_monitoring", False)}
                    ]
                    
                    modification = random.choice(modifications)
                    methodology[modification["aspect"]] = modification["value"]
                    
                    updates["changes"].append({
                        "type": "risk_assessment_change",
                        "aspect": modification["aspect"],
                        "new_value": modification["value"],
                        "description": f"{'Added' if modification['value'] else 'Removed'} {modification['aspect'].replace('_', ' ')} from risk assessment methodology"
                    })
                
                elif change == "Update labeling requirements":
                    current_value = self.regulatory_framework.get("labeling_requirements", False)
                    new_value = not current_value
                    
                    self.regulatory_framework["labeling_requirements"] = new_value
                    
                    updates["changes"].append({
                        "type": "labeling_change",
                        "new_value": new_value,
                        "description": f"{'Implemented' if new_value else 'Removed'} mandatory labeling requirements"
                    })
                
                elif change == "Revise approval process":
                    # Select a process to revise
                    process_types = list(self.approval_processes.keys())
                    process_type = random.choice(process_types)
                    process = self.approval_processes[process_type]
                    
                    # Possible revisions
                    revisions = [
                        {"aspect": "average_processing_time", "change": random.uniform(-0.2, 0.2)},  # -20% to +20%
                        {"aspect": "success_rate", "change": random.uniform(-0.1, 0.1)},  # -10% to +10%
                        {"aspect": "cost", "change": random.uniform(-0.15, 0.25)},  # -15% to +25%
                        {"aspect": "public_consultation", "change": not process.get("public_consultation", False)}
                    ]
                    
                    revision = random.choice(revisions)
                    
                    if revision["aspect"] == "public_consultation":
                        process[revision["aspect"]] = revision["change"]
                        description = f"{'Added' if revision['change'] else 'Removed'} public consultation for {process_type.replace('_', ' ')} approval process"
                    else:
                        old_value = process.get(revision["aspect"], 0)
                        if revision["aspect"] in ["average_processing_time", "cost"]:
                            new_value = old_value * (1 + revision["change"])
                        else:  # success_rate
                            new_value = max(0.1, min(0.95, old_value + revision["change"]))
                        
                        process[revision["aspect"]] = new_value
                        
                        if revision["change"] > 0:
                            direction = "Increased"
                        else:
                            direction = "Decreased"
                        
                        description = f"{direction} {revision['aspect'].replace('_', ' ')} for {process_type.replace('_', ' ')} approval process"
                    
                    updates["changes"].append({
                        "type": "approval_process_change",
                        "process_type": process_type,
                        "aspect": revision["aspect"],
                        "description": description
                    })
                
                elif change == "Adjust international alignment":
                    alignment = self.regulatory_framework.get("international_alignment", {})
                    
                    # Possible adjustments
                    adjustments = [
                        {"agreement": "codex_alimentarius", "value": not alignment.get("codex_alimentarius", False)},
                        {"agreement": "cartagena_protocol", "value": not alignment.get("cartagena_protocol", False)},
                        {"agreement": "oecd_guidelines", "value": not alignment.get("oecd_guidelines", False)},
                        {"agreement": "regional_harmonization", "value": not alignment.get("regional_harmonization", False)}
                    ]
                    
                    adjustment = random.choice(adjustments)
                    alignment[adjustment["agreement"]] = adjustment["value"]
                    
                    updates["changes"].append({
                        "type": "international_alignment_change",
                        "agreement": adjustment["agreement"],
                        "new_value": adjustment["value"],
                        "description": f"{'Aligned with' if adjustment['value'] else 'Moved away from'} {adjustment['agreement'].replace('_', ' ')}"
                    })
                
                elif change == "Update key principles":
                    principles = self.regulatory_framework.get("key_principles", [])
                    
                    # Possible new principles
                    new_principles = [
                        "Innovation-friendly approach",
                        "Sustainability focus",
                        "Food security considerations",
                        "Farmer's rights protection",
                        "Indigenous knowledge integration",
                        "Circular economy principles"
                    ]
                    
                    # Filter out principles already included
                    new_principles = [p for p in new_principles if p not in principles]
                    
                    if new_principles:
                        added_principle = random.choice(new_principles)
                        principles.append(added_principle)
                        
                        updates["changes"].append({
                            "type": "key_principle_addition",
                            "principle": added_principle,
                            "description": f"Added {added_principle} to key regulatory principles"
                        })
        
        return updates
    
    def _decide_on_annual_reviews(self, context: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Decide on annual reviews to conduct.
        
        Args:
            context: Contextual information for the current simulation step
            
        Returns:
            List of annual reviews to conduct
        """
        reviews = []
        
        # Determine if it's time for annual reviews (typically once per year)
        current_year = context.get("year", 0)
        current_month = context.get("month", 1)
        
        # Only conduct reviews in a specific month (e.g., January)
        if current_month != 1:
            return reviews
        
        # Check for previously approved products that need review
        for application in self.approved_applications:
            approval_year = application.get("approval_year", 0)
            years_since_approval = current_year - approval_year
            
            # Determine if this product needs review this year
            needs_review = False
            
            # Products typically reviewed in years 1, 3, 5, and 10 after approval
            if years_since_approval in [1, 3, 5, 10]:
                needs_review = True
            
            # Some products may have specific review schedules in their conditions
            for condition in application.get("conditions", []):
                if "annual review" in condition.lower() or "monitoring" in condition.lower():
                    needs_review = True
                    break
            
            if needs_review:
                # Create review
                review = {
                    "id": f"review_{len(self.annual_reviews) + 1}",
                    "application_id": application.get("id", ""),
                    "product_name": application.get("product_name", ""),
                    "product_type": application.get("product_type", ""),
                    "applicant_id": application.get("applicant_id", ""),
                    "review_year": current_year,
                    "years_since_approval": years_since_approval,
                    "focus_areas": self._determine_review_focus_areas(application, years_since_approval),
                    "status": "pending"
                }
                
                reviews.append(review)
                self.annual_reviews.append(review)
        
        return reviews
    
    def _determine_review_focus_areas(self, application: Dict[str, Any], years_since_approval: int) -> List[str]:
        """Determine focus areas for a product review.
        
        Args:
            application: The approved application being reviewed
            years_since_approval: Years since the application was approved
            
        Returns:
            List of focus areas for the review
        """
        product_type = application.get("product_type", "gmo_crop")
        
        # Common focus areas for all product types
        common_areas = [
            "Compliance with approval conditions",
            "Adverse event reports",
            "Post-market monitoring data"
        ]
        
        # Product-specific focus areas
        specific_areas = {
            "gmo_crop": [
                "Gene flow to wild relatives",
                "Insect resistance development",
                "Weed resistance development",
                "Effects on non-target organisms",
                "Changes in agricultural practices"
            ],
            "biopesticide": [
                "Environmental persistence",
                "Effects on non-target organisms",
                "Resistance development",
                "Worker exposure incidents"
            ],
            "biofertilizer": [
                "Soil microbial community effects",
                "Nutrient leaching",
                "Product efficacy"
            ],
            "novel_breeding_technique": [
                "Genetic stability",
                "Off-target effects",
                "Phenotypic performance"
            ],
            "plant_growth_regulator": [
                "Residue levels",
                "Environmental fate",
                "Non-target effects"
            ]
        }
        
        # Year-specific focus areas
        year_specific_areas = {
            1: ["Initial compliance", "Early adoption issues"],
            3: ["Medium-term effects", "Resistance monitoring"],
            5: ["Long-term environmental effects", "Socioeconomic impacts"],
            10: ["Comprehensive reassessment", "Technology obsolescence evaluation"]
        }
        
        # Select focus areas
        selected_areas = common_areas.copy()
        
        # Add 2-3 product-specific areas if available
        if product_type in specific_areas and specific_areas[product_type]:
            product_areas = random.sample(
                specific_areas[product_type], 
                random.randint(2, min(3, len(specific_areas[product_type])))
            )
            selected_areas.extend(product_areas)
        
        # Add year-specific areas if available
        if years_since_approval in year_specific_areas:
            selected_areas.extend(year_specific_areas[years_since_approval])
        
        return selected_areas
    
    def _decide_on_enforcement(self, context: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Decide on enforcement actions.
        
        Args:
            context: Contextual information for the current simulation step
            
        Returns:
            List of enforcement actions
        """
        actions = []
        
        # Get non-compliance reports from context
        non_compliance_reports = context.get("non_compliance_reports", [])
        
        # Filter reports relevant to this regulatory body's jurisdiction
        relevant_reports = [report for report in non_compliance_reports 
                          if report.get("jurisdiction", "") == self.jurisdiction]
        
        # Process each relevant report
        for report in relevant_reports:
            # Determine if enforcement action is taken
            enforcement_probability = self.enforcement_capacity / 100.0  # 0.0-1.0
            
            # Adjust based on severity of non-compliance
            severity = report.get("severity", 0.5)  # 0.0-1.0
            adjusted_probability = enforcement_probability * (0.5 + severity / 2)  # Severity increases probability
            
            if random.random() < adjusted_probability:
                # Determine type of enforcement action based on severity
                if severity < 0.3:  # Minor
                    action_type = random.choice(["warning", "additional_monitoring"])
                elif severity < 0.7:  # Moderate
                    action_type = random.choice(["fine", "corrective_action", "temporary_suspension"])
                else:  # Severe
                    action_type = random.choice(["major_fine", "approval_revocation", "legal_action"])
                
                # Create enforcement action
                action = {
                    "id": f"enforcement_{len(actions) + 1}",
                    "report_id": report.get("id", ""),
                    "entity_id": report.get("entity_id", ""),
                    "product_id": report.get("product_id", ""),
                    "action_type": action_type,
                    "severity": severity,
                    "year": context.get("year", 0),
                    "month": context.get("month", 1),
                    "description": self._generate_enforcement_description(action_type, report),
                    "penalties": self._generate_enforcement_penalties(action_type, severity)
                }
                
                actions.append(action)
                
                # If action is approval revocation, update approved applications
                if action_type == "approval_revocation" and report.get("product_id", ""):
                    for application in self.approved_applications.copy():
                        if application.get("id", "") == report.get("product_id", ""):
                            application["status"] = "revoked"
                            application["revocation_year"] = context.get("year", 0)
                            application["revocation_month"] = context.get("month", 1)
                            application["revocation_reason"] = report.get("description", "Non-compliance")
                            
                            # Move to rejected applications
                            self.rejected_applications.append(application)
                            self.approved_applications.remove(application)
        
        return actions
    
    def _generate_enforcement_description(self, action_type: str, report: Dict[str, Any]) -> str:
        """Generate a description for an enforcement action.
        
        Args:
            action_type: The type of enforcement action
            report: The non-compliance report
            
        Returns:
            String containing the description of the enforcement action
        """
        descriptions = {
            "warning": [
                "Formal warning issued for minor non-compliance.",
                "Written notice of violation with corrective measures required."
            ],
            "additional_monitoring": [
                "Increased frequency of monitoring and reporting required.",
                "Additional testing and data submission mandated."
            ],
            "fine": [
                "Monetary penalty imposed for regulatory violations.",
                "Financial sanction for non-compliance with approval conditions."
            ],
            "corrective_action": [
                "Mandatory implementation of specific corrective measures.",
                "Required changes to operational procedures to address non-compliance."
            ],
            "temporary_suspension": [
                "Temporary halt of product sales or distribution pending corrective actions.",
                "Suspension of specific activities until compliance is demonstrated."
            ],
            "major_fine": [
                "Substantial financial penalty for serious regulatory violations.",
                "Significant monetary sanction reflecting the severity of non-compliance."
            ],
            "approval_revocation": [
                "Permanent withdrawal of product approval due to serious violations.",
                "Revocation of authorization due to unacceptable risks or persistent non-compliance."
            ],
            "legal_action": [
                "Initiation of legal proceedings for regulatory violations.",
                "Referral to prosecution authorities for potential criminal charges."
            ]
        }
        
        if action_type in descriptions:
            return random.choice(descriptions[action_type])
        else:
            return "Enforcement action taken in response to non-compliance."
    
    def _generate_enforcement_penalties(self, action_type: str, severity: float) -> Dict[str, Any]:
        """Generate penalties for an enforcement action.
        
        Args:
            action_type: The type of enforcement action
            severity: The severity of the non-compliance (0.0-1.0)
            
        Returns:
            Dict containing the penalties for the enforcement action
        """
        penalties = {}
        
        if action_type in ["fine", "major_fine"]:
            # Calculate fine amount based on severity and action type
            base_amount = 50000 if action_type == "fine" else 500000
            severity_factor = 0.5 + severity  # 0.5-1.5
            
            # Add some randomness
            random_factor = generate_triangular(0.8, 1.0, 1.2)  # 0.8-1.2
            
            fine_amount = base_amount * severity_factor * random_factor
            penalties["fine_amount"] = int(fine_amount)
        
        elif action_type == "temporary_suspension":
            # Calculate suspension duration in months
            base_duration = 3  # 3 months
            severity_factor = 0.5 + severity * 2  # 0.5-2.5
            
            duration = int(base_duration * severity_factor)
            penalties["suspension_duration"] = duration
        
        elif action_type == "additional_monitoring":
            # Calculate monitoring duration in years
            base_duration = 1  # 1 year
            severity_factor = 1 + severity * 2  # 1-3
            
            duration = int(base_duration * severity_factor)
            penalties["monitoring_duration"] = duration
            penalties["monitoring_frequency"] = "monthly" if severity > 0.5 else "quarterly"
        
        elif action_type == "corrective_action":
            # Calculate deadline for corrective action in months
            base_deadline = 6  # 6 months
            severity_factor = 0.5 + (1 - severity)  # 0.5-1.5, higher severity = shorter deadline
            
            deadline = int(base_deadline * severity_factor)
            penalties["deadline_months"] = max(1, deadline)  # Minimum 1 month
        
        return penalties
    
    def _decide_on_international_cooperation(self, context: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Decide on international cooperation initiatives.
        
        Args:
            context: Contextual information for the current simulation step
            
        Returns:
            List of international cooperation initiatives
        """
        initiatives = []
        
        # Determine if new cooperation initiatives are started this year
        # Typically happens every 2-3 years
        current_year = context.get("year", 0)
        
        # Check if there are international events that might trigger cooperation
        international_events = context.get("international_events", [])
        relevant_events = [event for event in international_events 
                         if event.get("type", "") in ["regulatory_conference", "trade_agreement", "scientific_consensus"]]
        
        # Base probability of new initiative
        base_probability = 0.3  # 30% chance per year
        
        # Adjust based on relevant events
        adjusted_probability = base_probability + (len(relevant_events) * 0.15)  # Each event adds 15%
        
        if random.random() < adjusted_probability:
            # Determine type of cooperation initiative
            initiative_types = [
                "harmonization_effort",
                "mutual_recognition",
                "joint_risk_assessment",
                "data_sharing_agreement",
                "capacity_building"
            ]
            
            initiative_type = random.choice(initiative_types)
            
            # Determine partner jurisdictions
            all_jurisdictions = ["USA", "EU", "Japan", "Brazil", "China", "India", "Africa", "Australia", "Canada"]
            potential_partners = [j for j in all_jurisdictions if j != self.jurisdiction]
            
            # Select 1-3 partners
            num_partners = random.randint(1, 3)
            partners = random.sample(potential_partners, min(num_partners, len(potential_partners)))
            
            # Create initiative
            initiative = {
                "id": f"cooperation_{len(initiatives) + 1}",
                "type": initiative_type,
                "partners": partners,
                "start_year": current_year,
                "duration": random.randint(2, 5),  # 2-5 years
                "focus_areas": self._determine_cooperation_focus_areas(initiative_type),
                "expected_outcomes": self._determine_cooperation_outcomes(initiative_type),
                "status": "active"
            }
            
            initiatives.append(initiative)
        
        return initiatives
    
    def _determine_cooperation_focus_areas(self, initiative_type: str) -> List[str]:
        """Determine focus areas for a cooperation initiative.
        
        Args:
            initiative_type: The type of cooperation initiative
            
        Returns:
            List of focus areas for the initiative
        """
        focus_areas = {
            "harmonization_effort": [
                "Data requirements",
                "Risk assessment methodologies",
                "Labeling standards",
                "Approval processes",
                "Post-market monitoring"
            ],
            "mutual_recognition": [
                "Safety assessments",
                "Field trial data",
                "Compositional analysis",
                "Environmental risk assessment"
            ],
            "joint_risk_assessment": [
                "Novel breeding techniques",
                "Stacked trait products",
                "RNA interference products",
                "Synthetic biology applications"
            ],
            "data_sharing_agreement": [
                "Safety studies",
                "Post-market monitoring data",
                "Non-compliance incidents",
                "Detection methods"
            ],
            "capacity_building": [
                "Risk assessment training",
                "Laboratory capabilities",
                "Regulatory frameworks",
                "Enforcement mechanisms"
            ]
        }
        
        if initiative_type in focus_areas:
            # Select 2-3 focus areas
            num_areas = random.randint(2, 3)
            return random.sample(focus_areas[initiative_type], min(num_areas, len(focus_areas[initiative_type])))
        else:
            return ["General regulatory cooperation"]
    
    def _determine_cooperation_outcomes(self, initiative_type: str) -> List[str]:
        """Determine expected outcomes for a cooperation initiative.
        
        Args:
            initiative_type: The type of cooperation initiative
            
        Returns:
            List of expected outcomes for the initiative
        """
        outcomes = {
            "harmonization_effort": [
                "Reduced regulatory divergence",
                "Streamlined approval processes",
                "Common data requirements",
                "Aligned risk assessment approaches"
            ],
            "mutual_recognition": [
                "Reduced duplicate testing",
                "Faster approval processes",
                "Lower regulatory costs",
                "Expanded market access"
            ],
            "joint_risk_assessment": [
                "Shared expertise",
                "More robust assessments",
                "Consistent decisions",
                "Reduced resource requirements"
            ],
            "data_sharing_agreement": [
                "Improved monitoring",
                "Early warning of issues",
                "Reduced data gaps",
                "Enhanced transparency"
            ],
            "capacity_building": [
                "Strengthened regulatory systems",
                "Improved technical capabilities",
                "More effective enforcement",
                "Sustainable regulatory frameworks"
            ]
        }
        
        if initiative_type in outcomes:
            # Select 2-3 outcomes
            num_outcomes = random.randint(2, 3)
            return random.sample(outcomes[initiative_type], min(num_outcomes, len(outcomes[initiative_type])))
        else:
            return ["Enhanced international regulatory cooperation"]
    
    def _update_state(self, actions: Dict[str, Any], context: Dict[str, Any]) -> None:
        """Update state based on actions and context.
        
        Args:
            actions: Actions taken by the regulatory body
            context: Contextual information for the current simulation step
        """
        # Process new applications from context
        self._process_new_applications(context)
        
        # Update annual reviews
        self._update_annual_reviews(actions, context)
        
        # Update enforcement capacity based on context
        self._update_enforcement_capacity(context)
        
        # Update risk tolerance based on context
        self._update_risk_tolerance(context)
        
        # Update political influence based on context
        self._update_political_influence(context)
        
        # Update transparency based on context
        self._update_transparency(context)
    
    def _process_new_applications(self, context: Dict[str, Any]) -> None:
        """Process new applications from context.
        
        Args:
            context: Contextual information for the current simulation step
        """
        # Get new applications from context
        new_applications = context.get("new_applications", [])
        
        # Filter applications relevant to this regulatory body's jurisdiction
        relevant_applications = [app for app in new_applications 
                               if app.get("jurisdiction", "") == self.jurisdiction]
        
        # Add to pending applications
        for application in relevant_applications:
            # Add submission details
            application["submission_year"] = context.get("year", 0)
            application["submission_month"] = context.get("month", 1)
            application["status"] = "pending"
            
            # Add to pending applications
            self.pending_applications.append(application)
    
    def _update_annual_reviews(self, actions: Dict[str, Any], context: Dict[str, Any]) -> None:
        """Update annual reviews based on actions and context.
        
        Args:
            actions: Actions taken by the regulatory body
            context: Contextual information for the current simulation step
        """
        # Get reviews that were initiated
        new_reviews = actions.get("annual_reviews", [])
        
        # Update status of ongoing reviews
        current_year = context.get("year", 0)
        current_month = context.get("month", 1)
        
        for review in self.annual_reviews:
            if review.get("status", "") == "pending":
                # Reviews typically take 3-6 months
                review_year = review.get("review_year", current_year)
                months_since_start = (current_year - review_year) * 12 + (current_month - 1)
                
                if months_since_start >= random.randint(3, 6):
                    # Complete review
                    review["status"] = "completed"
                    review["completion_year"] = current_year
                    review["completion_month"] = current_month
                    
                    # Determine findings
                    review["findings"] = self._generate_review_findings(review)
                    
                    # Determine if any actions are needed based on findings
                    review["actions_needed"] = self._determine_review_actions(review)
                    
                    # Apply actions if needed
                    self._apply_review_actions(review)
    
    def _generate_review_findings(self, review: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate findings for a completed review.
        
        Args:
            review: The review to generate findings for
            
        Returns:
            List of findings for the review
        """
        findings = []
        
        # Determine number of findings (1-5)
        num_findings = random.randint(1, 5)
        
        # Generate findings based on focus areas
        focus_areas = review.get("focus_areas", [])
        
        for i in range(min(num_findings, len(focus_areas))):
            focus_area = focus_areas[i]
            
            # Determine if finding is positive, neutral, or negative
            finding_type = random.choices(
                ["positive", "neutral", "negative"],
                weights=[0.4, 0.4, 0.2],  # 40% positive, 40% neutral, 20% negative
                k=1
            )[0]
            
            # Generate finding description
            if finding_type == "positive":
                descriptions = [
                    f"Full compliance with requirements in {focus_area}.",
                    f"No issues identified in {focus_area}.",
                    f"Excellent performance in {focus_area}.",
                    f"Better than expected results in {focus_area}."
                ]
            elif finding_type == "neutral":
                descriptions = [
                    f"Minor issues identified in {focus_area}, but within acceptable limits.",
                    f"Some areas for improvement in {focus_area}, but generally compliant.",
                    f"Acceptable performance in {focus_area} with recommendations for enhancement.",
                    f"Adequate compliance with {focus_area} requirements."
                ]
            else:  # negative
                descriptions = [
                    f"Significant issues identified in {focus_area}.",
                    f"Non-compliance detected in {focus_area}.",
                    f"Unacceptable performance in {focus_area}.",
                    f"Failure to meet requirements in {focus_area}."
                ]
            
            description = random.choice(descriptions)
            
            # Create finding
            finding = {
                "id": f"finding_{i+1}",
                "focus_area": focus_area,
                "type": finding_type,
                "description": description,
                "severity": generate_normal(0.7, 0.1) if finding_type == "positive" else
                           generate_normal(0.5, 0.1) if finding_type == "neutral" else
                           generate_normal(0.3, 0.1)  # Lower is more severe for negative findings
            }
            
            findings.append(finding)
        
        return findings
    
    def _determine_review_actions(self, review: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Determine actions needed based on review findings.
        
        Args:
            review: The completed review
            
        Returns:
            List of actions needed based on the review
        """
        actions_needed = []
        
        # Check for negative findings
        negative_findings = [f for f in review.get("findings", []) if f.get("type", "") == "negative"]
        
        for finding in negative_findings:
            # Determine action based on focus area and severity
            focus_area = finding.get("focus_area", "")
            severity = finding.get("severity", 0.5)  # 0.0-1.0, lower is more severe for negative findings
            
            # Determine action type based on severity
            if severity < 0.2:  # Very severe
                action_types = ["approval_revocation", "major_corrective_action", "immediate_suspension"]
            elif severity < 0.4:  # Severe
                action_types = ["corrective_action", "additional_studies", "temporary_suspension"]
            else:  # Moderate
                action_types = ["additional_monitoring", "minor_corrective_action", "warning"]
            
            action_type = random.choice(action_types)
            
            # Create action
            action = {
                "id": f"action_{len(actions_needed) + 1}",
                "finding_id": finding.get("id", ""),
                "type": action_type,
                "description": self._generate_action_description(action_type, focus_area),
                "deadline": random.randint(1, 12),  # 1-12 months
                "status": "pending"
            }
            
            actions_needed.append(action)
        
        return actions_needed
    
    def _generate_action_description(self, action_type: str, focus_area: str) -> str:
        """Generate a description for a review action.
        
        Args:
            action_type: The type of action
            focus_area: The focus area of the finding
            
        Returns:
            String containing the description of the action
        """
        descriptions = {
            "approval_revocation": [
                f"Revoke approval due to serious non-compliance in {focus_area}.",
                f"Withdraw authorization based on unacceptable risks identified in {focus_area}."
            ],
            "major_corrective_action": [
                f"Implement comprehensive corrective measures to address serious issues in {focus_area}.",
                f"Develop and execute major remediation plan for {focus_area}."
            ],
            "immediate_suspension": [
                f"Immediately suspend product until serious issues in {focus_area} are resolved.",
                f"Halt all activities related to {focus_area} until compliance is demonstrated."
            ],
            "corrective_action": [
                f"Implement specific corrective measures for {focus_area}.",
                f"Develop and execute action plan to address issues in {focus_area}."
            ],
            "additional_studies": [
                f"Conduct additional studies to further assess {focus_area}.",
                f"Perform supplementary research to address knowledge gaps in {focus_area}."
            ],
            "temporary_suspension": [
                f"Temporarily suspend specific activities related to {focus_area}.",
                f"Pause operations in {focus_area} until issues are addressed."
            ],
            "additional_monitoring": [
                f"Implement enhanced monitoring protocols for {focus_area}.",
                f"Increase frequency and scope of monitoring for {focus_area}."
            ],
            "minor_corrective_action": [
                f"Make minor adjustments to improve performance in {focus_area}.",
                f"Implement targeted improvements for {focus_area}."
            ],
            "warning": [
                f"Formal warning regarding issues in {focus_area}.",
                f"Official notice of concerns related to {focus_area}."
            ]
        }
        
        if action_type in descriptions:
            return random.choice(descriptions[action_type])
        else:
            return f"Take appropriate action to address issues in {focus_area}."
    
    def _apply_review_actions(self, review: Dict[str, Any]) -> None:
        """Apply actions based on review findings.
        
        Args:
            review: The completed review
        """
        # Get the application ID from the review
        application_id = review.get("application_id", "")
        
        # Get actions needed
        actions_needed = review.get("actions_needed", [])
        
        # Apply actions
        for action in actions_needed:
            action_type = action.get("type", "")
            
            # If action is approval revocation, update approved applications
            if action_type == "approval_revocation":
                for application in self.approved_applications.copy():
                    if application.get("id", "") == application_id:
                        application["status"] = "revoked"
                        application["revocation_year"] = review.get("completion_year", 0)
                        application["revocation_month"] = review.get("completion_month", 1)
                        application["revocation_reason"] = "Serious issues identified in post-approval review"
                        
                        # Move to rejected applications
                        self.rejected_applications.append(application)
                        self.approved_applications.remove(application)
            
            # Other action types would be implemented here
            # For example, updating monitoring requirements, adding conditions, etc.
    
    def _update_enforcement_capacity(self, context: Dict[str, Any]) -> None:
        """Update enforcement capacity based on context.
        
        Args:
            context: Contextual information for the current simulation step
        """
        # Base annual change (slight increase in capacity over time)
        base_change = generate_normal(1.0, 0.5)  # Mean 1% increase per year
        
        # Adjust based on budget changes
        budget_change = context.get("regulatory_budget_change", 0.0)  # Percentage change
        budget_factor = budget_change / 2.0  # Budget has significant but not 1:1 impact
        
        # Adjust based on political support
        political_support = context.get("regulatory_political_support", 0.0)  # -1.0 to 1.0
        political_factor = political_support * 2.0  # Up to 2% change
        
        # Adjust based on public pressure
        public_pressure = context.get("public_pressure_for_enforcement", 0.0)  # 0.0 to 1.0
        public_factor = public_pressure * 1.5  # Up to 1.5% change
        
        # Calculate total change
        total_change = base_change + budget_factor + political_factor + public_factor
        
        # Apply change (with limits)
        self.enforcement_capacity = max(10.0, min(100.0, self.enforcement_capacity + total_change))
    
    def _update_risk_tolerance(self, context: Dict[str, Any]) -> None:
        """Update risk tolerance based on context.
        
        Args:
            context: Contextual information for the current simulation step
        """
        # Base annual change (slight decrease in risk tolerance over time - precautionary principle)
        base_change = generate_normal(-0.5, 0.3)  # Mean 0.5% decrease per year
        
        # Adjust based on recent incidents
        recent_incidents = context.get("biotech_safety_incidents", 0)  # Number of incidents
        incident_factor = -recent_incidents * 2.0  # Each incident reduces tolerance by up to 2%
        
        # Adjust based on scientific consensus
        scientific_consensus = context.get("scientific_safety_consensus", 0.0)  # -1.0 to 1.0
        science_factor = scientific_consensus * 3.0  # Up to 3% change
        
        # Adjust based on public opinion
        public_opinion = context.get("public_biotech_opinion", 0.0)  # -1.0 to 1.0
        public_factor = public_opinion * 2.0  # Up to 2% change
        
        # Calculate total change
        total_change = base_change + incident_factor + science_factor + public_factor
        
        # Apply change (with limits)
        self.risk_tolerance = max(10.0, min(90.0, self.risk_tolerance + total_change))
    
    def _update_political_influence(self, context: Dict[str, Any]) -> None:
        """Update political influence based on context.
        
        Args:
            context: Contextual information for the current simulation step
        """
        # Base annual change (slight increase in political influence over time)
        base_change = generate_normal(0.3, 0.2)  # Mean 0.3% increase per year
        
        # Adjust based on election cycles
        election_year = context.get("election_year", False)
        election_factor = 5.0 if election_year else 0.0  # Significant increase in election years
        
        # Adjust based on industry lobbying
        industry_lobbying = context.get("industry_lobbying_intensity", 0.0)  # 0.0 to 1.0
        lobbying_factor = industry_lobbying * 3.0  # Up to 3% increase
        
        # Adjust based on public scrutiny
        public_scrutiny = context.get("regulatory_public_scrutiny", 0.0)  # 0.0 to 1.0
        scrutiny_factor = -public_scrutiny * 2.0  # Up to 2% decrease
        
        # Calculate total change
        total_change = base_change + election_factor + lobbying_factor + scrutiny_factor
        
        # Apply change (with limits)
        self.political_influence = max(20.0, min(100.0, self.political_influence + total_change))
    
    def _update_transparency(self, context: Dict[str, Any]) -> None:
        """Update transparency based on context.
        
        Args:
            context: Contextual information for the current simulation step
        """
        # Base annual change (slight increase in transparency over time - modern governance trend)
        base_change = generate_normal(0.5, 0.3)  # Mean 0.5% increase per year
        
        # Adjust based on public pressure
        public_pressure = context.get("transparency_public_pressure", 0.0)  # 0.0 to 1.0
        public_factor = public_pressure * 3.0  # Up to 3% increase
        
        # Adjust based on political will
        political_will = context.get("transparency_political_will", 0.0)  # -1.0 to 1.0
        political_factor = political_will * 2.0  # Up to 2% change
        
        # Adjust based on international standards
        international_standards = context.get("international_transparency_standards", 0.0)  # 0.0 to 1.0
        standards_factor = international_standards * 2.0  # Up to 2% increase
        
        # Calculate total change
        total_change = base_change + public_factor + political_factor + standards_factor
        
        # Apply change (with limits)
        self.transparency = max(20.0, min(100.0, self.transparency + total_change))
    
    def receive_application(self, application: Dict[str, Any], current_year: int, current_month: int) -> None:
        """Receive a new application for review.
        
        Args:
            application: The application to be reviewed
            current_year: The current simulation year
            current_month: The current simulation month
        """
        # Add submission details
        application["submission_year"] = current_year
        application["submission_month"] = current_month
        application["status"] = "pending"
        
        # Add to pending applications
        self.pending_applications.append(application)
    
    def get_approval_process_info(self, product_type: str) -> Dict[str, Any]:
        """Get information about an approval process.
        
        Args:
            product_type: The type of product
            
        Returns:
            Dict containing information about the approval process
        """
        return self.approval_processes.get(product_type, {})
    
    def get_standards_info(self) -> List[Dict[str, Any]]:
        """Get information about regulatory standards.
        
        Returns:
            List of standards enforced by this regulatory body
        """
        return self.standards
    
    def get_application_status(self, application_id: str) -> Dict[str, Any]:
        """Get the status of an application.
        
        Args:
            application_id: The ID of the application
            
        Returns:
            Dict containing the status of the application, or None if not found
        """
        # Check pending applications
        for application in self.pending_applications:
            if application.get("id", "") == application_id:
                return {
                    "id": application_id,
                    "status": "pending",
                    "submission_year": application.get("submission_year", 0),
                    "submission_month": application.get("submission_month", 1),
                    "product_name": application.get("product_name", ""),
                    "product_type": application.get("product_type", "")
                }
        
        # Check approved applications
        for application in self.approved_applications:
            if application.get("id", "") == application_id:
                return {
                    "id": application_id,
                    "status": "approved",
                    "submission_year": application.get("submission_year", 0),
                    "submission_month": application.get("submission_month", 1),
                    "approval_year": application.get("approval_year", 0),
                    "approval_month": application.get("approval_month", 1),
                    "product_name": application.get("product_name", ""),
                    "product_type": application.get("product_type", ""),
                    "conditions": application.get("conditions", [])
                }
        
        # Check rejected applications
        for application in self.rejected_applications:
            if application.get("id", "") == application_id:
                status_info = {
                    "id": application_id,
                    "status": application.get("status", "rejected"),  # Could be "rejected" or "revoked"
                    "submission_year": application.get("submission_year", 0),
                    "submission_month": application.get("submission_month", 1),
                    "product_name": application.get("product_name", ""),
                    "product_type": application.get("product_type", "")
                }
                
                # Add rejection details if rejected
                if application.get("status", "") == "rejected":
                    status_info["rejection_year"] = application.get("rejection_year", 0)
                    status_info["rejection_month"] = application.get("rejection_month", 1)
                    status_info["rationale"] = application.get("rationale", "")
                
                # Add revocation details if revoked
                elif application.get("status", "") == "revoked":
                    status_info["approval_year"] = application.get("approval_year", 0)
                    status_info["approval_month"] = application.get("approval_month", 1)
                    status_info["revocation_year"] = application.get("revocation_year", 0)
                    status_info["revocation_month"] = application.get("revocation_month", 1)
                    status_info["revocation_reason"] = application.get("revocation_reason", "")
                
                return status_info
        
        # Not found
        return None