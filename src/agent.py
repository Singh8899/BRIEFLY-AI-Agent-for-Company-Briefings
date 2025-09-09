"""
Research Assistant Chatbot - Main Agent Framework
"""

import os
import json
import asyncio
import requests
import time
from typing import Dict, List, Any
from datetime import datetime
import logging
from dataclasses import dataclass, asdict

from langchain_community.llms import HuggingFaceEndpoint


from dotenv import load_dotenv


# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class AgentResponse:
    """Structure for agent responses"""
    content: str
    reasoning: str
    confidence: float
    sources: List[str]
    timestamp: str
    tokens_used: int

@dataclass
class ToolCall:
    """Structure for tool calls"""
    tool_name: str
    parameters: Dict[str, Any]
    result: Any
    success: bool
    execution_time: float

class ResearchTool:
    """Base class for research tools"""
    
    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description
    
    async def execute(self, query: str, **kwargs) -> Dict[str, Any]:
        """Execute the tool with given parameters"""
        raise NotImplementedError

class WebSearchTool(ResearchTool):
    """Web search tool for gathering information"""
    
    def __init__(self):
        super().__init__(
            name="web_search",
            description="Search the web for current information and research data"
        )
    
    async def execute(self, query: str, **kwargs) -> Dict[str, Any]:
        """Simulate web search (in real implementation, integrate with search API)"""
        await asyncio.sleep(0.5)  # Simulate API call
        
        # Simulated search results
        results = {
            "results": [
                {
                    "title": f"Research result for: {query}",
                    "content": f"Simulated research content about {query}. This would contain relevant information from web search.",
                    "url": f"https://example.com/research/{query.replace(' ', '-')}",
                    "relevance_score": 0.85
                }
            ],
            "total_results": 1,
            "search_time": 0.5
        }
        
        return {
            "success": True,
            "data": results,
            "sources": [result["url"] for result in results["results"]]
        }

class KnowledgeBaseTool(ResearchTool):
    """Tool for accessing internal knowledge base"""
    
    def __init__(self):
        super().__init__(
            name="knowledge_base",
            description="Access internal knowledge base for factual information"
        )
    
    async def execute(self, query: str, **kwargs) -> Dict[str, Any]:
        """Query internal knowledge base"""
        await asyncio.sleep(0.2)  # Simulate database query
        
        # Simulated knowledge base lookup
        knowledge = {
            "query": query,
            "facts": [
                f"Factual information related to {query}",
                "Additional contextual data",
                "Historical background information"
            ],
            "confidence": 0.9,
            "last_updated": "2024-01-01"
        }
        
        return {
            "success": True,
            "data": knowledge,
            "sources": ["internal_knowledge_base"]
        }

class MockLLM:
    """Mock LLM for testing when HuggingFace is not available"""
    
    def __call__(self, prompt: str) -> str:
        """Generate a mock response"""
        return f"Mock response to: {prompt[:100]}..."
    
    def invoke(self, prompt: str) -> str:
        """LangChain compatible invoke method"""
        return self(prompt)

class ResearchAgent:
    """Main Research Assistant Agent"""
    
    def __init__(self, model_name: str = None, hf_token: str = None):
        self.model_name = model_name or os.getenv("LLM_MODEL_NAME", "meta-llama/Llama-3.1-8B-Instruct")
        self.hf_token = hf_token or os.getenv("HUGGINGFACEHUB_API_TOKEN")
        self.max_tokens = int(os.getenv("LLM_MAX_TOKENS", "2048"))
        self.temperature = float(os.getenv("LLM_TEMPERATURE", "0.7"))
        self.max_iterations = int(os.getenv("MAX_ITERATIONS", "5"))
        self.top_p = float(os.getenv("LLM_TOP_P", "0.8"))

        # Initialize tools
        self.tools = {
            "web_search": WebSearchTool(),
            "knowledge_base": KnowledgeBaseTool()
        }
        
        # Conversation history
        self.conversation_history = []
        
        # Initialize LLM
        self._initialize_llm()
        
        logger.info(f"Research Agent initialized with model: {self.model_name}")
    
    def _initialize_llm(self):
        """Initialize the Hugging Face LLM"""
        try:
            self.llm = HuggingFaceEndpoint(
                repo_id=self.model_name,
                huggingfacehub_api_token=self.hf_token,
                max_new_tokens=self.max_tokens,
                temperature=self.temperature,
                top_p=self.top_p,
                do_sample=True,
            )
            logger.info("LLM initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize LLM: {e}")
            # Fallback to mock LLM for testing
            self.llm = MockLLM()
            logger.info("Using mock LLM for testing")
    
    def _should_use_tool(self, query: str) -> List[str]:
        """Determine which tools to use based on the query"""
        tools_to_use = []
        
        # Simple heuristics for tool selection
        query_lower = query.lower()
        
        if any(word in query_lower for word in ["current", "latest", "recent", "news", "today"]):
            tools_to_use.append("web_search")
        
        if any(word in query_lower for word in ["fact", "definition", "what is", "explain"]):
            tools_to_use.append("knowledge_base")
        
        # Default to knowledge base for general queries
        if not tools_to_use:
            tools_to_use.append("knowledge_base")
        
        return tools_to_use
    
    async def _execute_tools(self, query: str, tools_to_use: List[str]) -> List[ToolCall]:
        """Execute the selected tools"""
        tool_calls = []
        
        for tool_name in tools_to_use:
            if tool_name in self.tools:
                start_time = time.time()
                try:
                    result = await self.tools[tool_name].execute(query)
                    execution_time = time.time() - start_time
                    
                    tool_call = ToolCall(
                        tool_name=tool_name,
                        parameters={"query": query},
                        result=result,
                        success=result.get("success", False),
                        execution_time=execution_time
                    )
                    tool_calls.append(tool_call)
                    
                except Exception as e:
                    execution_time = time.time() - start_time
                    tool_call = ToolCall(
                        tool_name=tool_name,
                        parameters={"query": query},
                        result={"error": str(e)},
                        success=False,
                        execution_time=execution_time
                    )
                    tool_calls.append(tool_call)
        
        return tool_calls
    
    def _build_context(self, query: str, tool_calls: List[ToolCall]) -> str:
        """Build context from tool results"""
        context_parts = [f"User query: {query}"]
        
        for tool_call in tool_calls:
            if tool_call.success:
                context_parts.append(f"\n{tool_call.tool_name} results:")
                if "data" in tool_call.result:
                    context_parts.append(str(tool_call.result["data"]))
        
        return "\n".join(context_parts)
    
    def _generate_response(self, context: str, query: str) -> str:
        """Generate response using the LLM"""
        prompt = f"""Based on the following context and tools results, provide a comprehensive and helpful response to the user's query.

Context:
{context}

Guidelines:
1. Provide accurate information based on the context
2. Be clear and concise
3. Cite sources when available
4. If uncertain, acknowledge limitations

User query: {query}

Response:"""
        
        try:
            response = self.llm.invoke(prompt)
            return response
        except Exception as e:
            logger.error(f"Error generating response: {e}")
            return f"I apologize, but I encountered an error while processing your query: {query}. Please try again."
    
    def _extract_sources(self, tool_calls: List[ToolCall]) -> List[str]:
        """Extract sources from tool call results"""
        sources = []
        for tool_call in tool_calls:
            if tool_call.success and "sources" in tool_call.result:
                sources.extend(tool_call.result["sources"])
        return sources
    
    async def process_query(self, query: str) -> AgentResponse:
        """Process a user query and return a response"""
        start_time = time.time()
        
        # Determine which tools to use
        tools_to_use = self._should_use_tool(query)
        logger.info(f"Using tools: {tools_to_use}")
        
        # Execute tools
        tool_calls = await self._execute_tools(query, tools_to_use)
        
        # Build context from tool results
        context = self._build_context(query, tool_calls)
        
        # Generate response
        response_content = self._generate_response(context, query)
        
        # Extract sources
        sources = self._extract_sources(tool_calls)
        
        # Calculate confidence (simple heuristic)
        confidence = min(0.9, sum(1 for tc in tool_calls if tc.success) / max(len(tool_calls), 1))
        
        # Create response object
        response = AgentResponse(
            content=response_content,
            reasoning=f"Used tools: {', '.join(tools_to_use)}. Analysis based on gathered information.",
            confidence=confidence,
            sources=sources,
            timestamp=datetime.now().isoformat(),
            tokens_used=len(response_content.split())  # Approximation
        )
        
        # Add to conversation history
        self.conversation_history.append({
            "query": query,
            "response": response_content,
            "timestamp": response.timestamp,
            "tools_used": tools_to_use
        })
        
        processing_time = time.time() - start_time
        logger.info(f"Query processed in {processing_time:.2f}s")
        
        return response
    
    def get_conversation_history(self) -> List[Dict]:
        """Get the conversation history"""
        return self.conversation_history
    
    def clear_history(self):
        """Clear conversation history"""
        self.conversation_history = []
        logger.info("Conversation history cleared")
