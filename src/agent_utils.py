import ast
import json
import re

from template_content import Content


def parse_content(content_str: str):
    """Parse content string whether it's JSON or Python dict format"""

    if isinstance(content_str, str):
        content_str = content_str.strip()
        
        try:
            # Try JSON first
            return json.loads(content_str)
        except json.JSONDecodeError:
            try:
                # Try Python literal eval
                return ast.literal_eval(content_str)
            except (ValueError, SyntaxError):
                try:
                    fixed_str = re.sub(r"'([^']*)':", r'"\1":', content_str)  # Fix keys
                    fixed_str = re.sub(r": '([^']*)'", r': "\1"', fixed_str)   # Fix values
                    return json.loads(fixed_str)
                except:
                    raise ValueError("Could not parse content string as JSON or Python dict")
    elif isinstance(content_str, dict):
        return content_str
    elif isinstance(content_str, Content):
        return content_str.model_dump()