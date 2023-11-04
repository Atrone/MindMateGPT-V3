import stripe
from fastapi import Request, Header
from backend.base.app import BaseApp
import os


class PaymentApp(BaseApp):

    def __init__(self, redis_client, openai):
        super().__init__(redis_client, openai)

        @self.router.get("/payment_status")
        async def get_payment_status():
            return {"status": redis_client.get("PAYMENT") if redis_client.get("PAYMENT") else "pending"}

        @self.router.post("/webhook")
        async def webhook_received(request: Request, stripe_signature: str = Header(None)):
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
            print(event_type)
            if event_type == 'checkout.session.completed':
                print('success')
                redis_client.set("PAYMENT", "completed", ex=60)
            elif event_type == 'invoice.payment_failed':
                print('invoice payment failed')
            else:
                print(f'unhandled event: {event_type}')
            return {"status": "completed"}
