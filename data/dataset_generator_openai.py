""""Generate synthetic company profile data using OpenAI"""
import os
import argparse

from openai import OpenAI
from dotenv import load_dotenv, find_dotenv

from prompt import get_system_prompt_data, CompanyProfiles


load_dotenv(find_dotenv())

class dataset_generator_openai:
    """Generate synthetic company profile data using OpenAI"""
    def __init__(self):
        
        self.openai_client = OpenAI(
            api_key=os.getenv("OPENAI_API_KEY"),
            base_url=os.getenv("OPENAI_BASE_URL")
        )

    def generate_company_data(self, num_companies: int) -> CompanyProfiles:
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

        return response.output_parsed

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

    generator = dataset_generator_openai()
    company_profiles = generator.generate_company_data(num_companies=args.count)

    output_file = args.output if args.output else f"company_database.json"

    serializable_profiles = company_profiles.model_dump_json(indent=2)

    with open(output_file, "w", encoding="utf-8") as f:
        f.write(serializable_profiles)

    print(f"Saved profiles to {output_file}")

if __name__ == "__main__":
    main()