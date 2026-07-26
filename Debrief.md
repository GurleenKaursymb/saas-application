-25-07-2026-

Right now, I have switched from Gemini model to usign a Groq mmodel. But when I deployed to production i'm getting a 
{"detail":"Method Not Allowed"} error. 

Now one reason could be that basically HTTP 405 is a standard FastAPI message which happens when your frontend HTT method 
doesnt match what the python root decorator is listening for. But my root decorator says @app.post only not @app.get 

Previousl the error was that the frontend tried to talk to the backend at /api. But the path isnt matching up on vercel's servers. So it 
sends back the default 404 not found page. My fonrtend expected a JSON text but received a full HTML webpage instead. 

Now for the {"detail":"Method Not Allowed"} error - In web development browsers talk to servers using different HTTP methods: GET which is used for when we want to fetch data and POST when we watnt to send data. 

My python code opriginally only had POSt so im thinking maybe it only accepted POST requests so i changed the python ecorator to accept both POST and GET 

Also fastAPI needs to know how to read the prompt i typed into the text box so noe the python function originally looked like def generate_idea(prompt: str): now when i write prompt: str so maybe fastaPI that the data was coming inside the browser URL bar but modern javascript frontend sends data secretly inside the request body formatted as a JSON object. Because FastAPI looked at the URL bar and found nothing, it crashed.

So i've brought in Pydantic's BaseModel:
class IdeaRequest(BaseModel):
    prompt: str = "Generate a creative SaaS startup business idea."This acts as a "blueprint" for FastAPI. It tells python to Expect a JSON object in the request body with a key called prompt, unpack it automatically, and pass it to my function as request.prompt


* Now the backend was fine and returning the generated idea nut on the webpage the text was wrapped inside {result: " " } along with messy escape characters like \n. It happened because in my index.tsx file i had:

.then(res => res.text()) - so javascript took the entire raw response by the python server and gave it on screen as it is 
.then(setIdea)

so i changed to:
.then(res => res.json()) - instead of treating server resposne as plain text this converts 
it into a proper javascript object 
.then(data => setIdea(data.result)) - this extracts only the clean text stored under the "result" key leaving behind the JSON syntax wrappers. 

********

Now next, basically before when the user asked for a startup idea the app waited for the AI to write the whole response in the background before sending it to the frontend. This caused a 3-5 second delay where the screen showed nothing. Also the formatted text looked like raw code. 

So I updated the app to have:
1. Real time streaming: Instead of waiting for the full response, the Python backend sends words/tokens to the browser as soon as Groq generates them
2. Markdown and Typography Rendering: I added libraries to convert raw text tags into clean, styled HTML on the frontend (like converting **bold** into actual bold text).

i updated the index.py and index.tsx codes: 

import os — Standard Python library to read system environment variables (where your Groq API key is stored).
from fastapi import FastAPI — Imports FastAPI, the web framework used to build backend endpoints.
from fastapi.responses import StreamingResponse — Imports a special FastAPI response type that keeps an HTTP connection open to stream data live instead of sending it all at once
from pydantic import BaseModel — Imports Pydantic to validate incoming data structures from frontend requests.
client = Groq(...) — Initializes the Groq client using your secret API key from the environment.

class IdeaRequest(BaseModel): ... — Defines expected incoming request data. It tells FastAPI that if a JSON body is sent, it can contain a prompt string (with a default fallback).
@app.api_route("/api", methods=["GET", "POST"]) — Tells FastAPI to run generate_idea() whenever someone visits /api via either a GET or POST web request.
def generate_idea(request: IdeaRequest = None): — Defines the handler function, accepting optional JSON input matching IdeaRequest
user_prompt = (...) — Safely checks if the user provided a custom prompt; if not, it defaults to "Generate a creative SaaS startup business idea."

stream = client.chat.completions.create(...) — Sends the prompt to Groq's llama-3.3-70b-versatile model. Crucially, stream=True tells Groq not to wait, but to yield response chunks immediately as they are generated.

def event_stream(): — Defines a Python generator function to process incoming AI chunks into a format browsers understand.

for chunk in stream: — Loops through each tiny chunk of text as Groq streams it in real-time.

text = chunk.choices[0].delta.content — Extracts the newly generated piece of text from the chunk object.

**********

Next i'm updating the backend prompt in iindex.py like changing rhw prompt sent to the LLm so it asks for formatted output (headings, sub-headings, bullet points).
I'm also replacing the raw text UI in React (pages/index.tsx) with a styled Markdown parser (react-markdown) and glassmorphism Tailwind CSS styling.


So far i've successfully added Real time streaming and Professional UI to this LLM app that i'm making. 

----------------------------------------------------------------------------------------------------------------------------------------------------------------------
Day 3 / -26/07/2026- / 