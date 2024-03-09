# Import the command handler
import aiohttp
import hikari
import lightbulb
import os
from dotenv import load_dotenv
load_dotenv()

print(os.environ)

# Instantiate a Bot instance
bot = lightbulb.BotApp(token=os.environ["DISCORD_TOKEN"], prefix="+", intents=hikari.Intents.ALL,)

@bot.listen(hikari.StartedEvent)
async def botStartup(event):
    print("Bot has started up!")


@bot.listen(lightbulb.CommandErrorEvent)
async def on_error(event: lightbulb.CommandErrorEvent) -> None:
    if isinstance(event.exception, lightbulb.CommandInvocationError):
        await event.context.respond(
            f"Something went wrong during invocation of command `{event.context.command.name}`.")
        raise event.exception

    # Unwrap the exception to get the original cause
    exception = event.exception.__cause__ or event.exception

    if isinstance(exception, lightbulb.NotOwner):
        await event.context.respond("You are not the owner of this bot.")
    elif isinstance(exception, lightbulb.CommandIsOnCooldown):
        await event.context.respond(
            f"This command is on cooldown for you {event.context.author.mention}. Try again in `{exception.retry_after:.2f}` seconds.")

@bot.listen()
async def on_starting(event: hikari.StartingEvent) -> None:
    bot.d.aio_session = aiohttp.ClientSession()


@bot.listen()
async def on_stopping(event: hikari.StoppingEvent) -> None:
    await bot.d.aio_session.close()

bot.load_extensions_from("./plugins/", must_exist=True)

# Run the bot
# Note that this is blocking meaning no code after this line will run
# until the bot is shut off
bot.run()
