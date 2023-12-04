import json
import os

from backend.base.app import BaseApp
from fastapi import Request

from backend.base.entities import UserSessionData, PersistentUserData
from backend.base.free.request_models import GPTBody
from backend.base.free.service import FreeAppService, extract_form_data, \
     extract_details_from_last_session_string


class FreeApp(BaseApp):
    def __init__(self, redis_client, openai):
        super().__init__(redis_client, openai)
        self.initial_prompt = os.getenv("INITIAL_PROMPT")
        self.service = FreeAppService(openai, self.initial_prompt)

        @self.router.post("/getForm")
        async def get_form(request: Request):
            form_data = dict(await request.form())
            persistent_user_data = PersistentUserData(last_session=request.headers.get('taskResult',""),
                                                      mbti=request.cookies.get('mbti', ""))
            form_data['summary'], form_data['insight'] = \
                await extract_details_from_last_session_string(persistent_user_data.last_session)
            form_data['mbti'] = persistent_user_data.mbti

            user_data_dict = await extract_form_data(form_data)
            user_data = UserSessionData(**user_data_dict)

            content = await self.service.format_prompt(user_data)
            conversation = [{"role": "system", "content": content}]
            user_data.prompt = json.dumps(conversation)
            user_data.transcript = "This is a transcript"

            try:
                if redis_client.get(f"user_data_{request.headers['Session']}") is None:
                    redis_client.set(f"user_data_{request.headers['Session']}", json.dumps(user_data.__dict__), ex=24 * 60 * 60)
            except Exception as e:
                print(e)
                return user_data.__dict__
            return user_data.__dict__

        @self.router.post("/therapistGPT")
        async def get_response(request: Request, body: GPTBody):
            user_data = await self.get_user_data_dataclass(request.headers['Session'])
            if not user_data.prompt and not user_data.transcript:
                conversation = [{"role": "system", "content": self.initial_prompt}]
                user_data.transcript = "This is a transcript"
                user_data.prompt = json.dumps(conversation)
            conversation = json.loads(user_data.prompt)
            conversation.append({"role": "user", "content": body.message})
            user_data.prompt = json.dumps(conversation)
            user_data.transcript += f"\n\n\n\n {body.message} \n\n\n\n"

            result, conversation = await self.service.generate_response(body.message, conversation)
            user_data.prompt = json.dumps(conversation)
            user_data.transcript += f"\n\n\n\n {result} \n\n\n\n"
            try:
                redis_client.set(f"user_data_{request.headers['Session']}", json.dumps(user_data.__dict__), ex=24 * 60 * 60)
            except Exception as e:
                print(e)
                return result
            return result
