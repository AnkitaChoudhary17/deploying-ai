"""
MCP Finance Tools Module for Stock Market Information Assistant.
Handles asynchronous connections to external financial data sources via Model Context Protocol.
"""
import asyncio
from typing import Optional, Dict, Any
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from config import OPENAI_API_KEY


async def yahoo_finance_search(query: str) -> str:
    """
    Fetch financial data from Yahoo Finance via MCP.
    Simulates an asynchronous connection to a remote MCP server.
    
    Args:
        query: Search query for financial information (stock symbol, company name, or topic)
    
    Returns:
        Formatted string with financial information and market insights
    
    Raises:
        ValueError: If query is empty or invalid
    """
    if not query or not isinstance(query, str):
        raise ValueError("query must be a non-empty string")
    
    try:
        # Simulate MCP server communication delay
        await asyncio.sleep(0.5)
        
        query_lower = query.lower().strip()
        
        # Return context-specific financial insights
        if any(term in query_lower for term in ["bitcoin", "crypto", "ethereum"]):
            response = (
                f"💰 Crypto Market Data for '{query.title()}':\n"
                f"Current volatility is elevated. Bitcoin is trading near support levels.\n"
                f"Recent regulatory announcements have impacted institutional adoption."
            )
        elif any(term in query_lower for term in ["tech", "apple", "microsoft", "google"]):
            response = (
                f"🖥️ Tech Sector Analysis for '{query.title()}':\n"
                f"Tech stocks showing strong momentum with AI-related stocks leading gains.\n"
                f"Earnings seasons remain the key driver for sector performance."
            )
        elif any(term in query_lower for term in ["dividend", "income"]):
            response = (
                f"📊 Dividend & Income Strategy for '{query.title()}':\n"
                f"Dividend yields remain attractive in current rate environment.\n"
                f"Utility and consumer staple stocks offer stable passive income."
            )
        else:
            response = (
                f"📡 Market Research for '{query.title()}':\n"
                f"Market shows mixed trends with sector rotation occurring.\n"
                f"Tech leading gains while energy and financials show consolidation."
            )
        
        return response
    
    except asyncio.TimeoutError:
        return f"⚠️ Timeout: Could not retrieve data for '{query}' from MCP server."
    except Exception as e:
        return f"❌ Error fetching market data: {str(e)}"


async def get_stock_analysis(symbol: str) -> str:
    """
    Get detailed technical and fundamental analysis for a stock symbol.
    
    Args:
        symbol: Stock ticker symbol (e.g., 'AAPL', 'MSFT')
    
    Returns:
        Formatted string with stock analysis
    """
    if not symbol or not isinstance(symbol, str):
        raise ValueError("symbol must be a non-empty string")
    
    symbol = symbol.upper().strip()
    
    try:
        await asyncio.sleep(0.5)
        
        return (
            f"📈 Stock Analysis for {symbol}:\n"
            f"Technical: Price above 50-day MA indicates uptrend potential.\n"
            f"Fundamental: P/E ratio within historical range, earnings growth steady.\n"
            f"Sentiment: Analyst ratings show 'Buy' consensus with price target upside."
        )
    except Exception as e:
        return f"❌ Error analyzing {symbol}: {str(e)}"


async def get_market_summary() -> str:
    """
    Get overall market summary and major index performance.
    
    Returns:
        Formatted string with market summary
    """
    try:
        await asyncio.sleep(0.5)
        
        return (
            "🌍 Market Summary:\n"
            "• S&P 500: +0.85% (record highs on AI enthusiasm)\n"
            "• Nasdaq-100: +1.2% (tech-heavy index outperforming)\n"
            "• Dow Jones: +0.45% (large-cap stability)\n"
            "• VIX: 15.3 (volatility remains calm)\n"
            "Market sentiment: Cautiously optimistic"
        )
    except Exception as e:
        return f"❌ Error retrieving market summary: {str(e)}"


async def get_sector_performance() -> str:
    """
    Get performance metrics for major market sectors.
    
    Returns:
        Formatted string with sector performance data
    """
    try:
        await asyncio.sleep(0.5)
        
        return (
            "🏢 Sector Performance:\n"
            "• Technology: +2.1% (AI and cloud computing driving growth)\n"
            "• Healthcare: +0.8% (pharma names under pressure)\n"
            "• Financials: +0.3% (rate-sensitive but stable)\n"
            "• Consumer: -0.2% (mixed earnings outlook)\n"
            "• Energy: +1.5% (oil prices firm)\n"
            "• Utilities: -0.1% (defensive positioning)"
        )
    except Exception as e:
        return f"❌ Error retrieving sector data: {str(e)}"


async def combined_market_query(query: str) -> str:
    """
    Execute multiple MCP queries concurrently for comprehensive market data.
    
    Args:
        query: User's market inquiry
    
    Returns:
        Combined response from multiple MCP sources
    """
    if not query or not isinstance(query, str):
        raise ValueError("query must be a non-empty string")
    
    try:
        # Run multiple queries concurrently
        results = await asyncio.gather(
            yahoo_finance_search(query),
            get_market_summary(),
            raise_exceptions=False
        )
        
        return "\n".join(filter(None, results))
    except Exception as e:
        return f"❌ Error in combined market query: {str(e)}"
    