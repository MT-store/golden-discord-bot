import discord
from discord.ext import commands

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="-", intents=intents)

@bot.event
async def on_ready():
    print(f"تم تشغيل البوت: {bot.user}")

bot.load_extension("points")

bot.run("MTUyODEyMzMzODkxNDc5MTU2NA.G2EPyQ.C1RtDQJfQ6ICjJgdKCaGMyvHA7dG83Exs6BChE")
