from typing import Dict, Any
import os


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
        if any(word.lower() in [bad_word for bad_word in os.environ.get("badWords").split(", ")] for word in prompt.split(" ")): 
            return "I'm really sorry that you're feeling this way, but I'm unable to provide the help that you need. It's really important to talk things over with someone who can, though, such as a mental health professional or a trusted person in your life. You may also scroll down to our disclaimer for a crisis hotline"

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
            if "{" in response.choices[0].text or "}" in response.choices[0].text:
                response = self.openai.Completion.create(**completion_params)
        except:
            return "Rate limit reached. Please add to journal."

        return response.choices[0].text