import tkinter as tk
from tkinter import scrolledtext, messagebox
import boto3
import json

# Function to handle the bot's response
def call_bot():
    question = user_input.get("1.0", "end-1c")

    try:
        with open("questions.txt", "r", encoding='utf-8') as f:
            context = f.read()
    except FileNotFoundError:
        context = ""

    prompt = f"##{context}## Answer the question based only on the information provided between ##. User could ask questions in different ways. You should match new question with current Questions. If you cannot do that and there isn't enough information to answer return 'I don't have infor about it?'  Question: {question}"

    # Initialize the boto3 client
    bedrock_runtime = boto3.client(
        service_name="bedrock-runtime",
        region_name="us-east-1"
    )

    # Construct the request payload using json.dumps
    request_body = {
        "prompt": prompt,
        "maxTokens": 5000,
        "temperature": 0.7,
        "topP": 0.95,
        "stopSequences": ["END"],
    }

    kwargs = {
        "modelId": "ai21.j2-ultra-v1",
        "contentType": "application/json",
        "accept": "*/*",
        "body": json.dumps(request_body)
    }

    try:
        response = bedrock_runtime.invoke_model(**kwargs)
        response_body = json.loads(response['body'].read().decode('utf-8'))
        completion = response_body['completions'][0]['data']['text']
        add_message(question, completion)  # Add Bot's response to the chat
    except botocore.exceptions.ClientError as e:
        messagebox.showerror("Error", f"Error calling the API: {e}")

# Function to add messages to the chat interface
def add_message(question ,answer):
    chat_history.config(state='normal')
    chat_history.insert(tk.END, f"Emirhan: {question}\n")
    chat_history.insert(tk.END, f"Bot : {answer}\n\n")
    chat_history.config(state='disabled')
    chat_history.see(tk.END)

# Setting up the GUI
root = tk.Tk()
root.title("Chat with Bot")

# Chat history display
chat_history = scrolledtext.ScrolledText(root, wrap=tk.WORD, state='disabled')
chat_history.pack(expand=True, fill="both")

# User input field
user_input = tk.Text(root, height=3)
user_input.pack(expand=True, fill="x")

# Ask button
ask_button = tk.Button(root, text="Ask", command=call_bot)
ask_button.pack()

root.mainloop()
