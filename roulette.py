import discord
from discord.ext import commands


class Roulette(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.players = []


    @commands.command(name="روليت")
    async def roulette(self, ctx):

        embed = discord.Embed(
            title="🎰 روليت الطرد",
            description="اضغط الزر للدخول\n\n👥 المشاركين: 0",
            color=0xff0000
        )

        view = discord.ui.View(timeout=None)

        button = discord.ui.Button(
            label="دخول",
            emoji="🟢",
            style=discord.ButtonStyle.success
        )

        async def join_callback(interaction):
            user = interaction.user

            if user in self.players:
                await interaction.response.send_message(
                    "⚠️ أنت داخل الروليت مسبقاً",
                    ephemeral=True
                )
                return

            self.players.append(user)

            await interaction.response.send_message(
                "✅ دخلت بنجاح!",
                ephemeral=True
            )

        button.callback = join_callback
        view.add_item(button)

        await ctx.send(embed=embed, view=view)


async def setup(bot):
    await bot.add_cog(Roulette(bot))