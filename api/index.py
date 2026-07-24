import os
from fastapi import FastAPI
from groq import Groq

app = FastAPI()

# Initialize Groq client
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))


@app.post("/api")  # or whatever your route endpoint is
def generate_idea(prompt: str):
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",  # High quality, ultra-fast & free!
        messages=[
            {"role": "system", "content": "You are a helpful business idea generator."},
            {"role": "user", "content": prompt},
        ],
    )
    return {"result": response.choices[0].message.content}