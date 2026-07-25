import os
from fastapi import FastAPI
from groq import Groq
from pydantic import BaseModel

app = FastAPI()

# Initialize Groq client
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))


# 1. Schema for incoming JSON body from frontend
class IdeaRequest(BaseModel):
    prompt: str = "Generate a creative SaaS startup business idea."


# 2. API Endpoint handling both GET and POST
@app.api_route("/api", methods=["GET", "POST"])
def generate_idea(request: IdeaRequest = None):
    # Extract prompt safely whether sent via JSON body or default
    user_prompt = (
        request.prompt
        if request
        else "Generate a creative SaaS startup business idea."
    )

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": "You are a helpful business idea generator."},
            {"role": "user", "content": user_prompt},
        ],
    )
    return {"result": response.choices[0].message.content}