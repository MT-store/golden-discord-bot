import discord
from discord.ext import commands
import os

from flask import Flask
from threading import Thread


app = Flask(__name__)


@app.route("/")
def home():
    return "Bot is running"


def run():
    app.run(
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 10000))
    )


Thread(target=run).start()


intents = discord.Intents.default()
intents.message_content = True
intents.members = True


class MyBot(commands.Bot):

    async def setup_hook(self):
        await self.load_extension("points")
        await self.load_extension("auto_reply")
        await self.load_extension("roulette")


bot = MyBot(
    command_prefix="-",
    intents=intents
)


@bot.event
async def on_ready():
    print(f"تم تشغيل البوت: {bot.user}")


print("جاري تشغيل البوت...")


bot.run(os.environ["TOKEN"])
