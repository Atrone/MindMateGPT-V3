import os

import openai

openai.api_key = os.getenv("apikey")

async def summarize_text(text):
    prompt = f"Summarize the following text in 5 sentences:\n{text}"
    response = openai.Completion.create(
        engine="gpt-4",
        messages=[{"role": "user", "content": prompt}]
    )

    return response.choices[0].message.content


async def create_insights(text):
    prompt = f"Here is a completed therapy session:" \
             f"\n\n{text}\n\n " \
             f"For the above completed session, " \
             f"provide a summary of the session as well as expert level insights into what a good next step for " \
             f"the patient would be."
    response = openai.ChatCompletion.create(
        engine="gpt-4",
        messages=[{"role": "user", "content": prompt}]
    )

    return response.choices[0].message.content
