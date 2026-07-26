import os
from fastapi import FastAPI, Depends, Request
from fastapi.responses import StreamingResponse
from fastapi_clerk_auth import ClerkConfig, ClerkHTTPBearer, HTTPAuthorizationCredentials
from groq import Groq
from pydantic import BaseModel
from typing import Optional

app = FastAPI()

# Get JWKS URL with fallback safeguard
JWKS_URL = os.environ.get(
    "CLERK_JWKS_URL", 
    "https://inspired-mustang-21.clerk.accounts.dev/.well-known/jwks.json"
)

# Initialize Clerk Auth Guard
clerk_config = ClerkConfig(jwks_url=JWKS_URL)
clerk_guard = ClerkHTTPBearer(clerk_config)

# Initialize Groq client
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

# Schema for incoming JSON body
class IdeaRequest(BaseModel):
    prompt: Optional[str] = "Reply with a new business idea for AI Agents, formatted with headings, sub-headings and bullet points"

@app.api_route("/api", methods=["GET", "POST"])
def generate_idea(
    request: Optional[IdeaRequest] = None,
    creds: HTTPAuthorizationCredentials = Depends(clerk_guard)
):
    # Extract user ID from authenticated Clerk JWT
    user_id = creds.decoded.get("sub") if creds and hasattr(creds, 'decoded') else None

    # Safely extract prompt regardless of GET or POST
    user_prompt = "Reply with a new business idea for AI Agents, formatted with headings, sub-headings and bullet points"
    if request and request.prompt:
        user_prompt = request.prompt

    stream = client.chat.completions.create(
        model="llama-3.1-8b-instant",  # Updated to supported Groq model
        messages=[
            {"role": "system", "content": "You are a helpful business idea generator."},
            {"role": "user", "content": user_prompt},
        ],
        stream=True,
    )

    def event_stream():
        for chunk in stream:
            if chunk.choices and chunk.choices[0].delta.content:
                text = chunk.choices[0].delta.content
                # Replace raw newlines with encoded markers or send clean chunks
                escaped_text = text.replace("\n", "\\n")
                yield f"data: {escaped_text}\n\n"

    return StreamingResponse(event_stream(), media_type="text/event-stream")