# BRIEFLY-AI-Agent-for-Company-Briefings

An intelligent AI-powered research assistant that provides detailed company briefings and analysis using advanced language models and custom tools. The chatbot can analyze companies, provide insights on products, partnerships, and recent developments.

## Features

- 🤖 **AI-Powered Analysis**: Uses Hugging Face language models for intelligent responses
- 🏢 **Company Research**: Comprehensive company briefings with industry insights
- 🔍 **Multi-Tool Integration**: Custom tools for data retrieval and analysis
- 🛡️ **Security Features**: Built-in prompt injection filtering and output validation
- 📊 **Template System**: Customizable briefing templates using Jinja2
- 🌐 **Translation Support**: Multi-language support via Google Translate
- 📈 **Market Analysis**: Insights on products, partnerships, and market trends

## Project Structure

```
assistant-chatbot/
├── src/                      # Main source code
│   ├── agent.py             # Main agent implementation
│   ├── agent_utils.py       # Agent utility functions
│   ├── prompt.py            # Prompt templates and configurations
│   ├── security_filter.py   # Security and validation filters
│   ├── template_content.py  # Template content management
│   └── tools.py             # Custom tools and integrations
├── data/                    # Data files and datasets
│   ├── company_database.json # Company information database
│   ├── dataset_generator_openai.py # Dataset generation scripts
│   └── prompt.py            # Data-related prompts
├── briefing_templates/      # Jinja2 templates for reports
│   └── default.j2          # Default briefing template
├── requirements.txt         # Python dependencies
├── test.py                 # Test script and CLI interface
└── README.md               # This file
```

## Prerequisites

- **Python**: 3.8 or higher
- **Operating System**: Linux, macOS, or Windows
- **API Keys**: Hugging Face API token (required)
- **Internet Connection**: Required for API calls and external data

## Installation

### 1. Clone the Repository (Not pubblic)

```bash
git clone https://github.com/Singh8899/assistant-chatbot.git
cd assistant-chatbot
```

### 2. Create Virtual Environment (Recommended)

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Linux/macOS:
source venv/bin/activate

# On Windows:
venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Environment Configuration

Create a `.env` file in the root directory with the following variables:

```env
# Required: Hugging Face Configuration
HUGGINGFACE_REPO_ID=your_model_repo_id
HUGGINGFACEHUB_API_TOKEN=your_huggingface_api_token

# Optional: Model Parameters
LLM_TEMPERATURE=0.7
LLM_TOP_P=0.9
HUGGINGFACE_PROVIDER=nebius

# Optional: OpenAI (if using OpenAI features)
OPENAI_API_KEY=your_openai_api_key
```

#### Getting API Keys:

1. **Hugging Face API Token**:
   - Visit [Hugging Face Settings](https://huggingface.co/settings/tokens)
   - Create a new token with read permissions
   - Copy the token to your `.env` file

2. **OpenAI API Key** (optional):
   - Visit [OpenAI API Keys](https://platform.openai.com/api-keys)
   - Create a new secret key
   - Copy the key to your `.env` file

## Usage

### Command Line Interface

Run the chatbot with a default query:

```bash
python test.py
```

Run with a custom query:

```bash
python test.py -q "Provide analysis on Microsoft's recent partnerships"
```

### Examples

```bash
# Company analysis
python test.py -q "Give me a detailed briefing on OpenAI"

# Product research
python test.py -q "What are Google's main AI products and services?"

# Market analysis
python test.py -q "Analyze recent partnerships in the tech industry"
```

### Programmatic Usage

```python
from src.agent import run_agent_query

# Simple query
run_agent_query("Analyze Tesla's business model")
# this will save the report in output folder
```

## Configuration

### Model Configuration

Edit the model parameters in your `.env` file:

- `LLM_TEMPERATURE`: Controls randomness (0.0-1.0, default: 0.7)
- `LLM_TOP_P`: Controls nucleus sampling (0.0-1.0, default: 0.9)
- `HUGGINGFACE_PROVIDER`: API provider (default: "nebius")

### Custom Templates

Modify or create new briefing templates in the `briefing_templates/` directory:

```jinja
# briefing_templates/custom.j2
# Your custom template here
{{ company_name }} Analysis
Industry: {{ company_industry }}
```

### Security Settings

The chatbot includes built-in security features:

- **Prompt Injection Filter**: Prevents malicious prompt injections
- **Output Validator**: Validates and sanitizes responses
- **Content Filtering**: Ensures appropriate content generation

## Dependencies

Core dependencies (automatically installed via requirements.txt):

- `langchain==0.3.27` - LLM framework and orchestration
- `langchain-huggingface==0.3.1` - Hugging Face integration
- `langgraph==0.6.7` - Graph-based agent workflows
- `openai==1.107.1` - OpenAI API integration
- `googletrans==4.0.2` - Translation services
- `Jinja2==3.1.6` - Template engine
- `python-dotenv==1.1.1` - Environment variable management


## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
