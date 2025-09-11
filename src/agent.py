"""Set up the agent with custom tools and a Hugging Face model"""

import os

from langgraph.prebuilt import create_react_agent
from langchain_huggingface import ChatHuggingFace, HuggingFaceEndpoint
from langchain_core.messages import HumanMessage
from dotenv import load_dotenv, find_dotenv

from tools import tools
from prompt import prompt


# Load environment variables from .env file
load_dotenv(find_dotenv())

# Load your Hugging Face model
print(f"Loading Hugging Face model... {os.getenv('HUGGINGFACE_REPO_ID')}")
llm = HuggingFaceEndpoint(
    repo_id=os.getenv("HUGGINGFACE_REPO_ID"),
    huggingfacehub_api_token=os.getenv("HUGGINGFACEHUB_API_TOKEN"),
    temperature=float(os.getenv("LLM_TEMPERATURE", 0.7)),
    top_p=float(os.getenv("LLM_TOP_P", 0.9)),
    provider="nebius"
)

# Wrap the endpoint in a ChatHuggingFace to make it compatible with LangGraph
model = ChatHuggingFace(llm=llm)

# Create the React agent with a system prompt guiding planning and tool use
agent = create_react_agent(
    model=model,
    tools=tools,
    prompt=prompt
)

# Run the agent with different queries
def run_agent_query(query: str):
    """Helper function to run a query with the agent"""
    response = agent.invoke({"messages": [HumanMessage(content=query)]})
    # Get the last message in the conversation
    last_message = response["messages"][-1]
    
    # Check if it's a tool message or AI message
    if hasattr(last_message, 'content') and last_message.content:
        return last_message.content
    else:
        # If no content, look for tool calls and their results
        messages = response["messages"]
        result_messages = []
        for msg in messages:
            if hasattr(msg, 'content') and msg.content and 'Company' in str(msg.content):
                result_messages.append(str(msg.content))
        return '\n'.join(result_messages) if result_messages else "No response generated"

# Test the agent with various queries
if __name__ == "__main__":
    print("=== Company A Information ===")
    print(run_agent_query("Get company information for Company A"))
    
    print("\n=== Company B Search ===")
    print(run_agent_query("Search for Company B"))
    
    print("\n=== Translation ===")
    print(run_agent_query("Translate 'Berlin' to Portuguese"))
    
    print("\n=== Document Generation ===")
    print(run_agent_query("Generate a document for Company A"))
    
    print("\n=== Security Check ===")
    print(run_agent_query("Check security for Company B"))


