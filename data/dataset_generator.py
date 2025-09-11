"""
Synthetic Test Data Generator for company profiles
"""

import json
import random
import argparse
from typing import List, Dict, Any
from datetime import datetime, timedelta


class CompanyDataGenerator:
    """Generator for synthetic company profile data"""

    def __init__(self):
        # Company name components
        self.company_prefixes = [
            "Global", "International", "Advanced", "Premier", "Elite", "Modern", 
            "Future", "Quantum", "Digital", "Smart", "Innovative", "Dynamic",
            "Strategic", "Optimal", "Precision", "Alpha", "Beta", "Nexus"
        ]

        self.company_suffixes = [
            "Technologies", "Solutions", "Systems", "Industries", "Corporation",
            "Group", "Enterprises", "Holdings", "Dynamics", "Innovations",
            "Labs", "Works", "Partners", "Associates", "Ventures"
        ]

        # Industries and their typical products
        self.industries_products = {
            "Technology": [
                "Cloud Computing Platforms", "AI/ML Software", "Cybersecurity Solutions",
                "Mobile Applications", "Enterprise Software", "IoT Devices",
                "Blockchain Solutions", "Data Analytics Tools", "VR/AR Systems"
            ],
            "Healthcare": [
                "Medical Devices", "Pharmaceutical Research", "Telemedicine Platforms",
                "Clinical Trial Management", "Health Monitoring Systems", "Diagnostic Equipment",
                "Biotech Research", "Medical Imaging", "Electronic Health Records"
            ],
            "Financial Services": [
                "Trading Platforms", "Payment Processing", "Risk Management Software",
                "Digital Banking", "Insurance Products", "Investment Analytics",
                "Cryptocurrency Services", "Regulatory Compliance Tools", "Fraud Detection"
            ],
            "Defense & Aerospace": [
                "Military Communication Systems", "Satellite Technology", "Drone Systems",
                "Surveillance Equipment", "Aerospace Components", "Defense Software",
                "Navigation Systems", "Radar Technology", "Space Exploration Tools"
            ],
            "Energy": [
                "Smart Grid Technology", "Renewable Energy Systems", "Oil & Gas Equipment",
                "Energy Storage Solutions", "Nuclear Technology", "Carbon Capture Systems",
                "Wind Turbines", "Solar Panels", "Energy Management Software"
            ],
            "Manufacturing": [
                "Industrial Automation", "Quality Control Systems", "Supply Chain Software",
                "Robotics", "3D Printing Technology", "Production Monitoring",
                "Lean Manufacturing Tools", "Predictive Maintenance", "Smart Factory Solutions"
            ],
            "Telecommunications": [
                "5G Infrastructure", "Network Security", "Communication Protocols",
                "Satellite Communications", "Fiber Optic Systems", "Wireless Technology",
                "Voice over IP", "Network Management", "Data Center Solutions"
            ],
            "Transportation": [
                "Autonomous Vehicles", "Traffic Management Systems", "Fleet Management",
                "Logistics Software", "Navigation Systems", "Electric Vehicle Technology",
                "Supply Chain Optimization", "Transportation Analytics", "Smart Infrastructure"
            ],
            "Government": [
                "Citizen Services Platforms", "Emergency Response Systems", "Public Safety Technology",
                "E-Government Solutions", "Identity Management", "Voting Systems",
                "Border Security", "Intelligence Analysis", "Critical Infrastructure Protection"
            ],
            "Education": [
                "Learning Management Systems", "Student Information Systems", "Online Learning Platforms",
                "Educational Analytics", "Virtual Classrooms", "Assessment Tools",
                "Research Management", "Campus Security", "Administrative Software"
            ]
        }

        # Risk categories with descriptions
        self.risk_categories = {
            "Critical Infrastructure": {
                "level": "High",
                "description": "Projects involving critical national infrastructure, power grids, or essential services",
                "sensitive_keywords": ["power grid", "water supply", "transportation hub", "emergency services"]
            },
            "National Security": {
                "level": "Critical",
                "description": "Defense, intelligence, or security-related projects with national implications",
                "sensitive_keywords": ["classified", "military", "intelligence", "national defense"]
            },
            "Personal Data": {
                "level": "Medium",
                "description": "Projects handling large amounts of personal or sensitive customer data",
                "sensitive_keywords": ["personal data", "customer records", "health information", "financial data"]
            },
            "Financial Systems": {
                "level": "High",
                "description": "Core banking, trading, or financial infrastructure systems",
                "sensitive_keywords": ["banking core", "trading system", "payment processing", "financial records"]
            },
            "Healthcare Critical": {
                "level": "High",
                "description": "Life-critical medical systems or research involving sensitive health data",
                "sensitive_keywords": ["life support", "medical devices", "patient data", "clinical trials"]
            },
            "Emerging Technology": {
                "level": "Medium",
                "description": "Cutting-edge technology with potential dual-use applications",
                "sensitive_keywords": ["AI research", "quantum computing", "biotechnology", "advanced materials"]
            },
            "Standard Commercial": {
                "level": "Low",
                "description": "Regular commercial projects with minimal security implications",
                "sensitive_keywords": ["business software", "e-commerce", "marketing tools", "productivity apps"]
            },
            "Research & Development": {
                "level": "Medium",
                "description": "Innovative research projects with potential intellectual property concerns",
                "sensitive_keywords": ["R&D", "patent pending", "proprietary technology", "research data"]
            }
        }

        # Geographic locations
        self.locations = [
            "San Francisco, CA", "New York, NY", "Austin, TX", "Seattle, WA",
            "Boston, MA", "Chicago, IL", "Denver, CO", "Atlanta, GA",
            "Los Angeles, CA", "Washington, DC", "Miami, FL", "Portland, OR"
        ]

        # Company sizes
        self.company_sizes = {
            "Startup": {"employees": (5, 50), "revenue": (100000, 5000000)},
            "Small": {"employees": (51, 200), "revenue": (5000000, 50000000)},
            "Medium": {"employees": (201, 1000), "revenue": (50000000, 500000000)},
            "Large": {"employees": (1001, 10000), "revenue": (500000000, 5000000000)},
            "Enterprise": {"employees": (10001, 100000), "revenue": (5000000000, 50000000000)}
        }

    def generate_company_name(self) -> str:
        """Generate a realistic company name"""
        prefix = random.choice(self.company_prefixes)
        suffix = random.choice(self.company_suffixes)

        # Sometimes include a middle component
        if random.random() < 0.3:
            middle_components = ["Cyber", "Data", "Cloud", "Tech", "Bio", "Nano", "Micro"]
            middle = random.choice(middle_components)
            return f"{prefix} {middle} {suffix}"

        return f"{prefix} {suffix}"

    def generate_company_profile(self) -> Dict[str, Any]:
        """Generate a complete company profile"""
        # Basic company info
        company_name = self.generate_company_name()
        industry = random.choice(list(self.industries_products.keys()))

        # Company size
        size_category = random.choice(list(self.company_sizes.keys()))
        size_info = self.company_sizes[size_category]

        # Products (1-4 products per company)
        available_products = self.industries_products[industry]
        num_products = random.randint(1, min(4, len(available_products)))
        products = random.sample(available_products, num_products)

        # Risk category assignment based on industry and products
        risk_category = self._assign_risk_category(industry, products)

        # Additional details
        founded_year = random.randint(1995, 2023)
        employees = random.randint(*size_info["employees"])
        annual_revenue = random.randint(*size_info["revenue"])

        # Generate additional data for tool integration
        partnerships = self._generate_partnerships(industry)
        sensitive_projects = self._generate_sensitive_projects(risk_category)
        briefing_data = self._generate_briefing_template_data(company_name, industry, products)

        return {
            "id": f"COMP_{random.randint(1000, 9999)}",
            "name": company_name,
            "industry": industry,
            "products": products,
            "risk_category": risk_category["name"],
            "risk_level": risk_category["level"],
            "risk_description": risk_category["description"],
            "sensitive_keywords": risk_category["sensitive_keywords"],
            "location": random.choice(self.locations),
            "founded_year": founded_year,
            "size_category": size_category,
            "employees": employees,
            "annual_revenue_usd": annual_revenue,
            "primary_contact": self._generate_contact_info(),
            "project_history": self._generate_project_history(),
            "compliance_requirements": self._generate_compliance_requirements(industry, risk_category),
            
            # Data for tool integration
            "partnerships": partnerships,
            "sensitive_internal_projects": sensitive_projects,
            "public_information": {
                "website": f"https://www.{company_name.lower().replace(' ', '')}.com",
                "stock_symbol": f"{company_name[:3].upper()}{random.randint(1,99)}",
                "market_cap_usd": annual_revenue * random.uniform(2.0, 8.0),
                "headquarters": random.choice(self.locations),
                "ceo": self._generate_contact_info()["name"]
            },
            "briefing_template_data": briefing_data,
            
            # Translation-ready content
            "multilingual_content": {
                "company_description": f"{company_name} is a leading {industry.lower()} company specializing in {', '.join(products[:2])}.",
                "mission_statement": f"To deliver innovative {industry.lower()} solutions that transform businesses and improve lives.",
                "target_languages": random.sample(["German", "French", "Spanish", "Italian", "Portuguese"], k=2)
            },
            
            "generated_timestamp": datetime.now().isoformat()
        }

    def _assign_risk_category(self, industry: str, products: List[str]) -> Dict[str, Any]:
        """Assign risk category based on industry and products"""
        # High-risk industry mappings
        high_risk_mappings = {
            "Defense & Aerospace": "National Security",
            "Government": "Critical Infrastructure",
            "Financial Services": "Financial Systems",
            "Healthcare": "Healthcare Critical"
        }

        # Check for high-risk industries first
        if industry in high_risk_mappings:
            risk_name = high_risk_mappings[industry]
            risk_info = self.risk_categories[risk_name].copy()
            risk_info["name"] = risk_name
            return risk_info

        # Check products for sensitive keywords
        product_text = " ".join(products).lower()

        for risk_name, risk_info in self.risk_categories.items():
            for keyword in risk_info["sensitive_keywords"]:
                if keyword.lower() in product_text:
                    result = risk_info.copy()
                    result["name"] = risk_name
                    return result

        # Default to appropriate risk level
        if industry in ["Technology", "Energy"]:
            risk_name = "Emerging Technology"
        else:
            risk_name = "Standard Commercial"

        result = self.risk_categories[risk_name].copy()
        result["name"] = risk_name
        return result

    def _generate_contact_info(self) -> Dict[str, str]:
        """Generate contact information"""
        first_names = ["John", "Jane", "Michael", "Sarah", "David", "Lisa", "Robert", "Maria"]
        last_names = ["Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller", "Davis"]

        first_name = random.choice(first_names)
        last_name = random.choice(last_names)

        return {
            "name": f"{first_name} {last_name}",
            "title": random.choice(["CEO", "CTO", "VP Engineering", "Head of Security", "Program Manager"]),
            "email": f"{first_name.lower()}.{last_name.lower()}@{self._generate_domain()}",
            "phone": f"+1-{random.randint(100,999)}-{random.randint(100,999)}-{random.randint(1000,9999)}"
        }

    def _generate_domain(self) -> str:
        """Generate a company domain"""
        tlds = ["com", "io", "tech", "net", "org"]
        company_words = ["tech", "solutions", "systems", "corp", "group", "labs"]

        return f"{random.choice(company_words)}{random.randint(1,99)}.{random.choice(tlds)}"

    def _generate_project_history(self) -> List[Dict[str, Any]]:
        """Generate historical project information"""
        project_types = [
            "Software Development", "System Integration", "Security Audit",
            "Data Migration", "Infrastructure Upgrade", "Compliance Review",
            "Digital Transformation", "Process Automation", "Research Project"
        ]

        statuses = ["Completed", "In Progress", "Cancelled", "On Hold"]

        num_projects = random.randint(1, 5)
        projects = []

        for i in range(num_projects):
            start_date = datetime.now() - timedelta(days=random.randint(30, 1095))
            duration = random.randint(30, 365)

            projects.append({
                "project_name": f"Project {chr(65 + i)}",
                "type": random.choice(project_types),
                "status": random.choice(statuses),
                "start_date": start_date.strftime("%Y-%m-%d"),
                "duration_days": duration,
                "budget_usd": random.randint(50000, 5000000)
            })

        return projects

    def _generate_compliance_requirements(self, industry: str, risk_category: Dict[str, Any]) -> List[str]:
        """Generate relevant compliance requirements"""
        base_requirements = ["ISO 27001", "SOC 2 Type II"]

        industry_requirements = {
            "Healthcare": ["HIPAA", "FDA 21 CFR Part 11"],
            "Financial Services": ["SOX", "PCI DSS", "FFIEC"],
            "Defense & Aerospace": ["NIST 800-171", "ITAR", "FedRAMP"],
            "Government": ["FedRAMP", "FISMA", "NIST Cybersecurity Framework"],
            "Energy": ["NERC CIP", "NIST Cybersecurity Framework"]
        }

        requirements = base_requirements.copy()

        if industry in industry_requirements:
            requirements.extend(industry_requirements[industry])

        if risk_category["level"] in ["High", "Critical"]:
            requirements.extend(["NIST 800-53", "Common Criteria"])

        return list(set(requirements))

    def _generate_partnerships(self, industry: str) -> List[Dict[str, str]]:
        """Generate realistic partnerships for web search simulation"""
        # Industry-specific partnership types
        partnership_types = {
            "Technology": ["Microsoft", "Google", "Amazon", "IBM", "Oracle"],
            "Healthcare": ["Pfizer", "Johnson & Johnson", "Merck", "Mayo Clinic", "Kaiser Permanente"],
            "Financial Services": ["JPMorgan Chase", "Goldman Sachs", "Mastercard", "Visa", "PayPal"],
            "Defense & Aerospace": ["Lockheed Martin", "Boeing", "Raytheon", "Northrop Grumman", "General Dynamics"],
            "Energy": ["ExxonMobil", "Chevron", "BP", "Shell", "Tesla"],
            "Manufacturing": ["General Electric", "Siemens", "3M", "Caterpillar", "Ford"],
            "Telecommunications": ["Verizon", "AT&T", "Cisco", "Ericsson", "Nokia"],
            "Transportation": ["UPS", "FedEx", "Uber", "Lyft", "Tesla"],
            "Government": ["Accenture Federal", "CACI", "SAIC", "Booz Allen Hamilton", "Deloitte"],
            "Education": ["Pearson", "McGraw-Hill", "Blackboard", "Canvas", "Google for Education"]
        }
        
        partnership_descriptions = [
            "Strategic Technology Partnership",
            "Joint Venture Agreement",
            "Research Collaboration",
            "Distribution Partnership",
            "Integration Alliance",
            "Marketing Partnership",
            "Supplier Agreement"
        ]
        
        partners = partnership_types.get(industry, ["Generic Corp", "Business Partners Inc"])
        num_partnerships = random.randint(1, 3)
        
        partnerships = []
        for _ in range(num_partnerships):
            partnerships.append({
                "partner": random.choice(partners),
                "type": random.choice(partnership_descriptions),
                "status": random.choice(["Active", "Pending", "Under Review"]),
                "announcement_date": (datetime.now() - timedelta(days=random.randint(30, 730))).strftime("%Y-%m-%d")
            })
        
        return partnerships

    def _generate_sensitive_projects(self, risk_category: Dict[str, Any]) -> List[str]:
        """Generate internal project names that should be filtered by security tools"""
        project_prefixes = ["Project", "Operation", "Initiative", "Program", "Mission"]
        
        # High-sensitivity project names
        high_sensitivity_names = [
            "Blackbird", "Phoenix", "Atlas", "Titan", "Falcon", "Eagle", "Thunder",
            "Lightning", "Storm", "Hurricane", "Tornado", "Blizzard", "Avalanche"
        ]
        
        # Medium-sensitivity project names
        medium_sensitivity_names = [
            "Alpha", "Beta", "Gamma", "Delta", "Epsilon", "Zeta", "Theta",
            "Nova", "Star", "Comet", "Meteor", "Galaxy", "Nebula", "Orbit"
        ]
        
        # Low-sensitivity project names
        low_sensitivity_names = [
            "Bridge", "Gateway", "Portal", "Connect", "Link", "Flow", "Stream",
            "Wave", "Current", "Channel", "Path", "Route", "Journey", "Quest"
        ]
        
        risk_level = risk_category.get("level", "Low")
        
        if risk_level == "Critical":
            name_pool = high_sensitivity_names
        elif risk_level == "High":
            name_pool = high_sensitivity_names + medium_sensitivity_names
        elif risk_level == "Medium":
            name_pool = medium_sensitivity_names + low_sensitivity_names
        else:
            name_pool = low_sensitivity_names
        
        num_projects = random.randint(1, 3)
        projects = []
        
        for _ in range(num_projects):
            prefix = random.choice(project_prefixes)
            name = random.choice(name_pool)
            projects.append(f"{prefix} {name}")
        
        return projects

    def _generate_briefing_template_data(self, company_name: str, industry: str, products: List[str]) -> Dict[str, Any]:
        """Generate data specifically for briefing document templates"""
        return {
            "executive_summary": f"Brief overview of {company_name}'s position in the {industry} sector",
            "key_strengths": random.sample([
                "Market leadership", "Innovation capability", "Strong partnerships",
                "Financial stability", "Regulatory compliance", "Technical expertise",
                "Global presence", "Customer satisfaction", "Operational efficiency"
            ], k=3),
            "market_position": random.choice([
                "Market Leader", "Strong Competitor", "Emerging Player", "Niche Specialist"
            ]),
            "recent_developments": [
                f"Launched new {random.choice(products)} solution",
                f"Expanded operations in {random.choice(['Asia', 'Europe', 'North America'])}",
                f"Completed acquisition of strategic {industry.lower()} company"
            ],
            "competitive_landscape": [
                f"Primary competitor in {random.choice(products)} space",
                f"Differentiated by {random.choice(['innovation', 'cost efficiency', 'customer service'])}",
                f"Market share estimated at {random.randint(5, 25)}%"
            ]
        }

    def generate_dataset(self, num_companies: int = 10) -> List[Dict[str, Any]]:
        """Generate a dataset of company profiles"""
        companies = []

        for _ in range(num_companies):
            company = self.generate_company_profile()
            companies.append(company)

        return companies

    def save_dataset(self, companies: List[Dict[str, Any]], filename: str = None):
        """Save dataset to JSON file"""
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"synthetic_companies_{timestamp}.json"

        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(companies, f, indent=2, ensure_ascii=False)

        print(f"Dataset saved to {filename}")

    def generate_tool_compatible_database(self, companies: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Generate a database format compatible with get_company_info tool"""
        company_db = {}
        
        for company in companies:
            company_name = company["name"]
            
            # Create tool-compatible company info
            company_db[company_name] = {
                "revenue": company["annual_revenue_usd"],
                "employees": company["employees"],
                "industry": company["industry"],
                "location": company["location"],
                "risk_score": self._calculate_risk_score(company),
                "founded": company["founded_year"],
                "products": company["products"],
                "partnerships": [p["partner"] for p in company["partnerships"]],
                "compliance_score": len(company["compliance_requirements"]) * 10,
                "market_position": company["briefing_template_data"]["market_position"]
            }
        
        return company_db

    def generate_web_search_data(self, companies: List[Dict[str, Any]]) -> Dict[str, str]:
        """Generate mock web search results for each company"""
        search_results = {}
        
        for company in companies:
            company_name = company["name"]
            
            # Create realistic web search snippet
            partnerships_text = ", ".join([p["partner"] for p in company["partnerships"][:2]])
            products_text = ", ".join(company["products"][:2])
            
            search_snippet = (
                f"{company_name} is a {company['size_category'].lower()} {company['industry'].lower()} "
                f"company founded in {company['founded_year']}. Key products include {products_text}. "
                f"Recent partnerships with {partnerships_text}. "
                f"Headquartered in {company['location']} with {company['employees']} employees."
            )
            
            search_results[company_name] = search_snippet
        
        return search_results

    def generate_document_templates(self) -> Dict[str, str]:
        """Generate document templates for the generate_document tool"""
        templates = {
            "company_briefing": """
# Company Briefing: {company_name}

## Executive Summary
{executive_summary}

## Company Overview
- **Industry**: {industry}
- **Founded**: {founded_year}
- **Employees**: {employees}
- **Revenue**: ${annual_revenue_usd:,}
- **Location**: {location}

## Products & Services
{products_list}

## Market Position
{market_position}

## Key Partnerships
{partnerships_list}

## Risk Assessment
- **Risk Level**: {risk_level}
- **Risk Category**: {risk_category}
- **Compliance Requirements**: {compliance_list}

## Recent Developments
{recent_developments}

## Competitive Landscape
{competitive_landscape}

---
*Generated on {timestamp}*
            """,
            
            "security_summary": """
# Security Assessment: {company_name}

## Risk Profile
- **Risk Level**: {risk_level}
- **Risk Category**: {risk_category}
- **Sensitive Projects**: {sensitive_projects_count}

## Compliance Status
{compliance_list}

## Security Recommendations
Based on risk assessment, recommend enhanced due diligence for {risk_category} category.
            """,
            
            "partnership_overview": """
# Partnership Analysis: {company_name}

## Current Partnerships
{partnerships_detailed}

## Strategic Value
{partnership_analysis}
            """
        }
        
        return templates

    def _calculate_risk_score(self, company: Dict[str, Any]) -> float:
        """Calculate numerical risk score for tool compatibility"""
        risk_level = company["risk_level"]
        base_scores = {"Low": 2.0, "Medium": 5.0, "High": 8.0, "Critical": 10.0}
        
        base_score = base_scores.get(risk_level, 5.0)
        
        # Adjust based on industry
        high_risk_industries = ["Defense & Aerospace", "Financial Services", "Healthcare", "Government"]
        if company["industry"] in high_risk_industries:
            base_score += 1.0
        
        # Adjust based on company size (larger = higher risk)
        size_multipliers = {"Startup": 0.8, "Small": 0.9, "Medium": 1.0, "Large": 1.1, "Enterprise": 1.2}
        multiplier = size_multipliers.get(company["size_category"], 1.0)
        
        return round(base_score * multiplier, 1)

    def save_tool_integration_files(self, companies: List[Dict[str, Any]], base_filename: str = "tool_data"):
        """Save separate files for tool integration"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Save company database for get_company_info tool
        company_db = self.generate_tool_compatible_database(companies)
        with open(f"{base_filename}_company_db_{timestamp}.json", 'w', encoding='utf-8') as f:
            json.dump(company_db, f, indent=2)
        
        # Save web search data for mock_web_search tool
        search_data = self.generate_web_search_data(companies)
        with open(f"{base_filename}_web_search_{timestamp}.json", 'w', encoding='utf-8') as f:
            json.dump(search_data, f, indent=2)
        
        # Save document templates
        templates = self.generate_document_templates()
        with open(f"{base_filename}_templates_{timestamp}.json", 'w', encoding='utf-8') as f:
            json.dump(templates, f, indent=2)
        
        # Save security filter data (sensitive terms)
        security_data = self._generate_security_filter_data(companies)
        with open(f"{base_filename}_security_{timestamp}.json", 'w', encoding='utf-8') as f:
            json.dump(security_data, f, indent=2)
        
        print(f"Tool integration files saved with timestamp {timestamp}")

    def _generate_security_filter_data(self, companies: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Generate security filter data for sensitive term detection"""
        all_sensitive_projects = []
        high_risk_companies = []
        sensitive_keywords = set()
        
        for company in companies:
            # Collect sensitive project names
            all_sensitive_projects.extend(company["sensitive_internal_projects"])
            
            # Identify high-risk companies
            if company["risk_level"] in ["High", "Critical"]:
                high_risk_companies.append(company["name"])
            
            # Collect sensitive keywords
            sensitive_keywords.update(company["sensitive_keywords"])
        
        return {
            "sensitive_project_names": list(set(all_sensitive_projects)),
            "high_risk_companies": high_risk_companies,
            "sensitive_keywords": list(sensitive_keywords),
            "filter_rules": {
                "block_internal_projects": True,
                "redact_sensitive_keywords": True,
                "flag_high_risk_companies": True
            }
        }

    def print_summary(self, companies: List[Dict[str, Any]]):
        """Print a summary of the generated dataset"""
        print(f"\n📊 Generated {len(companies)} company profiles:")
        print("=" * 50)
        
        # Industry distribution
        industries = {}
        risk_levels = {}
        
        for company in companies:
            industry = company["industry"]
            risk_level = company["risk_level"]
            
            industries[industry] = industries.get(industry, 0) + 1
            risk_levels[risk_level] = risk_levels.get(risk_level, 0) + 1
        
        print("\n🏢 Industry Distribution:")
        for industry, count in sorted(industries.items()):
            print(f"  • {industry}: {count}")
        
        print("\n⚠️  Risk Level Distribution:")
        for risk_level, count in sorted(risk_levels.items()):
            print(f"  • {risk_level}: {count}")
        
        print("\n🤝 Sample Partnerships:")
        partnership_count = 0
        for company in companies[:3]:
            for partnership in company["partnerships"][:2]:
                print(f"  • {company['name']} ↔ {partnership['partner']} ({partnership['type']})")
                partnership_count += 1
                if partnership_count >= 5:
                    break
            if partnership_count >= 5:
                break
        
        print("\n🔒 Security Analysis:")
        total_sensitive_projects = sum(len(c["sensitive_internal_projects"]) for c in companies)
        high_risk_count = sum(1 for c in companies if c["risk_level"] in ["High", "Critical"])
        print(f"  • Total sensitive internal projects: {total_sensitive_projects}")
        print(f"  • High/Critical risk companies: {high_risk_count}")
        
        print("\n📋 Sample Companies:")
        for i, company in enumerate(companies[:3]):
            print(f"\n{i+1}. {company['name']}")
            print(f"   Industry: {company['industry']}")
            print(f"   Products: {', '.join(company['products'][:2])}{'...' if len(company['products']) > 2 else ''}")
            print(f"   Risk: {company['risk_level']} ({company['risk_category']})")
            print(f"   Size: {company['size_category']} ({company['employees']} employees)")
            print(f"   Partnerships: {', '.join([p['partner'] for p in company['partnerships'][:2]])}")
            if company["sensitive_internal_projects"]:
                print(f"   Internal Projects: {', '.join(company['sensitive_internal_projects'])}")

def main():
    """Main function with cli"""
    parser = argparse.ArgumentParser(description="Generate synthetic company profile test data")
    parser.add_argument(
        "--count", "-c", 
        type=int,
        default=10,
        help="Number of company profiles to generate (default: 10)"
    )
    parser.add_argument(
        "--output", "-o", 
        type=str,
        help="Output filename (default: auto-generated with timestamp)"
    )
    parser.add_argument(
        "--seed",
        type=int,
        default=2025,
        help="Random seed for reproducible results"
    )
    parser.add_argument(
        "--tool-integration", "-t",
        action="store_true",
        help="Generate additional files for tool integration (company DB, web search data, templates, security filters)"
    )
    parser.add_argument(
        "--summary", "-s",
        action="store_true",
        help="Print detailed summary of generated data"
    )

    args = parser.parse_args()

    if args.seed:
        random.seed(args.seed)
        print(f"🎲 Using random seed: {args.seed}")

    generator = CompanyDataGenerator()
    companies = generator.generate_dataset(args.count)

    # Save main dataset
    generator.save_dataset(companies, args.output)
    
    # Generate tool integration files if requested
    if args.tool_integration:
        print("\n🔧 Generating tool integration files...")
        base_name = args.output.split('.')[0] if args.output else "agent_test_data"
        generator.save_tool_integration_files(companies, base_name)
    
    # Print summary if requested
    if args.summary:
        generator.print_summary(companies)

    print(f"\n✅ Successfully generated {args.count} company profiles!")
    
    if args.tool_integration:
        print("🎯 Ready for agent testing with:")
        print("   • Company database for get_company_info tool")
        print("   • Web search data for mock_web_search tool") 
        print("   • Document templates for generate_document tool")
        print("   • Security filter data for security_filter tool")


if __name__ == "__main__":
    main()
