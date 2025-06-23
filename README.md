# LazyAI

A simple and intuitive wrapper around OpenAI compatible APIs with built-in tool support.

## Features

- Easy-to-use AI assistant with conversation memory
- Simple tool/function calling with decorators
- Automatic conversation history management
- Save and load conversations
- Support for multiple AI providers (OpenAI, Groq, etc.)
- Configurable model parameters

## Installation

```bash
pip install lazyai
```

## Quick Start

```python
from lazyai import Assistant

assistant = Assistant(api_key="your-api-key-here")

# Simple chat
response = assistant.chat("Hello! What's the weather like?")
print(response)

# With tools
@assistant.tool("Get the current weather for a city")
def get_weather(city: str) -> str:
    # Your weather API logic here
    return f"The weather in {city} is sunny and 72°F"

# The AI can now call your function
response = assistant.chat("What's the weather in New York?")
print(response)  # AI will call get_weather("New York") and respond
```

## Advanced Usage

### Using with Groq

```python
from lazyai import Assistant

assistant = Assistant(
    api_key="your-groq-api-key",
    base_url="https://api.groq.com/openai/v1",
    model="llama-3.3-70b-versatile"
)
```

### Multiple Tools

```python
@assistant.tool("Calculate the sum of two numbers")
def add(x: int, y: int) -> int:
    return x + y

@assistant.tool("Get user information from database")
def get_user(user_id: str) -> dict:
    # Your database logic here
    return {"id": user_id, "name": "John Doe"}

response = assistant.chat("Add 5 and 3, then get user info for user123")
```

### Conversation Management

```python
# Get conversation history
history = assistant.get_conversation_history()

# Clear conversation (keeps system prompt)
assistant.clear_conversation()

# Save conversation
assistant.save_conversation("chat_history.json")

# Load conversation
assistant.load_conversation("chat_history.json")
```

## API Reference

### Assistant

```python
Assistant(
    api_key: str,
    base_url: str,
    model: str,
    system_prompt: str = "You are a helpful AI assistant.",
    temperature: float = 0.7,
    max_tokens: Optional[int] = None
)
```

#### Methods

- `chat(message: str) -> str`: Send a message and get a response
- `tool(description: str = "")`: Decorator to register functions as tools
- `get_conversation_history() -> List[Dict[str, Any]]`: Get conversation history
- `clear_conversation()`: Clear conversation history
- `save_conversation(filename: str)`: Save conversation to JSON file
- `load_conversation(filename: str)`: Load conversation from JSON file

## Requirements

- Python 3.8+

## License

MIT License - see LICENSE file for details.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
