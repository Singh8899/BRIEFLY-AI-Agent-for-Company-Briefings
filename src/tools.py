"""Define custom tools for the agent"""

import json
import os
from langchain_core.tools import tool

def _load_company_data():
    """Load company database from JSON file"""
    data_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'company_database.json')
    try:
        with open(data_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Warning: Company database file not found at {data_path}")
        return {"companies": []}
    except json.JSONDecodeError:
        print(f"Warning: Invalid JSON in company database file at {data_path}")
        return {"companies": []}

_company_data = _load_company_data() 


@tool
def get_company_info(company_name: str) -> str:
    """Retrieve structured internal company data
    
    Args:
        company_name: The name of the company to get information for
        
    Returns:
        Company information as a string
    """
    data = {"Company A": "Revenue $100M, Employees: 500", "Company B": "Revenue $200M, Employees: 1000"}
    return data.get(company_name, f"No information found for {company_name}")

@tool
def web_search(company_name: str) -> str:
    """Retrieve public info about products and partnerships
    
    Args:
        company_name: The name of the company to search for
        
    Returns:
        Search results as a string
    """
    data = {"Company A": "Recent news shows 15% growth", "Company B": "Expansion into European markets"}
    return data.get(company_name, f"No search results found for {company_name}")

@tool
def translate_document(document: str, target_language: str) -> str:
    """Translate document to a target language.
    
    Args:
        document: The document to translate
        target_language: The target language for translation
        
    Returns:
        Translated text
    """
    translations = {"Berlin": "Berlim", "Bologna": "Bolonha", "London": "Londres", "Paris": "Paris"}
    return translations.get(document, f"Translation of '{document}' to {target_language} not available")

@tool
def generate_document(template: str, content_dict: dict) -> str:
    """Create a structured briefing document
    
    Args:
        template: The name of the company
        content_dict: The content to include in the document
        
    Returns:
        Generated document content
    """
    templates = {
        "Company A": f"Company A {template}: Leading technology firm with strong market position",
        "Company B": f"Company B {template}: Global enterprise with diverse portfolio"
    }
    return templates.get(template, f"No {template} template available for {template}")

@tool
def security_filter(content: str) -> str:
    """Remove sensitive internal terms from the document.
    
    Args:
        content: The content to check for security
        
    Returns:
        Security assessment result
    """
    security_data = {
        "Company A": "Security Status: APPROVED - Content cleared for distribution",
        "Company B": "Security Status: REQUIRES REVIEW - Sensitive information detected"
    }
    # Simple keyword-based security check
    for company, status in security_data.items():
        if company.lower() in content.lower():
            return status
    return "Security Status: CLEARED - No sensitive content detected"

# List of tools to be used by the agent
tools = [
    get_company_info,
    web_search,
    translate_document,
    generate_document,
    security_filter
]
