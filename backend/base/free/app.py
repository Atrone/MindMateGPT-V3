import json
import os
import time

from backend.base.app import BaseApp
from fastapi import Request

from backend.base.free.request_models import GPTBody
from backend.base.free.service import FreeAppService, extract_form_data


class FreeApp(BaseApp):
    def __init__(self, redis_client, openai):
        super().__init__(redis_client, openai)
        self.initial_prompt = os.getenv("INITIAL_PROMPT")
        self.service = FreeAppService(openai, self.initial_prompt)

        @self.router.post("/getForm")
        async def get_form(request: Request):
            form_data = await request.form()
            session_id = request.headers['Session']
            user_data_key = f"user_data_{session_id}"
            user_data = await extract_form_data(form_data, session_id)
            content = await self.service.format_prompt(user_data[session_id])
            conversation = [{"role": "system", "content": content}]
            user_data[session_id]['prompt'] = json.dumps(conversation)
            user_data[session_id]['transcript'] = "This is a transcript"
            redis_client.set(user_data_key, json.dumps(user_data))
            return user_data[session_id]

        @self.router.post("/therapistGPT")
        async def get_response(request: Request, body: GPTBody):
            session_id = request.headers['Session']
            user_data = await self.get_user_data(session_id)
            if "prompt" not in user_data[session_id] and "transcript" not in user_data[session_id]:
                conversation = [{"role": "system", "content": self.initial_prompt}]
                user_data[session_id]['transcript'] = "This is a transcript"
                user_data[session_id]['prompt'] = json.dumps(conversation)
            conversation = json.loads(user_data[session_id]['prompt'])
            conversation.append({"role": "user", "content": body.message})
            user_data[session_id]['prompt'] = json.dumps(conversation)
            user_data[session_id]['transcript'] += f"\n\n\n\n {body.message} \n\n\n\n"
            result, conversation = await self.service.generate_response(body.message, conversation)
            user_data[session_id]['prompt'] = json.dumps(conversation)
            user_data[session_id]['transcript'] += f"\n\n\n\n {result} \n\n\n\n"
            redis_client.set(f"user_data_{session_id}", json.dumps(user_data))
            return result
