"""
Simple short-term memory manager for the Stock Market Information Assistant.
Stores and trims conversation history to avoid overflowing context.
"""
MAX_MEMORY = 10  # only keep last 5 exchanges

conversation_memory = []


def add_to_memory(user_message: str, bot_response: str) -> None:
    """
    Add a new pair of user and bot messages to memory.
    
    Args:
        user_message: The user's message to store
        bot_response: The bot's response to store
        
    Raises:
        ValueError: If either message is empty or None
    """
    global conversation_memory
    
    # Validate inputs
    if not user_message or not isinstance(user_message, str):
        raise ValueError("user_message must be a non-empty string")
    if not bot_response or not isinstance(bot_response, str):
        raise ValueError("bot_response must be a non-empty string")
    
    # Add the conversation pair
    conversation_memory.append((user_message.strip(), bot_response.strip()))
    
    # Trim memory to avoid exceeding the context limit
    if len(conversation_memory) > MAX_MEMORY:
        conversation_memory = conversation_memory[-MAX_MEMORY:]


def get_recent_memory() -> str:
    """
    Return the last few conversation turns as formatted text.
    
    Returns:
        A string containing formatted conversation history, or empty string if no history exists
    """
    if not conversation_memory:
        return ""
    
    return "\n".join(
        [f"User: {u}\nBot: {b}" for u, b in conversation_memory[-MAX_MEMORY:]]
    )


def clear_memory() -> None:
    """Clear all conversation history."""
    global conversation_memory
    conversation_memory = []