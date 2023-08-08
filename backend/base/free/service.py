from typing import Dict, Any
import os


async def extract_form_data(form_data: Dict[str, Any], session_id: str) -> Dict[str, Any]:
    user_data = {session_id: {}}
    for key in ['childhood', 'relationship', 'mbti', 'working', 'summary', 'insight']:
        user_data[session_id][key] = form_data.get(key)
    return user_data


class FreeAppService:
    def __init__(self, openai, initial_prompt):
        self.openai = openai
        self.initial_prompt = initial_prompt

    async def format_prompt(self, user_data: Dict[str, Any]) -> str:
        main_string = self.initial_prompt
        formatted_prompt = main_string.format(**user_data)
        return formatted_prompt

    async def generate_response(self, message: str, conversation: list) -> tuple:
        categories = self.openai.Moderation.create(message)['results'][0]['categories']
        filtered_categories = [category for category in categories]
        if any(filtered_categories):
            return "I'm really sorry that you're feeling this way, but I'm unable to provide the help that you need. " \
                   "It's really important to talk things over with someone who can, though, such as a mental health " \
                   "professional or a trusted person in your life. You may also see our disclaimer for a crisis " \
                   "hotline. ", []

        try:
            response = self.openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=conversation
            )
        except Exception as e:
            print(e)
            return "Rate limit reached. Please add to journal.", []

        ai_message = response.choices[0].message['content']

        conversation.append({"role": "assistant", "content": ai_message})

        return ai_message, conversation
