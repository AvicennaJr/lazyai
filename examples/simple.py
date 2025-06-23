from lazyai import Assistant

api_key = "your-api-key"
base_url = "https://api.groq.com/openai/v1"
model = "llama-3.3-70b-versatile"

assistant = Assistant(api_key=api_key, base_url=base_url, model=model)

response = assistant.chat("Can you tell me what tools you have available?")
print(f"Assistant: {response}")
