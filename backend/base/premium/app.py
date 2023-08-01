from fastapi import Request
from backend.auth.keys import check_key
from backend.base.app import BaseApp
from backend.base.premium.service import create_insights
from backend.base.premium.request_models import InsightBody
from backend.tasks import send_email_task


class PremiumApp(BaseApp):
    def __init__(self, redis_client, openai):
        super().__init__(redis_client, openai)

        @self.router.post("/download")
        async def download_insights(request: Request, body: InsightBody):
            if await check_key(body.key, self.redis_client):
                session_id = request.headers['Session']
                user_data = await self.get_user_data(session_id)

                message = user_data[session_id]['transcript'] + "\n\n\n\n"

                send_email_task.delay(body.recipient, message, self.openai, user_data[session_id]['transcript'])
                return "sent"
            else:
                return None
