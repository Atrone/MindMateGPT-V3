import json
import os

from backend.app import check_key
from backend.base.app import BaseApp
from fastapi import Request

from backend.base.free.request_models import PaymentBody, GPTBody, KeyBody
from backend.base.free.service import FreeAppService, extract_form_data


class FreeApp(BaseApp):
    def __init__(self, redis_client, stripe, openai):
        super().__init__(redis_client, openai)
        self.stripe = stripe
        self.stripe.api_key = os.getenv("STRIPE_SECRET")
        self.initial_prompt = os.getenv("INITIAL_PROMPT")
        self.service = FreeAppService(openai, self.stripe, self.initial_prompt)

        @self.router.post("/getForm")
        async def get_form(request: Request):
            form_data = await request.form()
            session_id = request.headers['Session']
            user_data_key = f"user_data_{session_id}"
            user_data = await extract_form_data(form_data, session_id)
            user_data[session_id]['prompt'] = await self.service.format_prompt(user_data[session_id])
            user_data[session_id]['transcript'] = "This is a transcript"
            redis_client.set(user_data_key, json.dumps(user_data))
            return user_data[session_id]['first_name']

        @self.router.post("/therapistGPT")
        async def get_response(request: Request, body: GPTBody, key_body: KeyBody = KeyBody(key="INVAL")):
            session_id = request.headers['Session']
            user_data = await self.get_user_data(session_id)
            if "prompt" not in user_data[session_id] and "transcript" not in user_data[session_id]:
                user_data[session_id]['transcript'] = "This is a transcript"
                user_data[session_id]['prompt'] = self.initial_prompt
            user_data[session_id]['transcript'] += f"\n\n\n\n {body.message} \n\n\n\n"
            user_data[session_id]['prompt'] += f"\n\n\n\n {body.message} \n\n\n\n"
            result = await self.service.generate_response(user_data[session_id]['prompt'], await check_key(
                key_body.key, self.redis_client))
            user_data[session_id]['prompt'] += f"\n\n\n\n {result} \n\n\n\n"
            user_data[session_id]['transcript'] += f"\n\n\n\n {result} \n\n\n\n"
            redis_client.set(f"user_data_{session_id}", json.dumps(user_data))
            return result

        @self.router.post('/your-payment-endpoint')
        async def handle_payment(data: PaymentBody):
            result = await self.service.handle_payment(data.id, self.redis_client)
            return result
