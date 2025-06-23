from eyai import Assistant

def main():
    api_key = "your-api-key"
    base_url = "https://api.groq.com/openai/v1"
    model = "llama-3.3-70b-versatile"

    assistant = Assistant(api_key=api_key, base_url=base_url, model=model)

    @assistant.tool("Get the current time")
    def get_current_time() -> str:
        from datetime import datetime
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    @assistant.tool("Calculate the square of a number")
    def square(number: float) -> float:
        return number ** 2

    response = assistant.chat("Hello! What time is it?")
    print(f"Assistant: {response}")

    response = assistant.chat("What's the square of 7?")
    print(f"Assistant: {response}")

    response = assistant.chat("Can you tell me what tools you have available?")
    print(f"Assistant: {response}")

if __name__ == "__main__":
    main()
