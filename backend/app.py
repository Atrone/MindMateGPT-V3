from urllib.parse import urlparse

import redis
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import openai
from ssl import CERT_NONE
import random
import string
from fastapi import Request

from starlette.middleware.cors import CORSMiddleware
from starlette.responses import JSONResponse, FileResponse

from backend.base.payment.app import PaymentApp
from backend.env.variables import load_environment
from backend.base.free.app import FreeApp
from backend.base.premium.app import PremiumApp

from fastapi import FastAPI

api_app = FastAPI(title="api app")

origins = [
    "http://localhost:8000",
    'https://mindmategpt.herokuapp.com/',
    'https://mindmategpt.com',
    'https://www.mindmategpt.com'

]

cors = {"middleware_class": CORSMiddleware,
        "allow_origins": origins,
        "allow_credentials": True,
        "allow_methods": ['*'],
        "allow_headers": ['*']}

api_app.add_middleware(**cors)

import os

PARENT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STATIC_DIR = os.path.join(PARENT_DIR, 'static')


app = FastAPI(title="main app")
app.mount("/api", api_app)
app.mount("/static", StaticFiles(directory=STATIC_DIR, html=True), name="static")

origins = [
    "http://localhost:8000",
    'https://mindmategpt.herokuapp.com/',
    'https://mindmategpt.com',
    'https://www.mindmategpt.com'
]

app.add_middleware(**cors)

templates = Jinja2Templates(directory="static")

env_vars = load_environment()

# Backend-wide shared data
openai.api_key = env_vars['OPENAI_API_KEY']
redis_url = env_vars["REDIS_URL"]

if "redis://localhost:6379" == redis_url:
    ssl_var = False
else:
    ssl_var = True
parsed_url = urlparse(redis_url)

redis_client = redis.Redis(
    host=parsed_url.hostname,
    port=parsed_url.port,
    password=parsed_url.password,
    ssl=ssl_var,  # CHANGE TO FALSE FOR LOCAL
    ssl_cert_reqs=CERT_NONE
)

free_app = FreeApp(redis_client, openai)
premium_app = PremiumApp(redis_client, openai)
payment_app = PaymentApp(redis_client, openai)

api_app.include_router(free_app.router)
api_app.include_router(premium_app.router)
api_app.include_router(payment_app.router)


@api_app.delete("/session/{session_id}")
async def delete_session(session_id: str):
    redis_client.delete(session_id)
    return JSONResponse(status_code=200, content={"message": "Session deleted"})

@app.get("/ads.txt", response_class=FileResponse)
async def read_ads_txt():
    return FileResponse("static/ads.txt",media_type="text/plain")


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    user = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(10))
    return templates.TemplateResponse("index.html", {"request": request, "user": user})
