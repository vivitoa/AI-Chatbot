import groq
import os
import tkinter as tk
from tkinter import scrolledtext, font

# Initialize Groq API client
client = groq.Client(api_key="API KEY")

# Chat history
chat_history = []

# Dark theme colors
BG_COLOR = "#2d2d2d"
TEXT_COLOR = "#ffffff"
ENTRY_BG = "#404040"
BUTTON_BG = "#4a4a4a"
BUTTON_ACTIVE = "#666666"


# Function to save chat history
def save_chat_history(messages, filename="chat_history.txt"):
    try:
        with open(filename, "a") as file:
            for message in messages:
                file.write(f"{message['role'].capitalize()}: {message['content']}\n")
            file.write("\n")
        print(f"Chat history saved to: {filename}")
    except Exception as e:
        print(f"Error saving chat history: {e}")


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


# GUI Application
class ChatbotApp:
    def __init__(self, root):
        self.root = root
        self.root.title("AI Chatbot")
        self.root.configure(bg=BG_COLOR)
        self.root.minsize(400, 300)

        # Create main container first
        self.main_frame = tk.Frame(root, bg=BG_COLOR)
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Initialize UI components before setting theme
        self.setup_model_selection()
        self.setup_custom_prompt()
        self.setup_chat_display()
        self.setup_input_frame()

        # Set dark theme after components are initialized
        self.set_dark_theme()

        # Initialize chat
        self.custom_prompt = "You are a helpful assistant."
        chat_history.append({"role": "system", "content": self.custom_prompt})

    def setup_model_selection(self):
        # Model selection
        self.controls_frame = tk.Frame(self.main_frame, bg=BG_COLOR)
        self.controls_frame.pack(fill=tk.X, pady=5)

        self.model_label = tk.Label(self.controls_frame, text="Model:", bg=BG_COLOR, fg=TEXT_COLOR)
        self.model_label.pack(side=tk.LEFT, padx=5)

        self.model_var = tk.StringVar(value="llama3-8b-8192")
        self.model_menu = tk.OptionMenu(
            self.controls_frame,
            self.model_var,
            "llama3-8b-8192",
            "mixtral-8x7b-32768",
            "gemma-7b-it"
        )
        self.model_menu.config(bg=BUTTON_BG, fg=TEXT_COLOR, activebackground=BUTTON_ACTIVE)
        self.model_menu.pack(side=tk.LEFT, padx=5)

    def setup_custom_prompt(self):
        # Custom prompt
        self.prompt_button = tk.Button(
            self.controls_frame,
            text="Set Prompt",
            command=self.set_custom_prompt,
            bg=BUTTON_BG,
            fg=TEXT_COLOR,
            activebackground=BUTTON_ACTIVE
        )
        self.prompt_button.pack(side=tk.RIGHT, padx=5)

    def setup_chat_display(self):
        # Chat history display
        self.chat_history_display = scrolledtext.ScrolledText(
            self.main_frame,
            wrap=tk.WORD,
            state='disabled',
            bg=ENTRY_BG,
            fg=TEXT_COLOR,
            insertbackground=TEXT_COLOR
        )
        self.chat_history_display.pack(fill=tk.BOTH, expand=True, pady=5)

    def setup_input_frame(self):
        # Input frame
        self.input_frame = tk.Frame(self.main_frame, bg=BG_COLOR)
        self.input_frame.pack(fill=tk.X, pady=5)

        # User input field
        self.user_input = tk.Entry(
            self.input_frame,
            width=50,
            bg=ENTRY_BG,
            fg=TEXT_COLOR,
            insertbackground=TEXT_COLOR
        )
        self.user_input.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        self.user_input.bind("<Return>", lambda event: self.send_message())

        # Send button
        self.send_button = tk.Button(
            self.input_frame,
            text="Send",
            command=self.send_message,
            bg=BUTTON_BG,
            fg=TEXT_COLOR,
            activebackground=BUTTON_ACTIVE
        )
        self.send_button.pack(side=tk.RIGHT, padx=5)

    def set_dark_theme(self):
        # Configure default colors
        self.root.tk_setPalette(
            background=BG_COLOR,
            foreground=TEXT_COLOR,
            activeBackground=BUTTON_ACTIVE,
            activeForeground=TEXT_COLOR
        )

        # Style option menu if it exists
        if hasattr(self, 'model_menu'):
            menu = self.model_menu['menu']
            menu.config(bg=ENTRY_BG, fg=TEXT_COLOR)

    def set_custom_prompt(self):
        prompt_window = tk.Toplevel(self.root)
        prompt_window.title("Set Custom Prompt")
        prompt_window.configure(bg=BG_COLOR)

        prompt_label = tk.Label(
            prompt_window,
            text="Enter custom prompt:",
            bg=BG_COLOR,
            fg=TEXT_COLOR
        )
        prompt_label.pack(padx=10, pady=5)

        prompt_entry = tk.Text(
            prompt_window,
            height=4,
            width=40,
            bg=ENTRY_BG,
            fg=TEXT_COLOR,
            insertbackground=TEXT_COLOR
        )
        prompt_entry.pack(padx=10, pady=5)
        prompt_entry.insert("1.0", self.custom_prompt)

        def save_prompt():
            self.custom_prompt = prompt_entry.get("1.0", "end-1c")
            chat_history.append({"role": "system", "content": self.custom_prompt})
            prompt_window.destroy()

        save_button = tk.Button(
            prompt_window,
            text="Save",
            command=save_prompt,
            bg=BUTTON_BG,
            fg=TEXT_COLOR,
            activebackground=BUTTON_ACTIVE
        )
        save_button.pack(pady=5)

    def send_message(self):
        user_input = self.user_input.get().strip()
        if not user_input:
            return

        if user_input.lower() in ["exit", "quit"]:
            save_chat_history(chat_history)
            self.root.destroy()
            return

        self.update_chat_display(f"You: {user_input}", "user")
        self.user_input.delete(0, tk.END)

        response = get_ai_response(user_input, self.model_var.get(), chat_history)
        self.update_chat_display(f"AI: {response}", "ai")

    def update_chat_display(self, text, sender):
        self.chat_history_display.config(state='normal')
        tag = "user" if sender == "user" else "ai"
        self.chat_history_display.insert(tk.END, text + "\n", tag)
        self.chat_history_display.config(state='disabled')
        self.chat_history_display.yview(tk.END)


# Main application
if __name__ == "__main__":
    root = tk.Tk()
    app = ChatbotApp(root)
    root.mainloop()