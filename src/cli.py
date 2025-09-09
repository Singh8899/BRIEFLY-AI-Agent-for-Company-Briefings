"""
Command Line Interface for Research Assistant Chatbot
"""

import asyncio
import argparse
import sys
from pathlib import Path

# Add src to path
sys.path.append(str(Path(__file__).parent))

from agent import ResearchAgent
from evaluation import TestDataGenerator, AgentEvaluator

def print_banner():
    """Print application banner"""
    print("\n" + "="*60)
    print("🤖 RESEARCH ASSISTANT CHATBOT")
    print("Powered by Meta-Llama/Llama-3.1-8B-Instruct")
    print("="*60)

async def interactive_mode(agent: ResearchAgent):
    """Run interactive chat mode"""
    print("\nEntering interactive mode. Type 'quit' to exit.")
    print("Type 'clear' to clear conversation history.")
    print("Type 'history' to see conversation history.\n")
    
    while True:
        try:
            query = input("You: ").strip()
            
            if query.lower() in ['quit', 'exit', 'q']:
                print("Goodbye!")
                break
            elif query.lower() == 'clear':
                agent.clear_history()
                print("Conversation history cleared.")
                continue
            elif query.lower() == 'history':
                history = agent.get_conversation_history()
                if history:
                    print("\n--- Conversation History ---")
                    for i, entry in enumerate(history[-5:], 1):  # Show last 5
                        print(f"{i}. Query: {entry['query'][:50]}...")
                        print(f"   Response: {entry['response'][:100]}...")
                        print(f"   Tools: {entry['tools_used']}")
                        print()
                else:
                    print("No conversation history.")
                continue
            elif not query:
                continue
            
            print("Assistant: Thinking...")
            response = await agent.process_query(query)
            
            print(f"\nAssistant: {response.content}")
            print(f"\nConfidence: {response.confidence:.2f}")
            print(f"Sources: {', '.join(response.sources) if response.sources else 'None'}")
            print(f"Reasoning: {response.reasoning}")
            print(f"Response time: {response.timestamp}")
            print("-" * 50)
            
        except KeyboardInterrupt:
            print("\nGoodbye!")
            break
        except Exception as e:
            print(f"Error: {e}")

async def evaluation_mode(agent: ResearchAgent, output_dir: str = "evaluation_results"):
    """Run evaluation mode"""
    print("\nRunning evaluation mode...")
    
    # Create output directory
    Path(output_dir).mkdir(exist_ok=True)
    
    # Generate test data
    print("Generating test data...")
    generator = TestDataGenerator()
    test_cases = generator.get_all_test_cases()
    
    # Save test cases
    test_cases_path = Path(output_dir) / "test_cases.json"
    generator.save_test_cases(str(test_cases_path))
    
    # Run evaluation
    print(f"Evaluating agent on {len(test_cases)} test cases...")
    evaluator = AgentEvaluator(agent)
    results = await evaluator.evaluate_agent(test_cases)
    
    # Generate report
    report_path = Path(output_dir) / "evaluation_report.json"
    evaluator.generate_report(results, str(report_path))
    
    print(f"Evaluation complete! Results saved to {output_dir}/")

async def single_query_mode(agent: ResearchAgent, query: str):
    """Process a single query"""
    print(f"\nProcessing query: {query}")
    response = await agent.process_query(query)
    
    print(f"\nResponse: {response.content}")
    print(f"Confidence: {response.confidence:.2f}")
    print(f"Sources: {', '.join(response.sources) if response.sources else 'None'}")
    print(f"Tools used: {response.reasoning}")

def main():
    """Main CLI function"""
    parser = argparse.ArgumentParser(
        description="Research Assistant Chatbot CLI",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python cli.py --interactive                    # Start interactive chat
  python cli.py --evaluate                      # Run full evaluation
  python cli.py --query "What is AI?"           # Process single query
  python cli.py --model "custom-model" --token "hf_token"  # Custom model
        """
    )
    
    parser.add_argument(
        "--interactive", "-i",
        action="store_true",
        help="Start interactive chat mode"
    )
    
    parser.add_argument(
        "--evaluate", "-e",
        action="store_true",
        help="Run evaluation mode"
    )
    
    parser.add_argument(
        "--query", "-q",
        type=str,
        help="Process a single query"
    )
    
    parser.add_argument(
        "--model", "-m",
        type=str,
        help="HuggingFace model name (default: meta-llama/Llama-3.1-8B-Instruct)"
    )
    
    parser.add_argument(
        "--token", "-t",
        type=str,
        help="HuggingFace API token"
    )
    
    parser.add_argument(
        "--output-dir", "-o",
        type=str,
        default="evaluation_results",
        help="Output directory for evaluation results"
    )
    
    args = parser.parse_args()
    
    # Show banner
    print_banner()
    
    # Initialize agent
    print("Initializing Research Assistant Agent...")
    try:
        agent = ResearchAgent(
            model_name=args.model,
            hf_token=args.token
        )
        print("✅ Agent initialized successfully!")
    except Exception as e:
        print(f"❌ Failed to initialize agent: {e}")
        print("Note: Make sure you have set HF_API_TOKEN in your .env file")
        print("The agent will use mock responses for testing.")
        agent = ResearchAgent()
    
    # Run selected mode
    try:
        if args.interactive:
            asyncio.run(interactive_mode(agent))
        elif args.evaluate:
            asyncio.run(evaluation_mode(agent, args.output_dir))
        elif args.query:
            asyncio.run(single_query_mode(agent, args.query))
        else:
            print("Please specify a mode: --interactive, --evaluate, or --query")
            print("Use --help for more information.")
    
    except KeyboardInterrupt:
        print("\nOperation cancelled by user.")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
