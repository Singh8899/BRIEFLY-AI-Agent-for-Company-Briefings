"""Define custom tools for the agent"""

import json
import os
import re
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Union

from googletrans import Translator
from jinja2 import BaseLoader, Environment, StrictUndefined, TemplateError
from langchain_core.tools import tool
from pydantic import BaseModel, Field, ValidationError

from agent_utils import parse_content
from security_filter import generate_security_report
from template_content import Content


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



class PresentInput(BaseModel):
    briefing: str = Field(..., description="Final company briefing to return.")
    meta: Dict[str, Any] = Field(default_factory=dict)

@tool(args_schema=PresentInput, return_direct=True)
def present_result(briefing: str, meta: Dict[str, Any]) -> str:
    """Save the briefing to a .txt file (optional metadata can control location/name)
    Call this tool to present the final document to the user.
    🔴 THIS MUST BE THE LAST STEP - call this to complete the workflow.
    """

    output_dir = meta.get("output_dir") or os.path.join(os.path.dirname(os.path.dirname(__file__)), "outputs")
    os.makedirs(output_dir, exist_ok=True)

    raw_name = meta.get("file_name") or meta.get("company") or f"briefing-{datetime.utcnow().strftime('%Y%m%dT%H%M%SZ')}"
    # sanitize filename
    safe_name = re.sub(r'[^A-Za-z0-9._-]', '_', raw_name)
    if not safe_name.lower().endswith(".txt"):
        safe_name = f"{safe_name}.txt"

    out_path = os.path.join(output_dir, safe_name)

    try:
        with open(out_path, "w", encoding="utf-8") as fh:
            fh.write(briefing)
        print(f"Briefing saved to: {out_path}")
    except Exception as e:
        print(f"Warning: failed to save briefing to {out_path}: {e}")
    return briefing

@tool
def list_available_companies() -> list:
    """List all companies in the database
    needed to check if a company exists before proceeding."""
    return list(_companies_data.keys())

@tool
def get_company_internal_info(company_name: str) -> dict:
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
def get_company_web_search(company_name: str) -> dict:
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
def translate_document(document: str, target_language: str) -> str:
    """Translate document to a target language if different from english.
    
    Args:
        document: The document to translate
        target_language: The target language for translation
        
    Returns:
        Translated text
    """
    translator = Translator()
    result = translator.translate(document, src='en', dest=target_language)
    return result.text

@tool
def generate_document(content: Union[Content, str, dict]) -> str:
    """Create a structured briefing document.

    Args:
        content: The content to include in the document
        should be a json serializable dict or Content model

    Returns:
        Generated document content
    """

    # Handle case where content might be a JSON string instead of dict
    content = parse_content(content)

    # Load the template
    current_file = Path(__file__)
    project_root = current_file.parent.parent
    template_path = os.path.join(project_root, "briefing_templates", "default.j2")

    try:
        with open(template_path, "r", encoding="utf-8") as f:
            template = f.read()
    except FileNotFoundError:
        print(f"Warning: Template not found at {template_path}, using fallback template.")
        template = "# {{ company.name }}\n\n{{ overview }}\n"

    # Validate & normalize inputs
    try:
        # Will coerce/validate types
        content = Content.model_validate(content)
        # Convert back to plain dict for Jinja
        data = content.model_dump()
    except ValidationError as ve:
        # Surface a concise error message
        raise ValueError(f"content_dict failed validation: {ve}") from ve
    except Exception:
        # fall back to the raw dict
        data = content

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
    
    Must use after generate_document and before translate_document.

    Args:
        company_name: The name of the company to check against
        content: The content to check for security
        
    Returns:
        Security assessment result
    """
    _company_data = _companies_data.get(company_name, {})
    internal_info = _company_data.get("internal", {})

    return generate_security_report(document, internal_info)


# List of tools to be used by the agent
tools = [
    list_available_companies,
    get_company_internal_info,
    get_company_web_search,
    security_filter,
    generate_document,
    translate_document,
    present_result
]
