import discord
from discord.ext import commands


class AutoReply(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return

        text = message.content.lower()

        if text in [
            "السلام عليكم",
            "سلام عليكم",
            "السلام عليكم ورحمة الله"
        ]:
            await message.channel.send(
                f"وعليكم السلام ورحمة الله وبركاته {message.author.mention}"
            )

        await self.bot.process_commands(message)


async def setup(bot):
    await bot.add_cog(AutoReply(bot))