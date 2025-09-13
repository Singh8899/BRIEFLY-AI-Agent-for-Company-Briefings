"""Define custom tools for the agent"""

import json
import os


from jinja2 import Environment, BaseLoader, StrictUndefined, TemplateError
from pydantic import ValidationError

from langchain_core.tools import tool, InjectedToolArg
from googletrans import Translator

from template_content import Content
from security_filter import generate_security_report


def _load_company_data():
    """Load company database from JSON file"""
    data_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'company_database.json')
    try:
        with open(data_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Warning: Company database file not found at {data_path}")
        return {}
    except json.JSONDecodeError:
        print(f"Warning: Invalid JSON in company database file at {data_path}")
        return {}

_companies_data = _load_company_data()



@tool
def list_companies() -> list:
    """List all companies in the database"""
    return list(_companies_data.keys())

@tool
def get_company_info(company_name: str) -> dict:
    """Retrieve structured internal company data
    
    Args:
        company_name: The name of the company to get information for
        
    Returns:
        Company information as a dictionary
    """
    _company_data = _companies_data.get(company_name, {})
    internal_info = _company_data.get("internal", {})
    return internal_info

@tool
def web_search(company_name: str) -> dict:
    """Retrieve public info about products and partnerships
    
    Args:
        company_name: The name of the company to search for
        
    Returns:
        Search results as a dictionary
    """
    _company_data = _companies_data.get(company_name, {})
    external_info = _company_data.get("external", {})
    return external_info

@tool
async def translate_document(document: str, target_language: str) -> str:
    """Translate document to a target language.
    
    Args:
        document: The document to translate
        target_language: The target language for translation
        
    Returns:
        Translated text
    """
    translator = Translator()
    result = await translator.translate(document, src='en', dest=target_language)
    return result.text

@tool
def generate_document(content_dict: dict) -> str:
    """Create a structured briefing document
    
    Args:
        content_dict: The content to include in the document
        
    Returns:
        Generated document content
    """
    # Load the template
    template_path = os.path.join("..","briefing_templates", "default.j2")
    try:
        with open(template_path, "r", encoding="utf-8") as f:
            template = f.read()
    except FileNotFoundError:
        print(f"Warning: Template not found at {template_path}, using fallback template.")
        template = "# {{ company.name }}\n\n{{ overview }}\n"

    # Validate & normalize inputs
    try:
        # Will coerce/validate types
        content = Content.model_validate(content_dict)
        # Convert back to plain dict for Jinja
        data = content.model_dump()
    except ValidationError as ve:
        # Surface a concise error message
        raise ValueError(f"content_dict failed validation: {ve}") from ve
    except Exception:
        # fall back to the raw dict
        data = content_dict

    # Prepare Jinja environment
    env = Environment(
        loader=BaseLoader(),
        undefined=StrictUndefined,
        autoescape=False,
        trim_blocks=True,
        lstrip_blocks=True,
    )

    # Render
    try:
        tmpl = env.from_string(template)
        rendered = tmpl.render(**data)
    except TemplateError as te:
        raise RuntimeError(f"Template rendering failed: {te}") from te

    # Post-process
    lines = [line.rstrip() for line in rendered.strip().splitlines()]

    document_md = "\n".join(lines)

    return document_md


@tool
def security_filter(company_name:str, document: str) -> str:
    """Return report on security vulnerabilities.
    
    Args:
        company_name: The name of the company to check against
        content: The content to check for security
        
    Returns:
        Security assessment result
    """
    _company_data = _companies_data.get(company_name, {})
    internal_info = _company_data.get("internal", {})

    return generate_security_report(document, internal_info)

@tool
def document_format() -> dict:
    """Return the required data structure format for document generation.
    
    This tool provides the schema that defines how data should be structured
    when calling the generate_document tool. Use this to understand the
    expected format before gathering and organizing company information.

    Returns:
        dict: JSON schema defining the required data structure for documents
    """
    
    return Content.model_dump_schema()




# List of tools to be used by the agent
tools = [
    list_companies,
    get_company_info,
    web_search,
    document_format,
    security_filter,
    generate_document,
    translate_document
]
