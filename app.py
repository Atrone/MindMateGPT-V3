import json
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import redis
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import os

from starlette.middleware.cors import CORSMiddleware
from starlette.responses import JSONResponse

api_app = FastAPI(title="api app")

origins = [
    "http://localhost:8000",
    'https://mindmategpt.herokuapp.com/',
    'https://mindmategpt.com',
    'https://www.mindmategpt.com'

]

api_app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

import openai

openai.api_key = os.environ['apikey']
redis_url = os.getenv("REDIS_URL")
redis_client = redis.from_url(redis_url)


# user_data = {}

def summarize_text(text):
    prompt = f"Summarize the following text in 5 sentences:\n{text}"
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        temperature=0.3,
        max_tokens=150,  # = 112 words
        top_p=1,
        frequency_penalty=0,
        presence_penalty=1
    )

    return response["choices"][0]["text"]


def create_insights(text):
    prompt = f"Create expert level insights for this therapy session:\n{text}"
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        temperature=0.3,
        max_tokens=150,  # = 112 words
        top_p=1,
        frequency_penalty=0,
        presence_penalty=1
    )

    return response["choices"][0]["text"]


from fastapi import Request


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
    user_data[session_id]['growup'] = form_data.get('growup')
    user_data[session_id]['live'] = form_data.get('live')
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
                    f"Their criminal history, if any\n\nTheir religion\n\nWhere they grew up\n\nWhere they live\n\n" \
                    f"Their MBTI personality type\n\nTheir relationship to drugs and alcohol" \
                    f"\n---\n\nThis information is given in the prompt before the conversation." \
                    f"\n\nAct as the combination psychotherapist like I described before." \
                    f" DO NOT RECOMMEND GOING TO A REAL HUMAN FOR THERAPY. The patient may ask for details about you." \
                    f" Here are those details: your name is Mindy, you are female and" \
                    f" you live in America. You have dealt with mental health issues in the past and your own " \
                    f" experiences have" \
                    f" given you tremendous insight into mental illnesses' causes and solutions. Each message from you " \
                    f" and the patient will be separated by four new line characters and two spaces. " \
                    f" The patient will speak first. \n\n" \
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
                    f"{user_data[session_id]['mbti']}\n\nWhere they grew up: " \
                    f"{user_data[session_id]['growup']}\n\nWhere they live: " \
                    f"{user_data[session_id]['live']}\n\nTheir relationship to drugs and alcohol:  " \
                    f"{user_data[session_id]['drugs']}\n---\n"
    user_data[session_id]['transcript'] = ""
    redis_client.set(user_data_key, json.dumps(user_data))

    return user_data[session_id]['name']


@api_app.delete("/session/{session_id}")
async def delete_session(session_id: str):
    redis_client.delete(session_id)
    return JSONResponse(status_code=200, content={"message": "Session deleted"})


from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

app = FastAPI(title="main app")
app.mount("/api", api_app)
app.mount("/static", StaticFiles(directory="static", html=True), name="static")

origins = [
    "http://localhost:8000",
    'https://mindmategpt.herokuapp.com/',
    'https://mindmategpt.com',
    'https://www.mindmategpt.com'
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

templates = Jinja2Templates(directory="static")

import stripe
import random
import string

SENDER_EMAIL = os.getenv("SENDER_EMAIL")
SENDER_PASSWORD = os.getenv("SENDER_PASSWORD")

stripe.api_key = os.getenv("STRIPE_SECRET")


# Connect to Redis. Update these values with your Redis connection details.


def generate_key(length):
    # Generate a random alphanumeric key
    letters_and_digits = string.ascii_letters + string.digits
    return ''.join(random.choice(letters_and_digits) for _ in range(length))


@app.post('/your-payment-endpoint')
async def handle_payment(stripeToken: str):
    try:
        charge = stripe.Charge.create(
            amount=2000,  # amount in cents
            currency='usd',
            source=stripeToken,
            description='My first payment'
        )
        key = generate_key(5)
        # Store the key in Redis
        redis_client.set(key, 'true')
        return {"status": "success", "key": key}
    except Exception as e:
        return {"status": "error", "message": str(e)}


class KeyCheck(BaseModel):
    key: str


class CoreGPTBody(BaseModel):
    message: str
    key: str
    recipient: str = ""


@app.post('/check-key')
async def check_key(keyCheck: KeyCheck):
    # Check if the key exists in Redis
    try:
        if redis_client.exists(keyCheck.key):
            return {"status": "success", "message": "Valid key."}
        else:
            return {"status": "error", "message": "Invalid key."}
    except:
        return {"status": "error", "message": "Invalid key."}

@api_app.post("/download")
async def download_insights(body: CoreGPTBody, request: Request):
    key_check_result = await check_key(KeyCheck(key=body.key))
    print(key_check_result)
    if key_check_result['status'] == "success":
        session_id = request.headers['Session']
        user_data_key = f"user_data_{session_id}"
        user_data = redis_client.get(user_data_key)
        if user_data is None:
            user_data = {session_id: {}}
        else:
            user_data = json.loads(user_data)

        message = user_data[session_id]['transcript'] + "\n\n\n\n" + create_insights(user_data[session_id]['transcript'])
        subject = "Your Therapy Insights by MindMateGPT"

        try:
            # Create a multipart message and set headers
            msg = MIMEMultipart()
            msg["From"] = SENDER_EMAIL
            msg["To"] = body.recipient
            msg["Subject"] = subject

            # Add body to email
            msg.attach(MIMEText(message, "plain"))

            # Convert the message to a string
            text = msg.as_string()

            # Connect to the SMTP server
            server = smtplib.SMTP("smtp.gmail.com", 587)
            server.starttls()
            server.login(SENDER_EMAIL, SENDER_PASSWORD)

            # Send the email
            server.sendmail(SENDER_EMAIL, body.recipient, message)
            server.quit()

            return {"message": "Email sent successfully"}

        except Exception as e:
            return {"message": f"Failed to send email: {str(e)}"}


@api_app.post("/therapistGPT")
async def get_response(request: Request, body: CoreGPTBody):
    key_check_result = await check_key(KeyCheck(key=body.key))
    print(key_check_result)

    session_id = request.headers['Session']
    user_data_key = f"user_data_{session_id}"
    user_data = None
    if user_data is None:
        user_data = {session_id: {}}
    else:
        user_data = json.loads(user_data)

    user_data[session_id]['transcript'] += f"\n\n\n\n {body.message} \n\n\n\n"
    user_data[session_id]['prompt'] += f"\n\n\n\n {body.message} \n\n\n\n"
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
    except Exception as e:
        if key_check_result['status'] == "success":
            print('Youre in')
            user_data[session_id]['prompt'] = summarize_text(user_data[session_id]['prompt'])
            response = openai.Completion.create(
                model="text-davinci-003",
                prompt=user_data[session_id]['prompt'],
                temperature=0.9,
                max_tokens=824,
                top_p=1,
                frequency_penalty=0,
                presence_penalty=0.6
            )
        else:
            return "You have reached your session limit"
    user_data[session_id]['prompt'] += f"\n\n\n\n {response.choices[0].text} \n\n\n\n"
    result = response.choices[0].text
    redis_client.set(user_data_key, json.dumps(user_data))
    return result


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    user = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(10))
    return templates.TemplateResponse("index.html", {"request": request, "user": user})
