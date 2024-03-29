from fastapi import Request
from backend.base.app import BaseApp
from backend.base.entities import UserSessionData
from backend.base.premium.request_models import InsightBody, AnalysisBody
from backend.tasks import send_email_task, send_email_task2
from celery.result import AsyncResult


class PremiumApp(BaseApp):

    def __init__(self, redis_client, openai):
        super().__init__(redis_client, openai)

        @self.router.post("/api/download")
        async def download_insights(request: Request, body: InsightBody):
            session_id = request.headers['Session']
            user_data_dict = await self.get_user_data_dict(session_id)
            user_data = UserSessionData(**user_data_dict)
            message = user_data.transcript + "\n\n\n\n"

            task = send_email_task.delay(body.recipient, message, user_data.transcript)
            return {"task_id": task.id}

        @self.router.post("/api/downloadAnalysis")
        async def download_insights(request: Request, body: AnalysisBody):
            session_id = request.headers['Session']
            user_data_dict = await self.get_user_data_dict(session_id)
            user_data = UserSessionData(**user_data_dict)
            message = user_data.transcript + "\n\n\n\n" + body.journals

            task = send_email_task2.delay(body.recipient, message)
            return {"task_id": task.id}

        @self.router.get("/api/task_status/{task_id}")
        async def task_status(task_id: str):
            task = AsyncResult(task_id)
            if task.ready():
                return {"status": "completed", "result": task.result}
            return {"status": "pending"}
