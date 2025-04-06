from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from decouple import config
from Functions.model import handle_chat  # Import the function from model.py
from fastapi.responses import JSONResponse

# Custom Functions Import...
from Functions.model import convert_audio_to_text
from Functions.model import handle_chat  # Import the function from model.py

# Initiating App
app = FastAPI()

# CORS Origins
origins = [
    "http://localhost:5173",
    "http://localhost:5174",
    "http://localhost:4173", # Build app from react
    "http://localhost:4174",
    "http://localhost:3000", # Frontend setup
]

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Check healthy
# @app.get("/health")
# async def check_health():
#     return {"message": "Healthy"}


# Endpoint for processing audio and generating chat response
@app.post("/post-audio-get/")
async def get_audio():
    try:
        # Step 1: Specify the static path to the audio file
        audio_input = "Ashu's Voice.mp4"  # Path to your audio file

        # Step 2: Transcribe the audio content to text using Whisper
        message_decoded = convert_audio_to_text(audio_input)

        if not message_decoded:
            raise HTTPException(status_code=500, detail="Error in transcription")

        print(f"Transcription: {message_decoded}")

        # Step 3: Generate a chat response using the transcribed message
        assistant_response = handle_chat(message_decoded)  # Generate assistant's response

        return JSONResponse(content={"message": "Audio processed successfully", "transcription": message_decoded, "response": assistant_response})

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")

# # Post bot response (send a file from react to our fastapi backend)
# @app.post("/post-audio/")
# async def post_audio(file: UploadFile = File(...)):
#     print("hello")
