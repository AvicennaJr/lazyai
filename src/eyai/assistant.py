import inspect
import json
from typing import Any, Callable, Dict, List, Optional

import openai

class Assistant:
    def __init__(
        self,
        api_key: str,
        base_url: str,
        model: str,
        system_prompt: str = "You are a helpful AI assistant.",
        temperature: float = 0.7,
        max_tokens: Optional[int] = None
    ):
        """
        Initialize the AI Assistant

        Args:
            api_key: Your API key
            base_url: Base URL for the API (e.g., "https://api.groq.com/openai/v1")
            model: Model to use (e.g., "gpt-3.5-turbo", "llama-3.3-70b-versatile")
            system_prompt: System prompt for the assistant
            temperature: Randomness in responses (0.0 to 1.0)
            max_tokens: Maximum tokens in response
        """
        self.client = openai.Client(api_key=api_key, base_url=base_url)
        self.model = model
        self.temperature = temperature
        self.max_tokens = max_tokens

        self.conversation = [
            {"role": "system", "content": system_prompt}
        ]

        self.tools = []
        self.available_functions = {}

    def tool(self, description: str = ""):
        """
        Decorator to register a function as a tool

        Args:
            description: Description of what the tool does
        """
        def decorator(func: Callable):
            # Get function signature
            sig = inspect.signature(func)

            # Build tool schema
            tool_schema = {
                "type": "function",
                "function": {
                    "name": func.__name__,
                    "description": description or func.__doc__ or f"Execute {func.__name__}",
                    "parameters": {
                        "type": "object",
                        "properties": {},
                        "required": []
                    }
                }
            }

            # Extract parameters from function signature
            for param_name, param in sig.parameters.items():
                param_info = {
                    "type": self._python_type_to_json_type(param.annotation),
                    "description": f"The {param_name} parameter"
                }

                tool_schema["function"]["parameters"]["properties"][param_name] = param_info

                # Add to required if no default value
                if param.default == inspect.Parameter.empty:
                    tool_schema["function"]["parameters"]["required"].append(param_name)

            # Register the tool
            self.tools.append(tool_schema)
            self.available_functions[func.__name__] = func

            return func

        return decorator

    def _python_type_to_json_type(self, python_type) -> str:
        """Convert Python type annotations to JSON schema types"""
        if python_type is str or python_type == "str":
            return "string"
        elif python_type is int or python_type == "int":
            return "integer"
        elif python_type is float or python_type == "float":
            return "number"
        elif python_type is bool or python_type == "bool":
            return "boolean"
        elif python_type is list or python_type == "list":
            return "array"
        elif python_type is dict or python_type == "dict":
            return "object"
        else:
            return "string"  # Default to string

    def chat(self, message: str) -> str:
        """
        Send a message to the AI and get a response

        Args:
            message: The user's message

        Returns:
            The AI's response
        """
        # Add user message to conversation
        self.conversation.append({"role": "user", "content": message})

        # Prepare API call parameters
        api_params = {
            "messages": self.conversation,
            "model": self.model,
            "temperature": self.temperature
        }

        if self.max_tokens:
            api_params["max_tokens"] = self.max_tokens

        if self.tools:
            api_params["tools"] = self.tools
            api_params["tool_choice"] = "auto"

        # Get initial response
        response = self.client.chat.completions.create(**api_params)

        # Check if tools need to be called
        tool_calls = response.choices[0].message.tool_calls

        if tool_calls:
            # Add the assistant's message (with tool calls) to conversation
            self.conversation.append(response.choices[0].message)

            # Execute each tool call
            for tool_call in tool_calls:
                function_name = tool_call.function.name
                function_to_call = self.available_functions[function_name]
                function_args = json.loads(tool_call.function.arguments)

                try:
                    if function_args is None or function_args == {}:
                        function_response = function_to_call()
                    else:
                        function_response = function_to_call(**function_args)
                except Exception as e:
                    function_response = f"Error executing {function_name}: {str(e)}"

                self.conversation.append({
                    "tool_call_id": tool_call.id,
                    "role": "tool",
                    "name": function_name,
                    "content": str(function_response),
                })

            final_response = self.client.chat.completions.create(
                model=self.model,
                messages=self.conversation,
                temperature=self.temperature
            )

            response_content = final_response.choices[0].message.content
        else:
            response_content = response.choices[0].message.content
            self.conversation.append({"role": "assistant", "content": response_content})

        return response_content

    def get_conversation_history(self) -> List[Dict[str, Any]]:
        """Get the current conversation history"""
        return self.conversation.copy()

    def clear_conversation(self):
        """Clear conversation history (keeps system prompt)"""
        system_message = self.conversation[0]  # Keep system prompt
        self.conversation = [system_message]

    def save_conversation(self, filename: str):
        """Save conversation to a JSON file"""
        with open(filename, 'w') as f:
            json.dump(self.conversation, f, indent=2)

    def load_conversation(self, filename: str):
        """Load conversation from a JSON file"""
        with open(filename, 'r') as f:
            self.conversation = json.load(f)
