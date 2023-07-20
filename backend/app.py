
import redis
from fastapi.staticfiles import StaticFiles
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import openai
import stripe
import random
import string
from fastapi import Request

from starlette.middleware.cors import CORSMiddleware
from starlette.responses import JSONResponse
from backend.auth.keys import HTTPKeyCheckBody, check_key
from backend.env.variables import load_environment
from backend.base.free.app import FreeApp
from backend.base.premium.app import PremiumApp

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
env_vars = load_environment()
openai.api_key = env_vars['OPENAI_API_KEY']
redis_url = env_vars["REDIS_URL"]
redis_client = redis.from_url(redis_url)


free_app = FreeApp(redis_client, stripe, openai)
premium_app = PremiumApp(redis_client, openai)

api_app.include_router(free_app.router)
api_app.include_router(premium_app.router)


@api_app.delete("/session/{session_id}")
async def delete_session(session_id: str):
    redis_client.delete(session_id)
    return JSONResponse(status_code=200, content={"message": "Session deleted"})


@api_app.post('/check-key')
async def check_key_route(keyCheck: HTTPKeyCheckBody):
    return await check_key(keyCheck.key, redis_client)


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    user = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(10))
    return templates.TemplateResponse("index.html", {"request": request, "user": user})
