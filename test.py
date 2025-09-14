import argparse

from src.agent import run_agent_query

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run agent queries")
    parser.add_argument(
        "-q",
        type=str,
        help="The query to run",
        default="Provide a detailed briefing on the company OpenAI, including its products, partnerships, and any recent news.",
    )
    args = parser.parse_args()

    print(f"=== Query: {args.q} ===")
    print(run_agent_query(args.q))
