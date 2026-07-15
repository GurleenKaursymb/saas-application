"""
This cose is basically building a mini website which generates AI business ideas 

When someone visits my website line /api --> code will automaticlly log into AI ask it to create a brand new business idea for 
AI agents and display that exact idea on their screen as plain text. 

I'm swapping out the code using openAI to use gemini isntesad but im keeping the course code in comments.
"""

from fastapi import FastAPI  # type: ignore
"""
This imports FastAPI which is core class to build your web applications.
Now basically what type: ignore means? -
It helps to look at a fundamental difference in how python handles variables compared 
to languages like Java and TypeScript. 
Python uses dynamic typing. So if we write x = 5 and then immediately x = "hello" 
and python wont complain - it figures out what type a variable is while the code is 
actually running. 

But in large projects, developers often use tools like static type checkers (with Mypy being the most popular)
to look at the code before it runs and catch bugs early 
But sometimes mypy cant find fastapi etc and things like that. 

So i'm telling Mypy that we know it cany find the official definitions for fastapi right now. Dont throw an error and dont stop the build and just trust that this import works. 

"""
from fastapi.responses import PlainTextResponse  # type: ignore
"""
By default fastapi cpnverts whatever our function returns into a JSON object - So this line 
imports PlainTextResponse which overrides the behaviour so your API can return raw unformatted text instead. 
"""
#from openai import OpenAI  # type: ignore

#This imports the official client library for interacting with openAI's large language models. 

from google import genai #type: ignore. 
"""
This imports the official google Gen AI client library for interacting with Google's Gemini models 
Im using this instead of openAI because i want to power my Saas with gemini free of charge. 
"""
app = FastAPI() 
#Instantiates/create your main web application - The app variable is what our web server like Uvicorn willl look for to run your api


@app.get("/api", response_class=PlainTextResponse)
"""
This is a decorator which converts the function below it into an API endpoint. So whenever someone visits the URL i've mentioned 
above, fastapi will automatically run this funcition and show them the result. 

@app.get("/api") - this will trigger when a user sends an HTTP GET request to the URL path /api
respopsne_class = PlainTextResponse ---> Tells fastapi to send back the function's output as back as 
plain text and not as a JSON object.
"""
def idea():
    #client = OpenAI()
    """
    This basically means logging into openAI - I am not going to type my API key into the code for security 
    I have it saved in my computer settings as OPEN_API_KEY

    When this code runs openAI will automatically find that hidden password, log me in and 
    let me use the AI
    """
    client = genai.Client()
    """
    This initialised gemini client - It automatically looks into environment variables for GEMINI_API_KEY, logs me 
    in securely behind the scenes and gets the system ready to use gemini. 
    """
    #prompt = [{"role": "user", "content": "Come up with a new business idea for AI Agents"}]
    #Message strucutre for the Ai 

    prompt = "Come up with a new business idea for AI agents"
    """
    OpenAI requires an array of structured 'role' dictionaries. But Gemini will let you pass a simple straightforward string
    directly
    """

    #response = client.chat.completions.create(model="gpt-5-nano", messages=prompt)
    """
    This is a network request to openAI's servers ---> It passes the model we want to use and the messages array 
    """
    #return response.choices[0].message.content
    """
    OpenAI returns a deeply nested data object because a single object can generate multiple answers. This line digs into 
    that object: 

    -- It looks into the list of answers (.choices)
    -- It grabs the very first answer ([0])
    --Access the  text message inside that choice (.message.content)
    ---It then return that string whicb fastapi returns to the user's browser or application as plain text. 
    """

    response = client.models.generate_content(
        model = "gemini-3.5-flash",
        contents = prompt
    )

    """
    This is a way if sebding a secure netwirk request to Google's API servers 
    """

    return response.text 
    """
    SDK wraps google's reply in a structured response object. Instead of 
    digging through multiple nested layers of choices like openAI, genAI SDK 
    provides a convenient '.text' helper property which extratss rthe palin text response immediately 
    """