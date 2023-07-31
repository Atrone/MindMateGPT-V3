from typing import Dict, Any
import os
from backend.auth.keys import generate_key
from backend.base.premium.service import summarize_text


async def extract_form_data(form_data: Dict[str, Any], session_id: str) -> Dict[str, Any]:
    user_data = {session_id: {}}
    for key in ['childhood', 'relationship', 'mbti', 'working']:
        user_data[session_id][key] = form_data.get(key)
    return user_data


class FreeAppService:
    def __init__(self, openai, stripe, initial_prompt):
        self.openai = openai
        self.stripe = stripe
        self.initial_prompt = initial_prompt

    async def format_prompt(self, user_data: Dict[str, Any]) -> str:
        main_string = self.initial_prompt
        formatted_prompt = main_string.format(**user_data)
        return formatted_prompt

    async def generate_response(self, prompt: str, key_check_result: Dict[str, Any] = None) -> str:
        if any(word in os.environ.get("badWords") for word in prompt[len(self.initial_prompt):].split(" ")): 
            return "I'm really sorry that you're feeling this way, but I'm unable to provide the help that you need. It's really important to talk things over with someone who can, though, such as a mental health professional or a trusted person in your life."

        # Common settings for the Completion.create
        completion_params = {
            "model": "text-davinci-003",
            "prompt": prompt,
            "temperature": 0.9,
            "max_tokens": 824,
            "top_p": 1,
            "frequency_penalty": 0,
            "presence_penalty": 0.6
        }

        try:
            response = self.openai.Completion.create(**completion_params)
        except:
            completion_params['prompt'] = await summarize_text(self.openai, prompt)
            response = self.openai.Completion.create(**completion_params)

        return response.choices[0].text

    async def handle_payment(self, payment_id: str, redis_client) -> Dict:
        try:
            # Create a PaymentIntent with the amount and currency
            payment_intent = self.stripe.PaymentIntent.create(
                amount=2000,  # amount in cents
                currency='usd',
                payment_method=payment_id,
                confirm=True,  # Automatically confirm the payment
                description='My first payment',
            )

            if payment_intent.status == 'succeeded':
                key = generate_key(5)
                # Store the key in Redis
                redis_client.set(key, 'true')
                return f"Here is your key: {key}. " \
                       f"IMPORTANT: Please store this key for future use. You input it to access the premium features."
            else:
                return {"status": "error", "message": "Payment failed"}

        except Exception as e:
            return {"status": "error", "message": str(e)}
