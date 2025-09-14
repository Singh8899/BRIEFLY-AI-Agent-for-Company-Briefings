"""Template for structured content"""
from typing import List, Optional

from pydantic import BaseModel


class Product(BaseModel):
    """Product information"""
    product_name: str
    product_description: Optional[str] = None

class Citation(BaseModel):
    """Citation information"""
    citation_title: str = None
    citation_url: str = None
class Financials(BaseModel):
    """Financial information"""
    financial_revenue: Optional[str] = None
    financial_market_cap: Optional[str] = None
    financial_employees: Optional[str] = None

class Partnership(BaseModel):
    """Partnership information"""
    title: str
    summary: Optional[str] = None
    source: Optional[str] = None

class Content(BaseModel):
    """Structured content for company briefing"""
    company_name: str
    company_industry: Optional[str] = None
    company_headquarters: Optional[str] = None
    company_founded_year: Optional[int] = None
    company_ceo: Optional[str] = None
    content_overview: Optional[str] = None
    content_history: Optional[str] = None
    content_products: List[Product] = []
    content_partnerships: List[Partnership] = []
    content_financials: Financials = Financials()
    content_risks: List[str] = []
    content_citations: List[Citation] = []
