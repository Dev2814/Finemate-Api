from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from models import PromptRequest
from openai import OpenAI
from dotenv import load_dotenv
import os


load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")

# Initialize the OpenAI client
client = OpenAI(api_key=openai_api_key)

app = FastAPI()

# CORS for local testing
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change to your Flutter app's domain in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
#this is post method
@app.post("/get_suggestion/")
async def get_suggestion(data: PromptRequest):
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful finance assistant. Give one-line financial suggestions based on the user's input."},
                {"role": "user", "content": data.prompt}
            ],
            max_tokens=100,
            temperature=0.7
        )
        suggestion = response.choices[0].message.content
        return {"suggestion": suggestion}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
