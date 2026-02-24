"""
Alpha Vantage API Integration Module for Stock Market Information Assistant.
Features: Live stock prices, intraday data, company info, caching, error handling.
"""

import os
import requests
from dotenv import load_dotenv
from typing import Optional, Dict, Tuple
from datetime import datetime, timedelta

# Load environment variables
load_dotenv()
ALPHAVANTAGE_API_KEY = os.getenv("ALPHAVANTAGE_API_KEY")

# Extended mapping of company names to stock tickers
COMPANY_SYMBOLS: Dict[str, str] = {
    # Technology
    "microsoft": "MSFT",
    "apple": "AAPL",
    "google": "GOOGL",
    "alphabet": "GOOGL",
    "amazon": "AMZN",
    "meta": "META",
    "facebook": "META",
    "tesla": "TSLA",
    "nvidia": "NVDA",
    "intel": "INTC",
    "amd": "AMD",
    "ibm": "IBM",
    
    # Finance
    "jpmorgan": "JPM",
    "goldman": "GS",
    "morgan stanley": "MS",
    "bank of america": "BAC",
    "wells fargo": "WFC",
    
    # Consumer
    "walmart": "WMT",
    "target": "TGT",
    "costco": "COST",
    "mcdonald": "MCD",
    "coca cola": "KO",
    "pepsi": "PEP",
    
    # Energy
    "exxon": "XOM",
    "chevron": "CVX",
    "shell": "SHEL",
    
    # Healthcare
    "pfizer": "PFE",
    "moderna": "MRNA",
    "johnson": "JNJ",
    "merck": "MRK",
    
    # Telecommunications
    "at&t": "T",
    "verizon": "VZ",
}

# Cache for API responses
API_CALL_CACHE: Dict[str, Tuple[str, datetime]] = {}
CACHE_DURATION = timedelta(minutes=60)


def _get_symbol(query: str) -> Optional[str]:
    """
    Identify stock symbol from user query (company name or ticker).
    
    Args:
        query: User's search query
    
    Returns:
        Stock ticker symbol or None if not found
    """
    if not query or not isinstance(query, str):
        return None
    
    query_lower = query.lower().strip()
    
    # Check for exact ticker match
    for ticker in COMPANY_SYMBOLS.values():
        if ticker.lower() == query_lower:
            return ticker
    
    # Check for company name match
    for name, ticker in COMPANY_SYMBOLS.items():
        if name in query_lower:
            return ticker
    
    return None


def get_stock_price(query: str) -> str:
    """
    Fetch live stock price for a company by name or ticker.
    
    Args:
        query: Company name (e.g., "Apple") or stock ticker (e.g., "AAPL")
    
    Returns:
        Formatted string with stock price and daily change
    """
    if not query or not isinstance(query, str):
        return "❌ Invalid query. Please provide a company name or stock ticker."
    
    if not ALPHAVANTAGE_API_KEY:
        return "⚠️ Alpha Vantage API key not configured. Please set ALPHAVANTAGE_API_KEY in .env"
    
    # Check cache first
    cache_key = f"price_{query.lower()}"
    if cache_key in API_CALL_CACHE:
        cached_result, cached_time = API_CALL_CACHE[cache_key]
        if datetime.now() - cached_time < CACHE_DURATION:
            return cached_result
    
    # Identify the symbol
    symbol = _get_symbol(query)
    if not symbol:
        return (
            f"❌ Could not identify stock for '{query}'. "
            f"Try: AAPL, MSFT, GOOGL, or company names like Apple, Microsoft"
        )
    
    try:
        # Call Alpha Vantage API with timeout
        url = f"https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={symbol}&apikey={ALPHAVANTAGE_API_KEY}"
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        # Check for errors
        if "Error Message" in data:
            return f"⚠️ API Error: {data['Error Message']}"
        
        quote = data.get("Global Quote", {})
        if not quote or "05. price" not in quote:
            return f"⚠️ Could not retrieve stock data for {symbol}. Please try again."
        
        price = float(quote["05. price"])
        change = quote.get("09. change", "N/A")
        change_percent = quote.get("10. change percent", "N/A").rstrip("%")
        
        # Format with emoji indicator
        emoji = "📈" if not change_percent.startswith("-") else "📉"
        result = f"{emoji} {symbol} is trading at ${price:.2f}, change: {change} ({change_percent}%)"
        
        # Cache the result
        API_CALL_CACHE[cache_key] = (result, datetime.now())
        return result
    
    except requests.exceptions.Timeout:
        return "⏱️ Request timeout - Alpha Vantage server is slow, please try again."
    except requests.exceptions.RequestException as e:
        return f"❌ Network error: {str(e)}"
    except (KeyError, ValueError) as e:
        return f"❌ Error parsing data: {str(e)}"


def get_intraday_data(query: str, interval: str = "5min") -> str:
    """
    Fetch intraday stock price data at specified intervals.
    
    Args:
        query: Company name or stock ticker
        interval: Time interval (1min, 5min, 15min, 30min, 60min) - default: 5min
    
    Returns:
        Formatted string with latest intraday data
    """
    if not query or not isinstance(query, str):
        return "❌ Invalid query provided."
    
    if interval not in ["1min", "5min", "15min", "30min", "60min"]:
        return f"❌ Invalid interval. Choose from: 1min, 5min, 15min, 30min, 60min"
    
    if not ALPHAVANTAGE_API_KEY:
        return "⚠️ Alpha Vantage API key not configured."
    
    symbol = _get_symbol(query)
    if not symbol:
        return f"❌ Could not identify stock for '{query}'."
    
    try:
        url = (
            f"https://www.alphavantage.co/query?"
            f"function=TIME_SERIES_INTRADAY&symbol={symbol}"
            f"&interval={interval}&apikey={ALPHAVANTAGE_API_KEY}"
        )
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        if "Error Message" in data:
            return f"⚠️ API Error: {data['Error Message']}"
        
        # Get the time series data
        time_series_key = f"Time Series ({interval})"
        if time_series_key not in data:
            return f"⚠️ Could not retrieve intraday data for {symbol}."
        
        time_series = data[time_series_key]
        latest_time = list(time_series.keys())[0]
        latest_data = time_series[latest_time]
        
        return (
            f"📊 {symbol} Intraday ({interval}) - {latest_time}:\n"
            f"Open: ${latest_data['1. open']}, "
            f"High: ${latest_data['2. high']}, "
            f"Low: ${latest_data['3. low']}, "
            f"Close: ${latest_data['4. close']}, "
            f"Volume: {latest_data['5. volume']}"
        )
    
    except Exception as e:
        return f"❌ Error fetching intraday data: {str(e)}"


def get_company_info(query: str) -> str:
    """
    Get available company information for a stock.
    
    Args:
        query: Company name or stock ticker
    
    Returns:
        Formatted string with company information
    """
    if not query or not isinstance(query, str):
        return "❌ Invalid query provided."
    
    symbol = _get_symbol(query)
    if not symbol:
        return f"❌ Could not identify stock for '{query}'."
    
    # Return cached company info (would normally come from database)
    company_info = {
        "AAPL": "Apple Inc. - Technology, Founded 1976",
        "MSFT": "Microsoft Corporation - Technology, Founded 1975",
        "GOOGL": "Alphabet Inc. - Technology, Founded 1998",
        "AMZN": "Amazon.com Inc. - E-commerce/Cloud, Founded 1994",
        "TSLA": "Tesla Inc. - EV/Energy, Founded 2003",
        "NVDA": "NVIDIA Corporation - Semiconductors, Founded 1993",
        "META": "Meta Platforms - Social Media/Tech, Founded 2004",
        "INTC": "Intel Corporation - Semiconductors, Founded 1968",
    }
    
    return f"ℹ️ {symbol}: {company_info.get(symbol, f'Stock ticker: {symbol}')}"


def clear_cache() -> None:
    """Clear the API response cache."""
    global API_CALL_CACHE
    API_CALL_CACHE.clear()

