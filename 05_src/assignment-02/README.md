# 📈 Stock Market Information Assistant

An intelligent conversational AI chatbot designed to educate and inform users about investing, personal finance, and stock market fundamentals. This project combines OpenAI's GPT-4o-mini, semantic search with FAISS, and real-time market data from Alpha Vantage API to create an interactive financial education assistant.

## ⚠️ Important Disclaimer

**This is educational content only.** This assistant is NOT a financial advisor and does NOT provide personalized investment recommendations. Always consult with a licensed financial professional before making investment decisions. Past performance does not guarantee future results.

## 🎯 Features

### 1. **Real-Time Stock Information**
- Fetch live stock prices using Alpha Vantage API
- Get intraday trading data at multiple intervals (1min, 5min, 15min, 30min, 60min)
- Access company information for 50+ major stocks
- Smart caching to optimize API calls

### 2. **Semantic Search**
- Uses OpenAI embeddings with FAISS vector database
- Intelligent document search for financial concepts
- Context-aware responses based on your questions
- Pre-loaded knowledge base of investment and market information

### 3. **Educational Explanations**
- OpenAI-powered explanations for financial concepts
- Beginner-friendly explanations of complex topics
- Investment strategy comparisons
- Risk assessment and scenario analysis

### 4. **Conversation Memory**
- Maintains context across multiple exchanges
- Stores last 10 conversation turns
- Provides personalized, context-aware responses
- Memory management utilities

### 5. **Content Guardrails**
- Automatic filtering of off-topic queries
- Focused on finance and investing topics only
- Safe and educational environment

### 6. **Interactive Web Interface**
- Gradio-based chat interface
- Example questions to get started
- Real-time conversation history
- Clean, user-friendly design

## 🛠️ Technology Stack

- **OpenAI GPT-4o-mini** - Conversational AI and natural language understanding
- **LangChain** - Semantic search and embeddings framework
- **FAISS** - Facebook AI Similarity Search for vector storage
- **Alpha Vantage API** - Real-time and historical stock market data
- **Gradio** - Interactive web UI for chat interface
- **Python-dotenv** - Secure environment variable management

## 📁 Project Structure

```
assign-02/
├── main.ipynb              # Main Jupyter notebook with demonstrations
├── config.py               # Configuration and environment setup
├── .env                    # Environment variables (API keys)
├── README.md               # This file
└── utils/                  # Core utility modules
    ├── api.py              # Alpha Vantage API integration
    ├── custom.py           # Custom OpenAI-powered explanations
    ├── mcp.py              # MCP finance service (async market data)
    ├── memory.py           # Conversation memory management
    ├── semantic.py         # Semantic search with FAISS
    └── system_prompt.py    # System prompts and instructions
```

## 🚀 Getting Started

### Prerequisites

- Python 3.8 or higher
- OpenAI API key
- Alpha Vantage API key (free tier available)

### Installation

1. **Clone or download the project**
   ```bash
   cd assign-02
   ```

2. **Install required packages**
   ```bash
   pip install openai python-dotenv gradio requests langchain langchain-openai langchain-community faiss-cpu
   ```

3. **Set up environment variables**
   
   Create a `.env` file in the project root:
   ```bash
   cp .env.example .env
   ```
   
   Edit `.env` and add your API keys:
   ```dotenv
   OPENAI_API_KEY="your-openai-api-key-here"
   ALPHAVANTAGE_API_KEY="your-alphavantage-api-key-here"
   DEBUG=False
   LOG_LEVEL=INFO
   ```

4. **Get your API keys**
   - **OpenAI**: Sign up at [platform.openai.com](https://platform.openai.com)
   - **Alpha Vantage**: Get free API key at [alphavantage.co](https://www.alphavantage.co/support/#api-key)

### Running the Assistant

#### Option 1: Jupyter Notebook (Recommended)

1. Launch Jupyter:
   ```bash
   jupyter notebook main.ipynb
   ```

2. Run the cells sequentially:
   - **Cell 1**: Imports and setup
   - **Cell 2-7**: Individual service demonstrations
   - **Cell 8-14**: Feature demonstrations (guardrails, memory, routing)
   - **Cell 15**: Launch interactive Gradio interface

#### Option 2: Python Scripts

Run individual utility modules for testing:
```bash
# Test semantic search
python utils/semantic.py

# Test API integration
python utils/api.py

# Test custom explanations
python utils/custom.py
```

## 📚 Usage Examples

### Ask About Financial Concepts
```
User: "What is diversification?"
Bot: Diversification is an investment strategy that spreads your investments across different assets to reduce risk...
```

### Get Stock Information
```
User: "Tell me about Apple stock price"
Bot: 📈 AAPL is trading at $175.50, change: +2.15 (+1.24%)
```

### Learn Investment Strategies
```
User: "Explain P/E ratio in simple terms"
Bot: The P/E (Price-to-Earnings) ratio compares a company's stock price to its earnings per share...
```

## 🎯 Key Components

### Service Modules

**`utils/api.py`** - Alpha Vantage Integration
- Stock price queries
- Intraday data retrieval
- Company information
- Intelligent caching

**`utils/semantic.py`** - Semantic Search
- FAISS vector database
- OpenAI embeddings
- Document similarity search
- Knowledge base management

**`utils/custom.py`** - Educational Content
- GPT-powered explanations
- Concept comparisons
- Investment advice formatting
- Risk assessment

**`utils/memory.py`** - Conversation Management
- Turn-by-turn memory storage
- Context retrieval
- Memory size management

**`utils/mcp.py`** - Market Data (Optional)
- Async external data connections
- Market summaries
- Sector performance

**`utils/system_prompt.py`** - System Configuration
- Bot personality and behavior
- Response formatting guidelines
- Educational focus settings

## 🛡️ Content Filtering

The assistant automatically filters out non-financial topics:
- Animals/pets
- Entertainment/celebrities
- Astrology/horoscopes
- Politics/religion

This keeps conversations focused and educational.

## 🧪 Demonstrations in Notebook

The `main.ipynb` notebook includes comprehensive demonstrations:

1. **Demo 1A**: Semantic Search Service
2. **Demo 1B**: Custom Explanations Service
3. **Demo 1C**: AlphaVantage API Service
4. **Demo 2**: Guardrails & Content Filtering
5. **Demo 3**: Conversation Memory Management
6. **Demo 4**: Chat Routing Logic
7. **Demo 5**: Interactive Gradio Interface

## 📝 Notes

- **API Rate Limits**: Alpha Vantage free tier has 5 calls/minute, 500 calls/day
- **Caching**: API responses are cached for 60 minutes to reduce API usage
- **Memory**: Conversation history limited to last 10 exchanges
- **Semantic Search**: Pre-loaded with financial education documents

## 🔧 Troubleshooting

**Issue**: "OPENAI_API_KEY not found"
- **Solution**: Ensure `.env` file exists with valid API key

**Issue**: "Could not retrieve stock data"
- **Solution**: Check Alpha Vantage API rate limits or verify ticker symbol

**Issue**: "Semantic search module not available"
- **Solution**: Install langchain packages: `pip install langchain langchain-openai langchain-community faiss-cpu`

**Issue**: Gradio interface not launching
- **Solution**: Ensure gradio is installed: `pip install gradio`

## 📄 License

This project is for educational purposes. Please ensure compliance with API provider terms of service when using OpenAI and Alpha Vantage APIs.

## 🤝 Contributing

This is an educational project. Feel free to extend it with:
- Additional data sources
- More sophisticated analysis
- Enhanced UI features
- Additional financial metrics

## 📧 Support

For questions about the project structure or implementation, refer to the inline documentation in each module.

---

*Remember: This is for learning only. Always consult licensed financial professionals for investment decisions.*
