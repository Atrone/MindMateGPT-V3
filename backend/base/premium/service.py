async def summarize_text(openai, text):
    prompt = f"Summarize the following text in 5 sentences:\n{text}"
    response = openai.Completion.create(
        engine="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3,
        max_tokens=3500,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=1
    )

    return response["choices"][0]["text"]


async def create_insights(openai, text):
    prompt = f"Here is a completed therapy session:" \
             f"\n\n{text}\n\n " \
             f"For the above completed session, " \
             f"provide a summary of the session as well as expert level insights into what a good next step for " \
             f"the patient would be."
    response = openai.ChatCompletion.create(
        engine="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.5,
        max_tokens=1000,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=1
    )

    return response["choices"][0]["text"]
