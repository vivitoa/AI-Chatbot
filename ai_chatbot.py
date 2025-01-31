import groq
import os
print("Current working directory:", os.getcwd())

# Initialize Groq API client
client = groq.Client(api_key="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")

# Chat history
chat_history = []

# Function to save chat history
def save_chat_history(messages, filename="C:/Users/vivit/Documents/GitHub/AI-Chatbot/chat_history.txt"):
    try:
        with open(filename, "a") as file:
            for message in messages:
                file.write(f"{message['role'].capitalize()}: {message['content']}\n")
            file.write("\n")
        print(f"Chat history saved to: {filename}")
    except Exception as e:
        print(f"Error saving chat history: {e}")

# Function to select model
def select_model():
    models = {
        "1": "llama3-8b-8192",
        "2": "mixtral-8x7b-32768",
        "3": "gemma-7b-it"
    }
    print("Select a model:")
    for key, value in models.items():
        print(f"{key}. {value}")
    choice = input("Enter the number of the model: ")
    return models.get(choice, "llama3-8b-8192")  # Default model

# Function to set custom prompt
def set_custom_prompt():
    prompt = input("Enter a custom prompt (or press Enter to use default): ")
    return prompt if prompt else "You are a helpful assistant."

# Function to get AI response
def get_ai_response(user_input, model, chat_history):
    try:
        chat_history.append({"role": "user", "content": user_input})
        response = client.chat.completions.create(
            model=model,
            messages=chat_history
        )
        ai_message = response.choices[0].message.content
        chat_history.append({"role": "assistant", "content": ai_message})
        return ai_message
    except Exception as e:
        return f"Error: {e}"

# Main loop
if __name__ == "__main__":
    print("Welcome to your AI chatbot! Type 'exit' to quit.")
    model = select_model()
    custom_prompt = set_custom_prompt()
    chat_history.append({"role": "system", "content": custom_prompt})

    while True:
        user_input = input("\nYou: ")
        if user_input.lower() in ["exit", "quit"]:
            save_chat_history(chat_history)
            print("\nGoodbye! 👋")
            break
        response = get_ai_response(user_input, model, chat_history)
        print("AI:", response)