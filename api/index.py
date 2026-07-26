import os
from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from groq import Groq
from pydantic import BaseModel

app = FastAPI()

# Initialize Groq client
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))


# 1. Schema for incoming JSON body from frontend
class IdeaRequest(BaseModel):
    prompt: str = "Reply with a new business idea for AI Agents, formatted with headings, sub-headings and bullet points"


# 2. API Endpoint handling streaming
@app.api_route("/api", methods=["GET", "POST"])
def generate_idea(request: IdeaRequest = None):
    # Extract prompt safely whether sent via JSON body or default
    user_prompt = (
        request.prompt
        if request
        else "Reply with a new business idea for AI Agents, formatted with headings, sub-headings and bullet points"
    )
    
    # Enable streaming with stream=True
    stream = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": "You are a helpful business idea generator."},
            {"role": "user", "content": user_prompt},
        ],
        stream=True,
    )

    # Generator function to stream tokens chunk by chunk
    def event_stream():
        for chunk in stream:
            text = chunk.choices[0].delta.content
            if text:
                lines = text.split("\n")
                for line in lines:
                    yield f"data: {line}\n"
                yield "\n"

    return StreamingResponse(event_stream(), media_type="text/event-stream") 
    