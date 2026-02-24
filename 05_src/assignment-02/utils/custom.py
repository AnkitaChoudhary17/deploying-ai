"""
Custom OpenAI Tools Module for the Stock Market Information Assistant.
Uses OpenAI API to explain finance and tech concepts in simple, beginner-friendly language.
"""
from typing import Optional, Dict
from openai import OpenAI
import sys
from pathlib import Path

# Import configuration from config.py
sys.path.insert(0, str(Path(__file__).parent.parent))
from config import OPENAI_API_KEY

# Initialize OpenAI client
client = OpenAI(api_key=OPENAI_API_KEY)

# Cache for repeated explanations to reduce API calls
explanation_cache: Dict[str, str] = {}


def explain_simple(concept: str) -> str:
    """
    Explain a finance or tech concept in plain, beginner-friendly language.
    Uses caching to avoid repeated API calls for the same concept.
    
    Args:
        concept: The financial or technical concept to explain
    
    Returns:
        A simple, easy-to-understand explanation (under 80 words)
    
    Raises:
        ValueError: If concept is empty or invalid
    """
    if not concept or not isinstance(concept, str):
        raise ValueError("concept must be a non-empty string")
    
    concept = concept.strip()
    
    # Check cache first
    if concept in explanation_cache:
        return explanation_cache[concept]
    
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a patient financial educator who explains "
                        "complex ideas simply, using short sentences and everyday language. "
                        "Avoid jargon and technical terms. Be concise and beginner-friendly."
                    ),
                },
                {
                    "role": "user",
                    "content": f"Explain '{concept}' in simple, clear terms. Keep it under 80 words."
                },
            ],
            temperature=0.7,
            max_tokens=150,
        )
        
        explanation = response.choices[0].message.content.strip()
        # Cache the result
        explanation_cache[concept] = explanation
        return explanation
    
    except Exception as e:
        return f"❌ Error explaining '{concept}': {str(e)}"


def explain_with_examples(concept: str) -> str:
    """
    Explain a financial concept with real-world examples.
    
    Args:
        concept: The financial concept to explain
    
    Returns:
        An explanation with practical examples
    
    Raises:
        ValueError: If concept is empty or invalid
    """
    if not concept or not isinstance(concept, str):
        raise ValueError("concept must be a non-empty string")
    
    concept = concept.strip()
    
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a financial educator. Explain concepts clearly "
                        "with 2-3 real-world examples that beginners can relate to."
                    ),
                },
                {
                    "role": "user",
                    "content": (
                        f"Explain '{concept}' with simple, real-world examples. "
                        f"Keep total response under 200 words."
                    )
                },
            ],
            temperature=0.7,
            max_tokens=300,
        )
        
        return response.choices[0].message.content.strip()
    
    except Exception as e:
        return f"❌ Error creating examples for '{concept}': {str(e)}"


def compare_concepts(concept1: str, concept2: str) -> str:
    """
    Compare two financial concepts to highlight differences and similarities.
    
    Args:
        concept1: First concept to compare
        concept2: Second concept to compare
    
    Returns:
        A comparison of the two concepts
    
    Raises:
        ValueError: If either concept is empty or invalid
    """
    if not concept1 or not concept2:
        raise ValueError("Both concepts must be non-empty strings")
    
    concept1, concept2 = concept1.strip(), concept2.strip()
    
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a financial educator. Compare financial concepts "
                        "by explaining their differences, similarities, and when to use each."
                    ),
                },
                {
                    "role": "user",
                    "content": (
                        f"Compare '{concept1}' and '{concept2}'. "
                        f"Explain: 1) Key differences, 2) When to use each, "
                        f"3) Which is better for beginners. Keep it under 200 words."
                    )
                },
            ],
            temperature=0.7,
            max_tokens=300,
        )
        
        return response.choices[0].message.content.strip()
    
    except Exception as e:
        return f"❌ Error comparing concepts: {str(e)}"


def investment_advice_explainer(scenario: str) -> str:
    """
    Explain investment strategies or advice for a specific scenario.
    
    Args:
        scenario: An investment scenario or question (e.g., "I have $1000 to invest")
    
    Returns:
        Educational explanation of relevant strategies
    
    Raises:
        ValueError: If scenario is empty or invalid
    """
    if not scenario or not isinstance(scenario, str):
        raise ValueError("scenario must be a non-empty string")
    
    scenario = scenario.strip()
    
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a financial advisor and educator. Provide beginner-friendly "
                        "educational explanations of investment strategies. "
                        "DISCLAIMER: This is educational content, not financial advice."
                    ),
                },
                {
                    "role": "user",
                    "content": (
                        f"Scenario: {scenario}\n\n"
                        f"Explain the strategy options available, their pros/cons, "
                        f"and what a beginner should know. Keep under 250 words. "
                        f"Start with: 'Educational Overview:'"
                    )
                },
            ],
            temperature=0.7,
            max_tokens=350,
        )
        
        return response.choices[0].message.content.strip()
    
    except Exception as e:
        return f"❌ Error analyzing scenario: {str(e)}"


def risk_assessment_explainer(investment_type: str) -> str:
    """
    Explain the risk profile of different investment types.
    
    Args:
        investment_type: Type of investment to assess (e.g., "penny stocks", "bonds")
    
    Returns:
        Explanation of risk factors
    
    Raises:
        ValueError: If investment_type is empty or invalid
    """
    if not investment_type or not isinstance(investment_type, str):
        raise ValueError("investment_type must be a non-empty string")
    
    investment_type = investment_type.strip()
    
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a financial educator explaining investment risks. "
                        "Be clear, honest, and beginner-friendly about potential downsides."
                    ),
                },
                {
                    "role": "user",
                    "content": (
                        f"Explain the risks of {investment_type}. Cover:\n"
                        f"1) Main risks\n"
                        f"2) Who should consider it\n"
                        f"3) Risk mitigation strategies\n"
                        f"Keep under 200 words."
                    )
                },
            ],
            temperature=0.7,
            max_tokens=300,
        )
        
        return response.choices[0].message.content.strip()
    
    except Exception as e:
        return f"❌ Error assessing risks: {str(e)}"


def clear_cache() -> None:
    """Clear the explanation cache to save memory or refresh explanations."""
    global explanation_cache
    explanation_cache.clear()