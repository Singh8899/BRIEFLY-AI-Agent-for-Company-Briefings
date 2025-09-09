"""
Evaluation Framework for Research Assistant Chatbot
"""

import asyncio
import json
import time
from typing import Dict, List, Any, Tuple, Optional
from datetime import datetime
from dataclasses import dataclass, asdict
import logging
from pathlib import Path

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class TestCase:
    """Structure for individual test cases"""
    id: str
    query: str
    expected_topics: List[str]
    expected_tools: List[str]
    difficulty: str  # easy, medium, hard
    category: str
    ground_truth: Optional[str] = None

@dataclass
class EvaluationMetrics:
    """Structure for evaluation metrics"""
    accuracy: float
    relevance: float
    tool_selection_accuracy: float
    response_time: float
    confidence_calibration: float
    source_citation_rate: float

@dataclass
class TestResult:
    """Structure for individual test results"""
    test_case_id: str
    query: str
    response_content: str
    tools_used: List[str]
    expected_tools: List[str]
    response_time: float
    confidence: float
    sources: List[str]
    metrics: Dict[str, float]
    passed: bool

class TestDataGenerator:
    """Generates synthetic test data for agent evaluation"""
    
    def __init__(self):
        self.test_cases = []
    
    def generate_basic_tests(self) -> List[TestCase]:
        """Generate basic test cases"""
        basic_tests = [
            TestCase(
                id="basic_001",
                query="What is artificial intelligence?",
                expected_topics=["AI", "machine learning", "technology"],
                expected_tools=["knowledge_base"],
                difficulty="easy",
                category="definition",
                ground_truth="AI is a branch of computer science that aims to create intelligent machines."
            ),
            TestCase(
                id="basic_002",
                query="Explain the concept of machine learning",
                expected_topics=["ML", "algorithms", "data"],
                expected_tools=["knowledge_base"],
                difficulty="easy",
                category="explanation"
            ),
            TestCase(
                id="basic_003",
                query="What are the latest developments in quantum computing?",
                expected_topics=["quantum", "computing", "recent"],
                expected_tools=["web_search"],
                difficulty="medium",
                category="current_events"
            ),
            TestCase(
                id="basic_004",
                query="How does climate change affect biodiversity?",
                expected_topics=["climate", "biodiversity", "environment"],
                expected_tools=["knowledge_base", "web_search"],
                difficulty="medium",
                category="scientific"
            ),
            TestCase(
                id="basic_005",
                query="What happened in the latest SpaceX launch?",
                expected_topics=["SpaceX", "launch", "space"],
                expected_tools=["web_search"],
                difficulty="easy",
                category="current_events"
            )
        ]
        
        self.test_cases.extend(basic_tests)
        return basic_tests
    
    def generate_complex_tests(self) -> List[TestCase]:
        """Generate complex test cases"""
        complex_tests = [
            TestCase(
                id="complex_001",
                query="Compare the economic impacts of renewable energy adoption versus traditional fossil fuels in developing countries",
                expected_topics=["renewable energy", "economics", "developing countries"],
                expected_tools=["knowledge_base", "web_search"],
                difficulty="hard",
                category="comparative_analysis"
            ),
            TestCase(
                id="complex_002",
                query="What are the ethical implications of AI in healthcare decision-making?",
                expected_topics=["AI ethics", "healthcare", "decision making"],
                expected_tools=["knowledge_base"],
                difficulty="hard",
                category="ethics"
            ),
            TestCase(
                id="complex_003",
                query="Analyze the relationship between social media usage and mental health in teenagers",
                expected_topics=["social media", "mental health", "teenagers"],
                expected_tools=["knowledge_base", "web_search"],
                difficulty="hard",
                category="social_research"
            )
        ]
        
        self.test_cases.extend(complex_tests)
        return complex_tests
    
    def generate_edge_cases(self) -> List[TestCase]:
        """Generate edge case test scenarios"""
        edge_cases = [
            TestCase(
                id="edge_001",
                query="",
                expected_topics=[],
                expected_tools=[],
                difficulty="edge",
                category="empty_query"
            ),
            TestCase(
                id="edge_002",
                query="asdjfkl asdlkfj aslkdfj",
                expected_topics=[],
                expected_tools=["knowledge_base"],
                difficulty="edge",
                category="nonsense_query"
            ),
            TestCase(
                id="edge_003",
                query="Tell me everything about everything",
                expected_topics=["general"],
                expected_tools=["knowledge_base"],
                difficulty="edge",
                category="overly_broad"
            ),
            TestCase(
                id="edge_004",
                query="What is the exact temperature in New York City at this very moment?",
                expected_topics=["weather", "current"],
                expected_tools=["web_search"],
                difficulty="edge",
                category="impossible_precision"
            )
        ]
        
        self.test_cases.extend(edge_cases)
        return edge_cases
    
    def get_all_test_cases(self) -> List[TestCase]:
        """Get all generated test cases"""
        if not self.test_cases:
            self.generate_basic_tests()
            self.generate_complex_tests()
            self.generate_edge_cases()
        
        return self.test_cases
    
    def save_test_cases(self, filepath: str):
        """Save test cases to JSON file"""
        test_cases_dict = [asdict(tc) for tc in self.test_cases]
        with open(filepath, 'w') as f:
            json.dump(test_cases_dict, f, indent=2)
        logger.info(f"Saved {len(self.test_cases)} test cases to {filepath}")

class AgentEvaluator:
    """Evaluates agent performance on test cases"""
    
    def __init__(self, agent):
        self.agent = agent
        self.results = []
    
    def _calculate_tool_selection_accuracy(self, used_tools: List[str], expected_tools: List[str]) -> float:
        """Calculate accuracy of tool selection"""
        if not expected_tools:
            return 1.0 if not used_tools else 0.5
        
        if not used_tools:
            return 0.0
        
        # Calculate intersection over union
        used_set = set(used_tools)
        expected_set = set(expected_tools)
        
        intersection = len(used_set & expected_set)
        union = len(used_set | expected_set)
        
        return intersection / union if union > 0 else 0.0
    
    def _calculate_relevance_score(self, response: str, expected_topics: List[str]) -> float:
        """Calculate relevance of response to expected topics"""
        if not expected_topics:
            return 0.8  # Default score for cases without specific topics
        
        response_lower = response.lower()
        topic_matches = 0
        
        for topic in expected_topics:
            if topic.lower() in response_lower:
                topic_matches += 1
        
        return topic_matches / len(expected_topics) if expected_topics else 0.0
    
    def _calculate_response_quality(self, response: str) -> float:
        """Calculate overall response quality"""
        # Simple heuristics for response quality
        if len(response) < 10:
            return 0.2
        elif len(response) < 50:
            return 0.5
        elif len(response) > 1000:
            return 0.7  # Very long responses might be verbose
        else:
            return 0.8
    
    async def _evaluate_single_test(self, test_case: TestCase) -> TestResult:
        """Evaluate agent on a single test case"""
        logger.info(f"Evaluating test case: {test_case.id}")
        
        start_time = time.time()
        
        try:
            # Get agent response
            agent_response = await self.agent.process_query(test_case.query)
            response_time = time.time() - start_time
            
            # Extract tools used from agent response
            tools_used = []
            if hasattr(agent_response, 'reasoning') and "Used tools:" in agent_response.reasoning:
                tools_text = agent_response.reasoning.split("Used tools:")[1].split(".")[0]
                tools_used = [tool.strip() for tool in tools_text.split(",")]
            
            # Calculate metrics
            tool_accuracy = self._calculate_tool_selection_accuracy(tools_used, test_case.expected_tools)
            relevance = self._calculate_relevance_score(agent_response.content, test_case.expected_topics)
            quality = self._calculate_response_quality(agent_response.content)
            
            metrics = {
                "tool_selection_accuracy": tool_accuracy,
                "relevance": relevance,
                "quality": quality,
                "response_time": response_time
            }
            
            # Determine if test passed (simple criteria)
            passed = (
                tool_accuracy >= 0.5 and 
                relevance >= 0.3 and 
                quality >= 0.5 and 
                response_time < 30.0
            )
            
            result = TestResult(
                test_case_id=test_case.id,
                query=test_case.query,
                response_content=agent_response.content,
                tools_used=tools_used,
                expected_tools=test_case.expected_tools,
                response_time=response_time,
                confidence=agent_response.confidence,
                sources=agent_response.sources,
                metrics=metrics,
                passed=passed
            )
            
        except Exception as e:
            logger.error(f"Error evaluating test case {test_case.id}: {e}")
            result = TestResult(
                test_case_id=test_case.id,
                query=test_case.query,
                response_content=f"Error: {str(e)}",
                tools_used=[],
                expected_tools=test_case.expected_tools,
                response_time=time.time() - start_time,
                confidence=0.0,
                sources=[],
                metrics={"error": 1.0},
                passed=False
            )
        
        return result
    
    async def evaluate_agent(self, test_cases: List[TestCase]) -> List[TestResult]:
        """Evaluate agent on multiple test cases"""
        logger.info(f"Starting evaluation on {len(test_cases)} test cases")
        
        results = []
        for test_case in test_cases:
            result = await self._evaluate_single_test(test_case)
            results.append(result)
            
            # Small delay between tests
            await asyncio.sleep(0.1)
        
        self.results = results
        logger.info(f"Evaluation completed. {sum(1 for r in results if r.passed)}/{len(results)} tests passed")
        
        return results
    
    def calculate_overall_metrics(self, results: List[TestResult]) -> EvaluationMetrics:
        """Calculate overall evaluation metrics"""
        if not results:
            return EvaluationMetrics(0, 0, 0, 0, 0, 0)
        
        # Filter out error results
        valid_results = [r for r in results if "error" not in r.metrics]
        
        if not valid_results:
            return EvaluationMetrics(0, 0, 0, 0, 0, 0)
        
        # Calculate averages
        accuracy = sum(1 for r in valid_results if r.passed) / len(valid_results)
        relevance = sum(r.metrics.get("relevance", 0) for r in valid_results) / len(valid_results)
        tool_accuracy = sum(r.metrics.get("tool_selection_accuracy", 0) for r in valid_results) / len(valid_results)
        avg_response_time = sum(r.response_time for r in valid_results) / len(valid_results)
        
        # Calculate confidence calibration (simplified)
        confidence_calibration = sum(r.confidence for r in valid_results) / len(valid_results)
        
        # Calculate source citation rate
        source_citation_rate = sum(1 for r in valid_results if r.sources) / len(valid_results)
        
        return EvaluationMetrics(
            accuracy=accuracy,
            relevance=relevance,
            tool_selection_accuracy=tool_accuracy,
            response_time=avg_response_time,
            confidence_calibration=confidence_calibration,
            source_citation_rate=source_citation_rate
        )
    
    def generate_report(self, results: List[TestResult], output_path: str):
        """Generate evaluation report"""
        metrics = self.calculate_overall_metrics(results)
        
        report = {
            "evaluation_summary": asdict(metrics),
            "test_results": [asdict(result) for result in results],
            "timestamp": datetime.now().isoformat(),
            "total_tests": len(results),
            "passed_tests": sum(1 for r in results if r.passed),
            "failed_tests": sum(1 for r in results if not r.passed)
        }
        
        # Save to JSON
        with open(output_path, 'w') as f:
            json.dump(report, f, indent=2)
        
        logger.info(f"Evaluation report saved to {output_path}")
        
        # Print summary
        print("\n" + "="*50)
        print("EVALUATION SUMMARY")
        print("="*50)
        print(f"Total Tests: {len(results)}")
        print(f"Passed: {sum(1 for r in results if r.passed)}")
        print(f"Failed: {sum(1 for r in results if not r.passed)}")
        print(f"Overall Accuracy: {metrics.accuracy:.2%}")
        print(f"Average Relevance: {metrics.relevance:.2%}")
        print(f"Tool Selection Accuracy: {metrics.tool_selection_accuracy:.2%}")
        print(f"Average Response Time: {metrics.response_time:.2f}s")
        print(f"Source Citation Rate: {metrics.source_citation_rate:.2%}")
        print("="*50)
