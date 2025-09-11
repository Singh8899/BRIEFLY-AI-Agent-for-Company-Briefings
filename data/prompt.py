"""System prompt for the synthetic dataset generator"""

from typing import List, Optional
from pydantic import BaseModel


class InternalInfo(BaseModel):
    industry: str
    products: List[str]
    risk_category: Optional[str] = None
    notes: Optional[str] = None  # free text for extra details


class ExternalInfo(BaseModel):
    public_products: List[str]
    partnerships: Optional[List[str]] = None
    website: Optional[str] = None
    description: Optional[str] = None


class CompanyProfile(BaseModel):
    name: str
    internal: InternalInfo
    external: ExternalInfo

class CompanyProfiles(BaseModel):
    companies: List[CompanyProfile]



def get_system_prompt_data(num_companies: int) -> str:
    return f"""
        You are an expert data generator creating synthetic company profile data and mock web search results.
        You are to generate {num_companies} distinct company profiles.
        Your task is to generate an example of structured company data following the CompanyProfile schema.

        For each company, generate data for both INTERNAL and EXTERNAL information categories:

        NAME: The official/legal name of the company. Should be a single word.

        INTERNAL INFO (confidential company data):
        - industry: Specific industry sector (e.g., "Financial Services", "Healthcare Technology", "Manufacturing")
        - products: Detailed list of actual products/services offered
        - risk_category: Optional risk assessment ("Low", "Medium", "High", "Critical")
        - notes: Optional internal notes about the company (compliance issues, strategic importance, etc.)

        EXTERNAL INFO (public-facing data):
        - public_products: Marketing-friendly product descriptions
        - partnerships: Optional list of known business partnerships or alliances
        - website: Optional company website URL
        - description: Optional public company description/tagline

        Internally the projects should be something between 5 and 10.
        Externally can be something between 1 and 5.
        Generate diverse, realistic companies across different industries. Ensure internal and external data
        show realistic differences (e.g., internal names might be more formal, external descriptions more marketing-focused).
        Include a mix of risk categories and vary the optional fields to create realistic data diversity.

        Return the data as valid JSON following the CompanyProfile schema structure.
    """
