import nltk
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import tkinter as tk
from tkinter import scrolledtext
from PIL import Image, ImageTk
import string
import webbrowser

# Load the dataset
with open(r"file.txt", 'r', encoding='utf-8') as file:
    dataset = file.read()

# Preprocess the dataset
sent_tokens = nltk.sent_tokenize(dataset)
word_tokens = nltk.word_tokenize(dataset.lower())

lemmatizer = nltk.stem.WordNetLemmatizer()
remove_punct_dict = dict((ord(punct), None) for punct in string.punctuation)

def LemTokens(tokens):
    return [lemmatizer.lemmatize(token) for token in tokens]

def LemNormalize(text):
    return LemTokens(nltk.word_tokenize(text.lower().translate(remove_punct_dict)))

# TF-IDF Vectorization
TfidfVec = TfidfVectorizer(tokenizer=LemNormalize, stop_words='english')
tfidf_matrix = TfidfVec.fit_transform(sent_tokens)

# Function to generate response
def response(user_response):
    robo_response = ''
    user_tfidf = TfidfVec.transform([user_response])
    cosine_similarities = cosine_similarity(user_tfidf, tfidf_matrix)
    idx = cosine_similarities.argsort()[0][-1]
    flat = cosine_similarities.flatten()
    flat.sort()
    req_tfidf = flat[-1]

    if req_tfidf == 0:
        robo_response = "I am sorry! I don't understand your question."
    else:
        robo_response = sent_tokens[idx]

    return robo_response

# Function to handle user input
def handle_input():
    user_response = user_input.get()
    user_input.delete(0, tk.END)  # Clear input field after submission

    if user_response.lower() == 'bye':  # Check if user wants to exit
        root.destroy()  # Close the tkinter window
        return

    bot_response = response(user_response)
    conversation_text.configure(state=tk.NORMAL)  # Enable text box to insert conversation
    conversation_text.insert(tk.END, "You: " + user_response + "\n")
    conversation_text.insert(tk.END, "Bot: " + bot_response + "\n")
    conversation_text.configure(state=tk.DISABLED)  # Disable text box after inserting conversation

def start_conversation():
    main_menu_frame.pack_forget()  # Hide the main menu frame
    conversation_frame.pack()  # Show the conversation frame
    about_frame.pack_forget()

def home():
    main_menu_frame.pack()
    conversation_frame.pack_forget()
    about_frame.pack_forget()

def open_google_form():
    google_form_link = "https://docs.google.com/forms/d/e/1FAIpQLScoRVg2TJdS-Qflh5TcD8pQXHKyczeh0tTvTDbYAuxPbBV6zQ/viewform"
    webbrowser.open(google_form_link)

def about():
    conversation_frame.pack_forget()
    main_menu_frame.pack_forget()
    about_frame.pack()
    


heading = "LAND LEGAL BOT"
para = "\nI'm your property law expert, Ask me anything about\nIndian property law, from ownership to taxes, and I'll\nguide you through the legal jungle with quick,\naccurate answers.\n"
lable_colour="yellow"
# Initialize Tkinter
root = tk.Tk()
root.title("LAND LEGAL BOT(LLB)")
root.geometry("900x600")
root.configure(bg="#808080")  # Set background color to grey

#main frame
main_frame=tk.Frame(root,bg="#808080")
main_frame.pack(side=tk.TOP)
# Circular Logo
logo_image = Image.open(r"LOGO3.png")
logo_image = logo_image.resize((100, 100), Image.LANCZOS)
logo_image = ImageTk.PhotoImage(logo_image)
logo_label = tk.Label(main_frame, image=logo_image, bg="#808080")
logo_label.grid(row=0, column=0, padx=10, pady=10)

# Heading Label
main_menu_label = tk.Label(main_frame, text=heading, font=("Arial", 25,'bold'), bg="#808080",fg="#00FF00") # Light blue color
main_menu_label.grid(row=0, column=1, padx=10, pady=10)

#buttons frame
button_frame = tk.Frame(main_frame, bg="#808080")
button_frame.grid(row=1, column=0, columnspan=2, pady=(0, 10))

# Buttons
button_color = "#87CEEB"  # Light blue color for buttons
text_color = "#008000"  # Green color for button text

home_button = tk.Button(button_frame, text="Home", width=10, font=("Arial", 14, 'bold'), bg=button_color, fg=text_color, activebackground="#FFFFFF",command=home)
home_button.grid(row=1, column=0, padx=5)

about_button = tk.Button(button_frame, text="About", width=10, font=("Arial", 14, 'bold'), bg=button_color, fg=text_color, activebackground="#FFFFFF",command=about)
about_button.grid(row=1, column=1, padx=5)

chatbot_button = tk.Button(button_frame, text="Chatbot", width=10, font=("Arial", 14, 'bold'), bg=button_color, fg=text_color, activebackground="#FFFFFF",command=start_conversation)
chatbot_button.grid(row=1, column=2, padx=5)

contact_button = tk.Button(button_frame, text="Contact Us", width=10, font=("Arial", 14, 'bold'), bg=button_color, fg=text_color, activebackground="#FFFFFF",command=open_google_form)
contact_button.grid(row=1, column=3, padx=5)



# Main Menu Frame
main_menu_frame = tk.Frame(root, bg="#808080")
main_menu_frame.pack()  # Place main menu frame at the top

# Description Label
description_label = tk.Label(main_menu_frame, text=para, font=("Arial", 18,'bold'), bg="#808080", fg=lable_colour) # White color
description_label.grid(row=2, column=0, columnspan=2, padx=10, pady=10)

# Start Button
start_button = tk.Button(main_menu_frame, text="Start", command=start_conversation, width=15, height=2, font=("Arial", 18,'bold'),fg=text_color,bg=button_color,activebackground="#FFFFFF")
start_button.grid(row=3, column=0, columnspan=2, pady=(0, 10))

#label frame
description_label = tk.Label(main_menu_frame, text="I AM JUST A BOT PLEASE CONTACT \nA LAWYER BEFORE TAKING ANY LEGAL ACTION", font=("Arial", 14,"bold"), bg="#808080",fg="#FF0000") # Red color
description_label.grid(row=4, column=0, columnspan=2, padx=10, pady=10)


# Conversation Frame
conversation_frame = tk.Frame(root, bg="#808080")

# Left side of the conversation frame
left_frame = tk.Frame(conversation_frame, bg="#808080")
left_frame.grid(row=2, column=0, padx=10, pady=10, sticky="nsew")

# Bot introduction label
intro_label = tk.Label(left_frame, text="BOT: My name is LLB. Let's have a conversation. Also, \nif you want to exit any time, just type 'Bye'.", font=('Arial', 12,'bold'), bg="#808080", fg=lable_colour) # White color
intro_label.pack(anchor="w")

# Scrolled Text for conversation
conversation_text = scrolledtext.ScrolledText(left_frame, height=20, width=80, state=tk.DISABLED,font=('Arial',10,'bold'), bg="#808080", fg="white") # Dark mode background with white text
conversation_text.pack()

# Right side of the conversation frame
right_frame = tk.Frame(conversation_frame, bg="#808080")
right_frame.grid(row=2, column=1, padx=10, pady=10, sticky="nsew")

# Instruction label
instruction_label = tk.Label(right_frame, text="Write your input here:\n", font=('Arial', 12,'bold'), bg="#808080", fg=lable_colour) # White color
instruction_label.pack(pady=(0, 5))

# Text entry for user response
user_input = tk.Entry(right_frame, width=70, bg="#808080",font=('Arial',10,'bold'), fg="#FFFFFF") # Dark mode background with white text
user_input.pack(pady=(0, 5))

# Button to submit user response
submit_button = tk.Button(right_frame, text="Submit", command=handle_input, bg=button_color, fg=text_color, activebackground="#FFFFFF") # Light blue button with white text
submit_button.pack()

# Grid weights to make the conversation frame expandable
conversation_frame.columnconfigure(0, weight=1)
conversation_frame.columnconfigure(1, weight=1)

# Hide the conversation frame initially
conversation_frame.pack_forget()

about_frame = tk.Frame(root, bg="#808080")

# About Us Label
about_label = tk.Label(about_frame, text="About Us", font=("Arial", 20, 'bold'), bg="#808080", fg="#00FF00") # Green color
about_label.grid(row=0, column=0, columnspan=2, pady=(10, 5))

# Description Frame
desc_frame = tk.Frame(about_frame, bg="#808080")
desc_frame.grid(row=1, column=0, columnspan=2)

desc_label = tk.Label(desc_frame, text="We Yash Arora and Ridhima Kapoor are the brains behind\n Land Legal Bot (LLB), fueled by our love for AI\n and its impact. Our mission?  to empower every Indian\n citizen with comprehensive legal knowledge, ensuring they navigate the \nintricacies of the law with confidence and clarity, with all the legal\n goodness. And hey, we're pretty good at it too!", font=("Arial", 16,'bold'), bg="#808080", fg=lable_colour) # White color
desc_label.grid(row=0, column=0, padx=10, pady=10)



# Pack the About Frame
about_frame.pack()

# Hide the About Frame initially
about_frame.pack_forget()

# Start the GUI
root.mainloop()
