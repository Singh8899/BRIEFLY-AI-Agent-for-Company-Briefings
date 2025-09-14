"""Set up the agent with custom tools and a Hugging Face model"""

import os

from dotenv import find_dotenv, load_dotenv
from langchain_core.messages import HumanMessage
from langchain_huggingface import ChatHuggingFace, HuggingFaceEndpoint
from langgraph.prebuilt import create_react_agent

from .prompt import PROMPT
from .security_filter import OutputValidator, PromptInjectionFilter
from .tools import tools

# Load environment variables from .env file
load_dotenv(find_dotenv())

# Load your Hugging Face model
llm = HuggingFaceEndpoint(
    repo_id=os.getenv("HUGGINGFACE_REPO_ID"),
    huggingfacehub_api_token=os.getenv("HUGGINGFACEHUB_API_TOKEN"),
    temperature=float(os.getenv("LLM_TEMPERATURE", 0.7)),
    top_p=float(os.getenv("LLM_TOP_P", 0.9)),
    provider=os.getenv("HUGGINGFACE_PROVIDER", "nebius"),
)

# Initialize the prompt injection filter
prompt_injection_filter = PromptInjectionFilter()

# Initialize the output validator
output_validator = OutputValidator()

# Wrap the endpoint in a ChatHuggingFace to make it compatible with LangGraph
model = ChatHuggingFace(llm=llm)

# Create the React agent with a system prompt guiding planning and tool use
agent = create_react_agent(
    model=model,
    tools=tools,
    prompt=PROMPT
)

# Run the agent with different queries
def run_agent_query(query: str):
    """Helper function to run a query with the agent"""


    # Check for prompt injection
    if prompt_injection_filter.detect_injection(query):
        return "Potential prompt injection detected."

    response = agent.invoke({"messages": [HumanMessage(content=query)]},
    {"recursion_limit":50})
    # Get the last message in the conversation
    last_message = response["messages"][-1]

    # Check if it's a tool message or AI message
    if hasattr(last_message, 'content') and last_message.content:
        return last_message.content
    
    # If no content, look for tool calls and their results
    messages = response["messages"]
    result_messages = []
    for msg in messages:
        if hasattr(msg, 'content') and msg.content and 'Company' in str(msg.content):
            result_messages.append(str(msg.content))
    message = output_validator.filter_response('\n'.join(result_messages) if result_messages else "No response generated")
    return message
