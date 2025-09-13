"""System prompt for the synthetic dataset generator"""

from typing import List, Optional
from pydantic import BaseModel


class InternalInfo(BaseModel):
    industry: str
    products: List[str]
    risk_category: Optional[str] = None
    notes: Optional[str] = None  # free text for extra details
    methodologies: Optional[List[str]] = None  # internal frameworks/best practices
    kpis: Optional[List[str]] = None  # key performance indicators
    client_profiles: Optional[List[str]] = None  # organizational insights
    financial_estimates: Optional[str] = None  # revenue estimates, forecasts
    expertise_areas: Optional[List[str]] = None  # internal knowledge domains


class ExternalInfo(BaseModel):
    public_products: List[str]
    partnerships: Optional[List[str]] = None
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
        You are to generate {num_companies} distinct company profiles with comprehensive internal and external intelligence.
        Your task is to generate realistic structured company data following the CompanyProfile schema.

        For each company, generate data across both INTERNAL (proprietary) and EXTERNAL (publicly available) categories:

        NAME: The official/legal company name. Should be realistic and industry-appropriate.

        INTERNAL INFO (proprietary consulting knowledge):
        - industry: Specific industry sector (e.g., "Financial Services", "Healthcare Technology", "Manufacturing", "Retail", "Energy")
        - products: Detailed list of 5-10 actual products/services offered (technical names, internal project codes)
        - risk_category: Risk assessment ("Low", "Medium", "High", "Critical") based on financial stability, market position
        - notes: Internal observations (compliance issues, strategic challenges, leadership changes, operational concerns)
        - methodologies: Internal frameworks used (e.g., "Agile Development", "Six Sigma", "Design Thinking", "Lean Manufacturing")
        - kpis: Key performance metrics (e.g., "Customer Retention 85%", "Market Share 12%", "EBITDA Margin 15%")
        - client_profiles: Organizational insights (e.g., "Mid-market B2B", "Enterprise Fortune 500", "Government contractor")
        - financial_estimates: Revenue/growth estimates from past engagements (e.g., "$50M ARR", "20% YoY growth projected")
        - expertise_areas: Internal knowledge domains (e.g., "Cloud Migration", "Digital Transformation", "Supply Chain Optimization")

        EXTERNAL INFO (publicly available intelligence):
        - public_products: 1-5 marketing-friendly product descriptions (consumer-facing names)
        - partnerships: Strategic alliances, vendor relationships, channel partners
        - website: Realistic company website URL
        - description: Public company tagline/mission statement
        - recent_news: Recent developments (product launches, acquisitions, expansions, crises)
        - market_position: Competitive standing (e.g., "Market Leader", "Challenger", "Niche Player", "Startup")
        - regulatory_status: Compliance certifications, licenses (e.g., "ISO 27001", "SOC 2", "GDPR Compliant")
        - social_sentiment: Brand reputation indicator (e.g., "Positive", "Mixed", "Negative", "Neutral")

        GENERATION GUIDELINES:
        - Create realistic differences between internal (detailed/technical) vs external (polished/marketing) data
        - Include diverse industries: tech, finance, healthcare, manufacturing, retail, energy, consulting
        - Vary company sizes: startups, mid-market, enterprise, multinational corporations
        - Mix risk categories and optional fields for realistic diversity
        - Make internal data more granular and technical than external data
        - Ensure consistency between related fields (industry should align with products/expertise)

        Return the data as valid JSON following the CompanyProfiles schema structure with all companies in a "companies" array.
    """
