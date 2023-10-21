import stripe
from fastapi import Request, Header
from backend.base.app import BaseApp
from backend.base.premium.request_models import InsightBody
from backend.tasks import send_email_task
from celery.result import AsyncResult
import os


class PremiumApp(BaseApp):
    def __init__(self, redis_client, openai):
        super().__init__(redis_client, openai)

        @self.router.post("/download")
        async def download_insights(request: Request, body: InsightBody):
            session_id = request.headers['Session']
            user_data = await self.get_user_data(session_id)

            message = user_data[session_id]['transcript'] + "\n\n\n\n"

            task = send_email_task.delay(body.recipient, message, user_data[session_id]['transcript'])
            return {"task_id": task.id}

        @self.router.get("/task_status/{task_id}")
        async def task_status(task_id: str):
            task = AsyncResult(task_id)
            if task.ready():
                return {"status": "completed", "result": task.result}
            return {"status": "pending"}

        @self.router.get("/payment_status/{payment_id}")
        async def get_payment_status(payment_id: str):
            return {"status": self.redis_client.get(self.get_user_data(payment_id),'pending')}

        @self.router.post("/webhook")
        async def webhook_received(request: Request, stripe_signature: str = Header(None)):
            session_id = request.headers['Session']
            webhook_secret = os.environ["STRIPE_WEBHOOK_SECRET"]
            data = await request.body()
            try:
                event = stripe.Webhook.construct_event(
                    payload=data,
                    sig_header=stripe_signature,
                    secret=webhook_secret
                )
            except Exception as e:
                return {"error": str(e)}

            event_type = event['type']
            if event_type == 'checkout.session.completed' or event_type == 'invoice.paid':
                print('success')
            elif event_type == 'invoice.payment_failed':
                print('invoice payment failed')
            else:
                print(f'unhandled event: {event_type}')
            self.redis_client[self.get_user_data(session_id)] = "completed"

            return {"status": "success"}
