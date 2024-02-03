from typing import Dict, Any, Union
import re
import urllib.parse
from dataclasses import fields

from backend.base.entities import UserSessionData


async def extract_details_from_last_session_string(last_session_string: str) -> tuple[str, str]:
    decoded_string = urllib.parse.unquote(last_session_string).lower()

    # Find the summary
    pattern = r"summary(.*?)insight"
    summary_to_insights = re.search(pattern, decoded_string, re.DOTALL)
    if summary_to_insights:
        summary = summary_to_insights.group(1).strip()

        insights = decoded_string.find("insight")

        insights = decoded_string[insights + len("insight"):].strip()
        return summary, insights
    else:
        return "", ""


async def extract_form_data(form_data: Dict[str, Any]) -> Dict[str, Any]:
    user_data = {}
    keys = [f.name.lower() for f in fields(UserSessionData)]
    for key in keys:
        if form_data.get(key):
            user_data[key] = form_data.get(key)
    return user_data


class FreeAppService:
    def __init__(self, openai, initial_prompt):
        self.openai = openai
        self.initial_prompt = initial_prompt

    async def format_prompt(self, user_data: UserSessionData) -> str:
        main_string = self.initial_prompt
        formatted_prompt = main_string.format(**user_data.to_dict())
        return formatted_prompt

    async def generate_response(self, message: str, conversation: list) -> tuple:
        try:
            if self.openai.Moderation.create(message)['results'][0]['flagged']:
                return "I'm really sorry that you're feeling this way, but I'm unable to provide the help that you " \
                       "need. " \
                       "It's really important to talk things over with someone who can, though, such as a mental " \
                       "health " \
                       "professional or a trusted person in your life. You may also see our disclaimer for a crisis " \
                       "hotline. ", conversation
        except Exception as e:
            print(e)
            return "Something is wrong with our AI provider", []
        try:
            response = self.openai.ChatCompletion.create(
                model="gpt-3.5-turbo-0125",
                messages=conversation
            )
        except Exception as e:
            print(e)
            return "Rate limit reached. Please add to journal.", []

        ai_message = response.choices[0].message['content']

        conversation.append({"role": "assistant", "content": ai_message})

        return ai_message, conversation
