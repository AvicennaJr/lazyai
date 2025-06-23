from eyai import Assistant

api_key = "your-api-key"
base_url = "https://api.groq.com/openai/v1"
model = "llama-3.3-70b-versatile"

assistant = Assistant(api_key=api_key, base_url=base_url, model=model)

response = assistant.chat("Hi, how are you?")
print(f"Assistant: {response}")
