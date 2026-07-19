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

        await ctx.send(
            f"💰 | {ctx.author.mention} لديك **{data[user]}** نقطة."
        )

    @commands.command(name="اعطاء")
    @commands.has_permissions(administrator=True)
    async def add_points(self, ctx, member: discord.Member, amount: int):
        data = self.load_points()
        user = str(member.id)

        if user not in data:
            data[user] = 0

        data[user] += amount
        self.save_points(data)

        await ctx.send(
            f"✅ تم إضافة **{amount}** نقطة إلى {member.mention}"
        )

    @commands.command(name="سحب")
    @commands.has_permissions(administrator=True)
    async def remove_points(self, ctx, member: discord.Member, amount: int):
        data = self.load_points()
        user = str(member.id)

        if user not in data:
            data[user] = 0

        data[user] = max(0, data[user] - amount)
        self.save_points(data)

        await ctx.send(
            f"❌ تم سحب **{amount}** نقطة من {member.mention}"
        )

    @commands.command(name="توب")
    async def top_points(self, ctx):
        data = self.load_points()

        if not data:
            await ctx.send("📭 لا يوجد لاعبين لديهم نقاط.")
            return

        top = sorted(
            data.items(),
            key=lambda x: x[1],
            reverse=True
        )[:10]

        embed = discord.Embed(
            title="🏆 توب النقاط",
            description="أفضل 10 لاعبين",
            color=0xffd700
        )

        for i, (user_id, points) in enumerate(top, start=1):
            user = self.bot.get_user(int(user_id))

            name = user.name if user else "مستخدم"

            embed.add_field(
                name=f"#{i} {name}",
                value=f"💰 النقاط: **{points}**",
                inline=False
            )

        embed.set_footer(
            text=f"طلب بواسطة {ctx.author.name}"
        )

        await ctx.send(embed=embed)


async def setup(bot):
    await bot.add_cog(Points(bot))
