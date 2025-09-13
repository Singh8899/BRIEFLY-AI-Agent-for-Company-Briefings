from pydantic import BaseModel
from typing import List, Optional

class Product(BaseModel):
    name: str
    description: Optional[str] = None

class Citation(BaseModel):
    title: str
    url: str

class Financials(BaseModel):
    revenue: Optional[str] = None
    market_cap: Optional[str] = None
    employees: Optional[str] = None

class Company(BaseModel):
    name: str
    industry: Optional[str] = None
    headquarters: Optional[str] = None
    founded: Optional[str] = None
    ceo: Optional[str] = None

class Content(BaseModel):
    company: Company
    overview: Optional[str] = None
    history: Optional[str] = None
    products: List[Product] = []
    partnerships: List[dict] = [] 
    financials: Financials = Financials()
    risks: List[str] = []
    citations: List[Citation] = []
    metadata: dict
