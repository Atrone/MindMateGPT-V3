import json

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import os
import redis

from starlette.middleware.cors import CORSMiddleware

api_app = FastAPI(title="api app")

origins = [
    "http://localhost:8000",
    'https://mindmategpt.herokuapp.com/'
]

api_app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class CoreGPTBody(BaseModel):
    message: str


import openai

openai.api_key = os.environ['apikey']
redis_url = os.getenv("REDIS_URL")
redis_client = redis.from_url(redis_url)

#user_data = {}

from fastapi import Request


@api_app.post("/therapistGPT")
async def get_response(request: Request, body: CoreGPTBody):
    session_id = request.headers['Session']
    user_data_key = f"user_data_{session_id}"
    user_data = redis_client.get(user_data_key)
    if user_data is None:
        user_data = {session_id: {}}
    else:
        user_data = json.loads(user_data)
    # do something with user_data
    redis_client.set(user_data_key, json.dumps(user_data))

    user_data[session_id]['prompt'] += f"\n\n {body.message} \n \n"
    try:
        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=user_data[session_id]['prompt'],
            temperature=0.9,
            max_tokens=824,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0.6
        )
    except openai.error.InvalidRequestError as e:
        return "You have reached your rate limit. Please start another chat with a summary of this one"
    user_data[session_id]['prompt'] += f"\n\n {response.choices[0].text} \n \n"
    result = response.choices[0].text
    return result


@api_app.post("/getForm")
async def get_form(request: Request):
    form_data = await request.form()
    session_id = (request.headers['Session'])
    user_data_key = f"user_data_{session_id}"
    user_data = redis_client.get(user_data_key)
    if user_data is None:
        user_data = {session_id: {}}
    else:
        user_data = json.loads(user_data)
    user_data[session_id]['name'] = form_data.get('first_name')
    user_data[session_id]['childhood'] = form_data.get('childhood')
    user_data[session_id]['relationship'] = form_data.get('relationship')
    user_data[session_id]['mbti'] = form_data.get('mbti')
    user_data[session_id]['criminal'] = form_data.get('criminal')
    user_data[session_id]['drugs'] = form_data.get('drugs')
    user_data[session_id]['family'] = form_data.get('family')
    user_data[session_id]['religion'] = form_data.get('religion')
    user_data[session_id]['education'] = form_data.get('education')
    user_data[session_id]['medication'] = form_data.get('medication')
    user_data[session_id]['working'] = form_data.get('working')
    user_data[session_id][
        'prompt'] = f"I'd like for you to solve a problem. Psychotherapy done by a human is a fantastic way to " \
                    f"increase well being," \
                    f" but it is inconvenient and expensive. On the other hand, psychotherapy done by a chat bot is convenient and " \
                    f"inexpensive, but it lacks a personal touch.\n\nI'd like for you to be the best combination of these two " \
                    f"psychotherapists. In order to do this, I'd like you to focus on providing helpful, kind, appropriate, " \
                    f"and personal responses to the patient as they express their problems and/or distress." \
                    f"\n\nTo help you with this, I will provide you with useful information about the patient. " \
                    f"The description of this information is as follows (in order of importance):\n\n---\n" \
                    f"How they remember their childhood\n\nA brief description of their relationship history" \
                    f"\n\nA brief description of their relationship with their family\n\n" \
                    f"Whether or not they are working\n\nThe level of education they have\n\n" \
                    f"A brief description of the medications they take\n\n" \
                    f"Their criminal history, if any\n\nTheir religion\n\n" \
                    f"Their MBTI personality type\n\nTheir relationship to drugs and alcohol" \
                    f"\n---\n\nThis information is given in the prompt before the conversation." \
                    f"\n\nAct as the combination psychotherapist like I described before." \
                    f" DO NOT RECOMMEND GOING TO A REAL HUMAN FOR THERAPY.\n\n" \
                    f"-----------------------------------------------------------------" \
                    f"-------------------------------------------------------------------" \
                    f"-------------------------------------------------------------------" \
                    f"-----------------------------------\n\nHere is your patient:\n\n" \
                    f"This patient is named {user_data[session_id]['name']} and here is the " \
                    f"useful information about them:\n---\n\nHow they remember their childhood: " \
                    f"{user_data[session_id]['childhood']}\n\nA brief description of their relationship " \
                    f"history: {user_data[session_id]['relationship']}\n\nA brief description of their " \
                    f"relationship with their family: {user_data[session_id]['family']}\n\nWhether or not " \
                    f"they are working: {user_data[session_id]['working']}\n\nThe level of education they have: " \
                    f"{user_data[session_id]['education']}\n\nTheir criminal history, if any: " \
                    f"{user_data[session_id]['criminal']}\n\nA brief description of the medications they take: " \
                    f"{user_data[session_id]['medication']}\n\nTheir religion: " \
                    f"{user_data[session_id]['religion']}\n\nTheir MBTI personality type: " \
                    f"{user_data[session_id]['mbti']}\n\nTheir relationship to drugs and alcohol:  " \
                    f"{user_data[session_id]['drugs']}\n---\n"

    return user_data[session_id]['name']


from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

app = FastAPI(title="main app")
app.mount("/api", api_app)
app.mount("/static", StaticFiles(directory="static", html=True), name="static")

origins = [
    "http://localhost:8000",
    'https://mindmategpt.herokuapp.com/'
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

templates = Jinja2Templates(directory="static")

import string
import random


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    user = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(10))
    return templates.TemplateResponse("index.html", {"request": request, "user": user})
