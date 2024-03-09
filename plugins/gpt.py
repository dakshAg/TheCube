import re, datetime, hashlib, os
import hikari, lightbulb
import google.generativeai as genai

plugin = lightbulb.Plugin("GPT")

genai.configure(api_key=os.environ["GEMINI_API_KEY"])

# Set up the model
generation_config = {
    "temperature": 1,
    "top_p": 1,
    "top_k": 1,
    "max_output_tokens": 2000,
}

safety_settings = [
    {
        "category": "HARM_CATEGORY_HARASSMENT",
        "threshold": "BLOCK_ONLY_HIGH"
    },
    {
        "category": "HARM_CATEGORY_HATE_SPEECH",
        "threshold": "BLOCK_ONLY_HIGH"
    },
    {
        "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
        "threshold": "BLOCK_ONLY_HIGH"
    },
    {
        "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
        "threshold": "BLOCK_ONLY_HIGH"
    },
]

model = genai.GenerativeModel(model_name="gemini-pro",
                              generation_config=generation_config,
                              safety_settings=safety_settings)
@plugin.listener(hikari.GuildMessageCreateEvent)
async def main(event) -> None:
    print("Event received")
    if event.is_bot or not event.content:
        return
    mentioned_ids = event.message.user_mentions_ids
    if plugin.bot.application.id not in mentioned_ids:
        return
    messageContent = event.content
    prompt_parts = [
        f"You're a super intelligent but abstract chat bot hosted on discord. "
        f"Don't name yourself, but if someone ever asked, you're The Cube. "
        f"You are made by the Universe to help all data science students at The University of Melbourne "
        f"Keep it sharp and SHORT, no need for a full paragraph. <user>{messageContent}</user>"
    ]

    response = model.generate_content(prompt_parts)

    if response.candidates[0].finish_reason != 1:
        await event.message.respond("Too NSFW to say", user_mentions=True, reply=True)
        return

    await event.message.respond(response.text, user_mentions=True, reply=True)


def load(bot: lightbulb.BotApp) -> None:
    bot.add_plugin(plugin)