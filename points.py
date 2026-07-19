import discord
from discord.ext import commands
import json
import os

class Points(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.file = "points.json"

        if not os.path.exists(self.file):
            with open(self.file, "w", encoding="utf-8") as f:
                json.dump({}, f)

    def load_points(self):
        with open(self.file, "r", encoding="utf-8") as f:
            return json.load(f)

    def save_points(self, data):
        with open(self.file, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)

    @commands.command(name="نقاطي")
    async def my_points(self, ctx):
        data = self.load_points()
        user = str(ctx.author.id)

        if user not in data:
            data[user] = 0
            self.save_points(data)

        await ctx.send(f"💰 | {ctx.author.mention} لديك **{data[user]}** نقطة.")

    @commands.command(name="اعطاء")
    @commands.has_permissions(administrator=True)
    async def add_points(self, ctx, member: discord.Member, amount: int):
        data = self.load_points()
        user = str(member.id)

        if user not in data:
            data[user] = 0

        data[user] += amount
        self.save_points(data)

        await ctx.send(f"✅ تم إضافة **{amount}** نقطة إلى {member.mention}")

    @commands.command(name="سحب")
    @commands.has_permissions(administrator=True)
    async def remove_points(self, ctx, member: discord.Member, amount: int):
        data = self.load_points()
        user = str(member.id)

        if user not in data:
            data[user] = 0

        data[user] = max(0, data[user] - amount)
        self.save_points(data)

        await ctx.send(f"❌ تم سحب **{amount}** نقطة من {member.mention}")

async def setup(bot):
    await bot.add_cog(Points(bot))
