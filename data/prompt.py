"""System prompt for the synthetic dataset generator"""

from typing import List, Optional

from pydantic import BaseModel


class InternalProduct(BaseModel):
    name: str
    description: Optional[str] = None
    category: Optional[str] = None  # e.g., "Software", "Consulting", "Hardware"
    launch_year: Optional[int] = None
    revenue_contribution: Optional[str] = None  # e.g., "$10M annually", "20% of total revenue"

class InternalPartnership(BaseModel):
    partner_name: str
    relationship_type: Optional[str] = None  # e.g., "Strategic Alliance", "Vendor", "Channel Partner"
    start_year: Optional[int] = None
    details: Optional[str] = None  # free text for extra details

class InternalInfo(BaseModel):
    industry: str
    products: List[InternalProduct]
    risk_category: Optional[str] = None
    partnerships: Optional[List[InternalPartnership]] = None
    notes: Optional[str] = None  # free text for extra details
    methodologies: Optional[List[str]] = None  # internal frameworks/best practices
    kpis: Optional[List[str]] = None  # key performance indicators
    client_profiles: Optional[List[str]] = None  # organizational insights
    financial_estimates: Optional[str] = None  # revenue estimates, forecasts
    expertise_areas: Optional[List[str]] = None  # internal knowledge domains

class ExternalProduct(BaseModel):
    name: str
    description: Optional[str] = None
    category: Optional[str] = None  # e.g., "Software", "Consulting", "Hardware"
    launch_year: Optional[int] = None

class ExternalPartnership(BaseModel):
    partner_name: str
    relationship_type: Optional[str] = None  # e.g., "Strategic Alliance", "Vendor", "Channel Partner"
    start_year: Optional[int] = None
    details: Optional[str] = None  # free text for extra details

class ExternalInfo(BaseModel):
    public_products: List[ExternalProduct]
    partnerships: Optional[List[ExternalPartnership]] = None
    website: Optional[str] = None
    description: Optional[str] = None
    recent_news: Optional[List[str]] = None  # recent developments
    market_position: Optional[str] = None  # competitive standing
    regulatory_status: Optional[List[str]] = None  # compliance, certifications
    social_sentiment: Optional[str] = None  # brand reputation indicator


class CompanyProfile(BaseModel):
    name: str
    internal: InternalInfo
    external: ExternalInfo

class CompanyProfiles(BaseModel):
    companies: List[CompanyProfile]


def get_system_prompt_data(num_companies: int) -> str:
    return f"""
        You are an expert data generator creating synthetic company profile data for a consulting/business intelligence context.
        Generate {num_companies} distinct, realistic company profiles with comprehensive internal and external intelligence.
        
        CRITICAL: Return valid JSON that strictly follows the CompanyProfiles schema with a "companies" array.

        DETAILED FIELD REQUIREMENTS:
    
        COMPANY NAME: Generate realistic company names appropriate for each industry. MUST BE A SINGLE WORD

        INTERNAL INFO (Proprietary consulting data):
        - industry: Specific sectors like "Financial Services", "Healthcare Technology", "Advanced Manufacturing", "Renewable Energy", "E-commerce Platform"
        - products: 3-8 internal products with technical names, detailed descriptions, categories ("Software", "Consulting", "Hardware", "Service"), launch years (2015-2024), revenue contributions ("$5M annually", "15% of revenue")
        - risk_category: Balanced distribution across "Low", "Medium", "High", "Critical"
        - partnerships: 1-4 internal partnerships with technical relationship types, start years, operational details
        - notes: Insider observations about compliance, leadership, strategy, operational challenges (100-200 words)
        - methodologies: 2-5 internal frameworks like "Agile", "Six Sigma", "Design Thinking", "DevOps", "Lean Manufacturing"
        - kpis: 3-6 specific metrics with values like "Customer Retention 87%", "Market Share 12%", "EBITDA 18%"
        - client_profiles: 2-4 segments like "Mid-market B2B", "Enterprise Fortune 500", "Government contracts"
        - financial_estimates: Specific revenue data from engagements like "$50M ARR", "25% YoY growth"
        - expertise_areas: 3-6 domains like "Cloud Migration", "Digital Transformation", "Supply Chain Optimization"

        EXTERNAL INFO (Publicly available data):
        - public_products: 1-4 consumer-facing products with marketing names and descriptions
        - partnerships: 1-3 public partnerships with marketing-friendly descriptions
        - website: Realistic URLs matching company names
        - description: Professional taglines/mission statements (50-100 words)
        - recent_news: 2-4 realistic developments (product launches, acquisitions, expansions, challenges)
        - market_position: Distribute across "Market Leader", "Challenger", "Niche Player", "Startup"
        - regulatory_status: Relevant certifications like "ISO 27001", "SOC 2", "GDPR Compliant", "FDA Approved"
        - social_sentiment: Mix of "Positive", "Mixed", "Negative", "Neutral" based on realistic scenarios

        GENERATION GUIDELINES:
        - Create clear distinctions between internal (technical/detailed) vs external (polished/marketing) data
        - Ensure industry diversity: technology, finance, healthcare, manufacturing, retail, energy, consulting, aerospace
        - Vary company sizes and maturity levels realistically
        - Make optional fields realistically sparse (not every company has all fields)
        - Ensure internal products are more technical than external products
        - Align all company data for consistency (industry should match products, expertise, partnerships)
        - Use realistic years, metrics, and financial figures
        - Create believable company narratives across all fields

        OUTPUT FORMAT: Return only valid JSON with no additional text, comments, or markdown formatting.
    """