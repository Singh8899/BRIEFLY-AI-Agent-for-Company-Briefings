import os

from openai import OpenAI
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

_security_prompt = """
You are a security auditor AI. Your task is to analyze the provided document and check whether it contains leaks of sensitive internal company information.

Inputs:
- Document to analyze:
{document}

- Reference internal information (highly confidential):
{internal_info}

Instructions:
1. Compare the document against the internal information.
2. Determine if there is any leakage:
   - NONE: No overlap or irrelevant mentions.
   - PARTIAL: Some overlap but not enough to expose full sensitive content.
   - STRONG LEAK: Significant or complete disclosure of internal information.
3. If leakage is detected, provide:
   - A summary of what was leaked.
   - Why it qualifies as a leak.
   - Risk assessment (LOW / MEDIUM / HIGH).
4. If no leakage is found, explicitly state "No internal information leaked."

"""

openai_client = OpenAI(
        api_key=os.getenv("OPENAI_API_KEY"),
        base_url=os.getenv("OPENAI_BASE_URL")
    )

def generate_security_report(document: str, internal_info: dict) -> str:
    """Generate a security report"""

    messages = [
        {
            "role": "user",
            "content": _security_prompt.format(
                document=document,
                internal_info=internal_info
            ),
        }
    ]

    response = openai_client.responses.parse(
        model=os.getenv("OPENAI_MODEL"),
        input=messages,
        temperature=float(os.getenv("OPENAI_TEMPERATURE")),
        top_p=float(os.getenv("OPENAI_TOP_P")),
    )

    return response.output_parsed
