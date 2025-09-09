# Research Assistant Chatbot

A sophisticated AI-powered research assistant built with **Meta-Llama/Llama-3.1-8B-Instruct** and **LangChain**, featuring an agentic workflow with tool selection, memory management, and comprehensive evaluation framework.

## 🚀 Features

### Core Agent Capabilities
- **Intelligent Tool Selection**: Automatically selects appropriate research tools based on query analysis
- **Multi-Tool Integration**: Web search and knowledge base access
- **Conversation Memory**: Maintains context across multiple interactions
- **Source Citation**: Tracks and cites information sources
- **Confidence Scoring**: Provides confidence estimates for responses

### Evaluation Framework
- **Synthetic Test Data Generation**: Creates diverse test scenarios
- **Comprehensive Metrics**: Accuracy, relevance, tool selection, response time
- **Performance Analytics**: Detailed evaluation reports
- **Edge Case Testing**: Handles unusual and challenging queries

### Technical Implementation
- **LLM Integration**: Hugging Face API with Meta-Llama/Llama-3.1-8B-Instruct
- **Async Processing**: Non-blocking tool execution
- **Modular Design**: Extensible tool and evaluation frameworks
- **Error Handling**: Graceful degradation and fallback mechanisms

## 📋 Requirements

- Python 3.8+
- Hugging Face API token
- Dependencies listed in `requirements.txt`

## 🛠️ Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/Singh8899/assistant-chatbot.git
   cd assistant-chatbot
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env and add your HuggingFace API token
   ```

4. **Test the installation**
   ```bash
   python test_agent.py
   ```

## 🎯 Usage

### Interactive Chat Mode
Start an interactive conversation with the research assistant:

```bash
python src/cli.py --interactive
```

**Commands:**
- `quit` or `exit`: Exit the chat
- `clear`: Clear conversation history
- `history`: View recent conversation history

### Single Query Mode
Process a single query:

```bash
python src/cli.py --query "What is artificial intelligence?"
```

### Evaluation Mode
Run comprehensive evaluation:

```bash
python src/cli.py --evaluate
```

This will:
- Generate synthetic test data
- Evaluate agent performance
- Create detailed reports in `evaluation_results/`

### Custom Model Configuration
Use a different model or token:

```bash
python src/cli.py --model "meta-llama/Llama-3.1-70B-Instruct" --token "your_hf_token" --interactive
```

## 🏗️ Architecture

### Agent Framework (`src/agent.py`)

```python
class ResearchAgent:
    - Tool selection logic
    - LLM integration (HuggingFace)
    - Memory management
    - Response generation
    - Source tracking
```

### Available Tools
1. **WebSearchTool**: Simulated web search for current information
2. **KnowledgeBaseTool**: Access to internal knowledge base

### Evaluation System (`src/evaluation.py`)

```python
class AgentEvaluator:
    - Test case execution
    - Metrics calculation
    - Performance analysis
    - Report generation
```

## 📊 Evaluation Metrics

| Metric | Description |
|--------|-------------|
| **Accuracy** | Percentage of tests that meet passing criteria |
| **Relevance** | How well responses match expected topics |
| **Tool Selection Accuracy** | Correctness of tool choice for queries |
| **Response Time** | Average time to generate responses |
| **Confidence Calibration** | Alignment of confidence scores with accuracy |
| **Source Citation Rate** | Percentage of responses with cited sources |

## 🧪 Test Categories

### Basic Tests
- Definition queries
- Explanation requests
- Current events
- Scientific questions

### Complex Tests
- Comparative analysis
- Ethical implications
- Multi-domain research

### Edge Cases
- Empty queries
- Nonsense input
- Overly broad requests
- Impossible precision demands

## 📈 Sample Evaluation Report

```json
{
  "evaluation_summary": {
    "accuracy": 0.85,
    "relevance": 0.78,
    "tool_selection_accuracy": 0.92,
    "response_time": 2.3,
    "confidence_calibration": 0.81,
    "source_citation_rate": 0.75
  },
  "total_tests": 12,
  "passed_tests": 10,
  "failed_tests": 2
}
```

## 🔧 Configuration

### Environment Variables (.env)
```bash
# Hugging Face Configuration
HF_API_TOKEN=your_huggingface_api_token_here
LLM_MODEL_NAME=meta-llama/Llama-3.1-8B-Instruct
LLM_MAX_TOKENS=2048
LLM_TEMPERATURE=0.7
LLM_TOP_P=0.9

# Agent Configuration
MAX_ITERATIONS=5
MEMORY_SIZE=10

# Evaluation Configuration
TEST_BATCH_SIZE=5
EVALUATION_TIMEOUT=30
```

## 🚦 Development Status

### ✅ Completed Features
- [x] Basic agent framework
- [x] Tool selection logic
- [x] LLM integration (HuggingFace)
- [x] Memory management
- [x] Evaluation framework
- [x] Test data generation
- [x] CLI interface
- [x] Comprehensive documentation

### 🔄 Future Enhancements
- [ ] Real web search API integration
- [ ] Vector database for knowledge base
- [ ] Multi-turn conversation optimization
- [ ] Advanced reasoning chains
- [ ] Custom tool creation interface

## 🐛 Troubleshooting

### Common Issues

1. **Import Errors**
   ```bash
   pip install -r requirements.txt
   ```

2. **HuggingFace API Issues**
   - Verify API token in `.env`
   - Check model availability
   - Ensure sufficient API quota

3. **Mock LLM Fallback**
   - Agent uses mock responses when HuggingFace API is unavailable
   - Useful for testing without API access

## 📝 Example Interactions

### Research Query
```
You: What are the latest developments in quantum computing?
Assistant: Based on my research using web search tools, recent quantum computing developments include significant advances in error correction, quantum supremacy demonstrations, and commercial applications. IBM, Google, and other companies have made progress in quantum processors with improved coherence times...

Confidence: 0.85
Sources: https://example.com/research/quantum-computing
Tools used: web_search
```

### Definition Query
```
You: What is machine learning?
Assistant: Machine learning is a subset of artificial intelligence that enables computers to learn and improve from experience without being explicitly programmed for every task...

Confidence: 0.92
Sources: internal_knowledge_base
Tools used: knowledge_base
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Make your changes and add tests
4. Commit your changes: `git commit -am 'Add feature'`
5. Push to the branch: `git push origin feature-name`
6. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Meta AI** for the Llama-3.1-8B-Instruct model
- **LangChain** for the excellent framework
- **Hugging Face** for model hosting and API
- **Resaro** for the take-home assignment opportunity

---

**Built with ❤️ for AI-powered research assistance**