import discord
from discord.ext import commands
import random
import json
import os


class Roulette(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.players = []
        self.reward = 0
        self.file = "points.json"


    def load_points(self):
        if not os.path.exists(self.file):
            return {}

        with open(self.file, "r", encoding="utf-8") as f:
            return json.load(f)


    def save_points(self, data):
        with open(self.file, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)


    @commands.command(name="روليت")
    async def roulette(self, ctx, amount: int = None):

        if amount is None:
            await ctx.send("❌ اكتب قيمة الجائزة\nمثال: `-روليت 50`")
            return

        self.players = []
        self.reward = amount

        embed = discord.Embed(
            title="🎰 روليت النقاط",
            description=f"""
🏆 الجائزة: **{amount} نقطة**

اضغط دخول للمشاركة

👥 المشاركين: 0
""",
            color=0xff0000
        )

        view = discord.ui.View(timeout=60)

        join = discord.ui.Button(
            label="دخول",
            emoji="🟢",
            style=discord.ButtonStyle.success
        )

        start = discord.ui.Button(
            label="بدء الروليت",
            emoji="🎰",
            style=discord.ButtonStyle.primary
        )


        async def join_callback(interaction):

            if interaction.user in self.players:
                await interaction.response.send_message(
                    "⚠️ أنت داخل مسبقاً",
                    ephemeral=True
                )
                return

            self.players.append(interaction.user)

            await interaction.response.send_message(
                "✅ دخلت بنجاح!",
                ephemeral=True
            )


        async def start_callback(interaction):

            if len(self.players) < 3:
                await interaction.response.send_message(
                    "❌ يحتاج الروليت 3 لاعبين أو أكثر",
                    ephemeral=True
                )
                return

            winner = random.choice(self.players)

            data = self.load_points()
            user = str(winner.id)

            if user not in data:
                data[user] = 0

            data[user] += self.reward
            self.save_points(data)

            await interaction.response.send_message(
                f"🎉 مبروك {winner.mention}\n"
                f"🏆 فزت بـ **{self.reward} نقطة**!"
            )

            self.players.clear()


        join.callback = join_callback
        start.callback = start_callback

        view.add_item(join)
        view.add_item(start)

        await ctx.send(embed=embed, view=view)


async def setup(bot):
    await bot.add_cog(Roulette(bot))
