import whisper
import numpy as np
import openai
from decouple import config
from Functions.database import create_message, store_message, get_recent_messages

# Set your OpenAI API key (loaded from .env file)
openai.api_key = config("OPENAI_API_KEY")


# Load the Whisper small model
model = whisper.load_model("small", download_root="C:\\Users\\EliteBook\\Documents\\Voice Chatbot\\Backend\\Whisper_model")

# Convert Audio to Text
def convert_audio_to_text(audio_file_path):
    try:
         # Load audio from file path
        audio = whisper.load_audio(audio_file_path)  # Load audio from the given file path
        audio = whisper.pad_or_trim(audio)  # Ensure the audio is of the correct length for Whisper
        
        # Perform the transcription
        result = model.transcribe(audio)
        
        # Extract the transcribed text from the result
        message_text = result["text"]
        return message_text
    except Exception as e:
        print(f"Error occurred: {e}")
        return None


# Function to get response from OpenAI's GPT model
def get_chat_response(prompt):
    try:
        # Make a request to OpenAI's API for a chat-based completion
        response = openai.Completion.create(
            model="gpt-3.5-turbo",  # You can adjust this to the latest available model
            prompt=prompt,
            max_tokens=150,
            temperature=0.7,
            stop=["\n"]
        )
        # Return the text of the response
        return response.choices[0].text.strip()
    except Exception as e:
        print(f"Error generating response: {e}")
        return "Sorry, I couldn't generate a response."
    

# Function to generate the conversation prompt from recent messages
def generate_chat_prompt():
    # Get the last 5 messages (you can adjust this number as needed)
    recent_messages = get_recent_messages()

    # Format the conversation with each message (user -> assistant)
    prompt = ""
    for message in recent_messages:
        role = "User" if message['role'] == "user" else "Assistant"
        prompt += f"{role}: {message['content']}\n"
    
    prompt += "Assistant: "  # Assistant's turn to respond
    return prompt

# Function to handle new chat and save messages
def handle_chat(message_content):
    # Create user message and store it
    user_message = create_message(message_content, role="user")
    store_message(user_message)

    # Generate prompt based on recent conversation
    prompt = generate_chat_prompt()

    # Get the assistant's response from OpenAI
    assistant_response = get_chat_response(prompt)

    # Create and store assistant's message
    assistant_message = create_message(assistant_response, role="assistant")
    store_message(assistant_message)

    return assistant_response