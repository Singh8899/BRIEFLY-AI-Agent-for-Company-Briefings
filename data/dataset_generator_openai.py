""""Generate synthetic company profile data using OpenAI"""
import argparse
import json
import os

from dotenv import find_dotenv, load_dotenv
from openai import OpenAI

from prompt import CompanyProfiles, get_system_prompt_data

load_dotenv(find_dotenv())

class datasetGeneratorOpenAI:
    """Generate synthetic company profile data using OpenAI"""
    def __init__(self):

        self.openai_client = OpenAI(
            api_key=os.getenv("OPENAI_API_KEY"),
            base_url=os.getenv("OPENAI_BASE_URL")
        )


    def _to_company_dict(self, payload):
        # payload is the CompanyProfiles model returned by OpenAI
        out = {}
        for c in payload.companies:
            name = c.name
            out[name] = {
                "internal": c.internal.model_dump(),
                "external": c.external.model_dump(),
            }
        return out

    def generate_company_data(self, num_companies: int) -> dict:
        """Generate a synthetic company profile"""

        messages = [
            {
                "role": "user",
                "content": get_system_prompt_data(num_companies),
            }
        ]

        response = self.openai_client.responses.parse(
            model=os.getenv("OPENAI_MODEL"),
            input=messages,
            temperature=float(os.getenv("OPENAI_TEMPERATURE")),
            top_p=float(os.getenv("OPENAI_TOP_P")),
            text_format=CompanyProfiles
        )

        return self._to_company_dict(response.output_parsed)

def main():
    """Main function to generate and print synthetic company profiles"""
    parser = argparse.ArgumentParser(description="Generate synthetic company profile test data")
    parser.add_argument(
        "--count", "-c", 
        type=int,
        default=10,
        help="Number of company profiles to generate (default: 10)"
    )
    parser.add_argument(
        "--output", "-o", 
        type=str,
        help="Output filename (default: company_database.json)"
    )
    args = parser.parse_args()

    generator = datasetGeneratorOpenAI()
    company_profiles = generator.generate_company_data(num_companies=args.count)

    output_file = args.output if args.output else f"company_database.json"

    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(company_profiles, f, indent=2, ensure_ascii=False)

    print(f"Saved profiles to {output_file}")

if __name__ == "__main__":
    main()
