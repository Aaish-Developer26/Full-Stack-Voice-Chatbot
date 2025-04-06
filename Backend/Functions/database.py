import json
from datetime import datetime

# File path for storing messages
STORE_FILE = "stored_data.json"

# Function to read stored messages from the JSON file
def read_stored_messages():
    try:
        with open(STORE_FILE, "r") as file:
            data = json.load(file)
            return data.get("messages", [])
    except FileNotFoundError:
        # If file doesn't exist, create it with an empty list
        return []

# Function to store recent messages to the stored_data.json file
def store_message(message_data):
    # Read current stored messages
    stored_messages = read_stored_messages()

    # Append the new message to the stored messages
    stored_messages.append(message_data)

    # Save the updated list back to the file
    with open(STORE_FILE, "w") as file:
        json.dump({"messages": stored_messages}, file, indent=4)

# Function to get the last X messages (e.g., last 5 messages)
def get_recent_messages(num_messages=5):
    stored_messages = read_stored_messages()
    return stored_messages[-num_messages:]

# Function to generate a timestamped message
def create_message(content, role="user"):
    return {
        "content": content,
        "role": role,  # Either "user" or "assistant"
        "timestamp": datetime.now().isoformat()
    }

# Function to store a specific prompt (optional)
def store_prompt(prompt):
    try:
        stored_prompts = read_stored_prompts()
        stored_prompts.append({"prompt": prompt, "timestamp": datetime.now().isoformat()})
        with open("stored_prompts.json", "w") as file:
            json.dump({"prompts": stored_prompts}, file, indent=4)
    except Exception as e:
        print(f"Error storing prompt: {e}")

# Function to read stored prompts
def read_stored_prompts():
    try:
        with open("stored_prompts.json", "r") as file:
            data = json.load(file)
            return data.get("prompts", [])
    except FileNotFoundError:
        return []
