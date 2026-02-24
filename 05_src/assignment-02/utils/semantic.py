"""
Semantic search module for the Stock Market Information Assistant.
Uses OpenAI embeddings and FAISS for semantic similarity search.
No external Document classes - uses simple dictionaries instead.
"""
from typing import List, Optional, Dict, Tuple
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS

# Import configuration
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))
from config import OPENAI_API_KEY


# Simple Document-like class (replacing langchain.schema.Document)
class Document:
    """Minimal document class for storing text content."""
    _id_counter = 0
    
    def __init__(self, page_content: str, metadata: dict = None):
        self.page_content = page_content
        self.metadata = metadata or {}
        # Auto-generate unique ID for each document
        Document._id_counter += 1
        self.id = str(Document._id_counter)


# Stock Market Information Dataset
STOCK_MARKET_DOCS = [
    Document("The S&P 500 index tracks the performance of 500 largest US companies and is a key indicator of market health."),
    Document("Dividend stocks provide regular income and are popular among long-term investors seeking stable returns."),
    Document("Blue-chip stocks are shares of large, well-established companies with strong market positions and stable earnings."),
    Document("Penny stocks are low-priced, high-risk stocks of smaller companies that can offer high volatility and potential gains."),
    Document("Market capitalization (market cap) is calculated by multiplying stock price by the number of outstanding shares."),
    Document("Price-to-earnings (P/E) ratio compares a company's stock price to its earnings per share, indicating valuation."),
    Document("Technical analysis uses historical price and volume data to predict future price movements."),
    Document("Fundamental analysis evaluates a company's financial health, management, and competitive position."),
    Document("Diversification reduces portfolio risk by spreading investments across different asset classes and sectors."),
    Document("ETFs (Exchange-Traded Funds) allow investors to buy a basket of stocks with a single investment."),
    Document("Volatility measures stock price fluctuations; high volatility means larger price swings and higher risk."),
    Document("The Federal Reserve controls interest rates which directly impact stock valuations and market performance."),
    Document("Earnings per share (EPS) shows how much profit a company makes for each share outstanding."),
    Document("Market trends include bull markets (rising prices) and bear markets (falling prices)."),
    Document("Risk tolerance determines the right investment strategy based on individual financial goals and timeline."),
]

# Initialize embeddings and vector store
try:
    embeddings = OpenAIEmbeddings(model="text-embedding-3-small", api_key=OPENAI_API_KEY)
    vector_store = FAISS.from_documents(STOCK_MARKET_DOCS, embeddings)
except Exception as e:
    raise RuntimeError(f"Failed to initialize semantic search: {e}")


def search_docs(query: str, k: int = 1) -> str:
    """
    Search for relevant stock market information based on semantic similarity.
    
    Args:
        query: The search query
        k: Number of top results to return (default: 1)
    
    Returns:
        A formatted string with the most relevant information
    """
    if not query or not isinstance(query, str):
        return "No relevant information found."
    
    try:
        results = vector_store.similarity_search(query, k=k)
        if not results:
            return "No relevant information found."
        
        if k == 1:
            return f"📊 {results[0].page_content}"
        else:
            formatted_results = "\n".join(
                [f"• {result.page_content}" for result in results]
            )
            return f"📊 Related Information:\n{formatted_results}"
    except Exception as e:
        return f"Error searching documents: {str(e)}"


def search_with_scores(query: str, k: int = 3) -> List[tuple]:
    """
    Search for relevant documents and return results with similarity scores.
    
    Args:
        query: The search query
        k: Number of top results to return (default: 3)
    
    Returns:
        List of tuples containing (document_content, similarity_score)
    """
    if not query or not isinstance(query, str):
        return []
    
    try:
        results = vector_store.similarity_search_with_scores(query, k=k)
        return [(doc.page_content, score) for doc, score in results]
    except Exception as e:
        print(f"Error in similarity search: {e}")
        return []


def add_custom_docs(documents: List[str]) -> None:
    """
    Add custom documents to the vector store.
    
    Args:
        documents: List of document texts to add
    """
    global vector_store
    
    if not documents or not isinstance(documents, list):
        raise ValueError("documents must be a non-empty list")
    
    try:
        doc_objects = [Document(doc) for doc in documents]
        new_docs = FAISS.from_documents(doc_objects, embeddings)
        vector_store.merge_from(new_docs)
    except Exception as e:
        raise RuntimeError(f"Failed to add custom documents: {e}")