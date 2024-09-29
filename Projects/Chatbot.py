import tkinter as tk
from datetime import datetime
import threading
from gtts import gTTS
import os
import re
import nltk
from movie_recommendation import recommend_movie
from nltk.tokenize import word_tokenize
from nltk import pos_tag, ne_chunk

# Ensure the necessary nltk resources are downloaded
nltk.download('punkt')
nltk.download('punkt_tab')
nltk.download('averaged_perceptron_tagger')
nltk.download('averaged_perceptron_tagger_eng')
nltk.download('maxent_ne_chunker')
nltk.download('maxent_ne_chunker_tab')
nltk.download('words')

# Load responses from a file
def load_responses(filename):
    responses = {}
    with open(filename, 'r') as file:
        lines = file.readlines()
        key = None
        for line in lines:
            line = line.strip()
            if line.startswith("user:"):
                key = line.split("user:")[1].strip()
            elif line.startswith("bot:") and key:
                responses[key] = line.split("bot:")[1].strip()
                key = None
    return responses

def play_music():
    text = "Hello, I'm a chatbot! La la la la..."
    tts = gTTS(text=text, lang="en")
    tts.save("music.mp3")
    os.system("music.mp3")

def process_input_nltk(user_message):
    # Tokenize the message
    tokens = word_tokenize(user_message)
    
    # Part-of-speech tagging
    pos_tags = pos_tag(tokens)
    
    # Named Entity Recognition (NER)
    entities = ne_chunk(pos_tags)

    return tokens, pos_tags, entities


# Simple bot function that checks the input and returns the corresponding response
def simple_bot(user_message):
    tokens, pos_tags, entities = process_input_nltk(user_message)
    
    # Handle exit commands
    if any(phrase in tokens for phrase in ["bye", "exit", "quit", "goodbye"]):
        root.quit()  # Close the Tkinter window
        return "Goodbye!"
    
    # Check if the user is asking for the time
    if "time" in tokens:
        return f"The current time is {datetime.now().strftime('%H:%M:%S')}."
    if "music" in tokens:
        threading.Thread(target=play_music).start()  # Start playing music in a separate thread
        return "Playing music..."
    if "weather" in tokens:
        return "The weather is nice today."
    
    # Improved movie recommendation logic
    movie_request_match = re.search(r'recommend a movie in (bollywood|hollywood)\s*(\w+)', user_message.lower())
    if movie_request_match:
        industry = movie_request_match.group(1).strip()
        genre = movie_request_match.group(2).strip()
        return recommend_movie(industry, genre)
    if "recommend a movie" in tokens:
        return "Please specify the industry (Bollywood/Hollywood) and genre for movie recommendations."

    # Check if the user is asking for a calculation
    if "calculation" in tokens or "maths" in user_message:
        return "Enter two numbers with operators to perform your calculation...I can do basic operations!"
    
    # Check if the user input contains a basic arithmetic operation
    match = re.match(r'(\d+)\s*([+\-*/])\s*(\d+)', user_message)
    if match:
        num1, operator, num2 = match.groups()
        num1, num2 = float(num1), float(num2)
        if operator == '+':
            return str(num1 + num2)
        elif operator == '-':
            return str(num1 - num2)
        elif operator == '*':
            return str(num1 * num2)
        elif operator == '/':
            if num2 != 0:
                return str(num1 / num2)
            else:
                return "Error: Division by zero is not possible."
    
    # Default response from the predefined responses
    return responses.get(user_message, "Sorry, I don't understand that.")

# Function to display user input and bot response
def display_input(event=None):
    user_input = entry.get()
    
    # Display the user's message in the conversation area
    conversation.config(state='normal')
    conversation.insert(tk.END, f"You: {user_input}\n", "user")
    conversation.config(state='disabled')
    
    # Clear the entry widget
    entry.delete(0, tk.END)
    
    # Get the bot's response
    bot_response = f"Bot: {simple_bot(user_input)}\n"
    
    # Display the bot's response in the conversation area
    conversation.config(state='normal')
    conversation.insert(tk.END, bot_response, "bot")
    conversation.config(state='disabled')

    # Auto-scroll to the end of the conversation
    conversation.see(tk.END)

# Function to handle the Up Arrow key press
def handle_up_arrow(event):
    # Get the last user message
    history = conversation.get("1.0", tk.END).strip().split('\n')
    for line in reversed(history):
        if line.startswith("You: "):
            entry.delete(0, tk.END)
            entry.insert(tk.END, line[len("You: "):])
            break

# Function to resize fonts based on window size
def resize_fonts(event):
    # Calculate font sizes based on the window width
    base_width = 400
    scale_factor = event.width / base_width
    new_font_size = int(16 * scale_factor)
    new_font_size_text = int(12 * scale_factor)

    # Update the fonts
    label.config(font=("Helvetica", new_font_size, "bold"))
    conversation.config(font=("Arial", new_font_size_text))
    entry.config(font=("Arial", new_font_size_text))
    button.config(font=("Helvetica", new_font_size, "bold"))

# Initialize the Tkinter root window
root = tk.Tk()
root.title("Chatbot")
root.geometry("800x600")
root.configure(bg="#2C3E50")  # Set a dark background color

# Bind the resize event to the resize_fonts function
root.bind('<Configure>', resize_fonts)

# Bind Enter key to send the message
root.bind('<Return>', display_input)

# Bind Up Arrow key to copy the previous message
root.bind('<Up>', handle_up_arrow)

# Create a label at the top with a custom font and color
label = tk.Label(root, text="Chat with the Bot", font=("Helvetica", 16, "bold"), fg="#ECF0F1", bg="#2C3E50")
label.pack(pady=10, fill='x')

# Create a Text widget for displaying the conversation with a custom font and color
conversation = tk.Text(root, height=10, state='disabled', wrap='word', font=("Arial", 12), bg="#34495E", fg="#ECF0F1", relief='flat')
conversation.pack(pady=10, padx=10, fill='both', expand=True)

# Create an Entry widget for user input with a custom font and color
entry = tk.Entry(root, width=20, font=("Arial", 12), bg="#ECF0F1", fg="#2C3E50", relief='flat')
entry.pack(pady=5, padx=10, fill='x')

# Create a button and pack it with padding and expansion, with a custom color
button = tk.Button(root, text="Send", command=display_input, font=("Helvetica", 12, "bold"), bg="#1ABC9C", fg="#ECF0F1", relief='flat', activebackground="#16A085")
button.pack(pady=10, fill='x')

# Load the responses from the text file
filename = "responses.txt"
responses = load_responses(filename)

# Start the Tkinter main loop
root.mainloop()
