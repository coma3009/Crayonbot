import io
import asyncio
import discord
import random
import asyncio
import random
import datetime
import config
import discord
from discord import errors
from discord.ext import commands
from discord.ext import commands
class general(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def hellothisisverification(self, ctx):
        await ctx.send("Coma#3009")
    @commands.command(name="개발자")
    async def modelf(self, ctx):
        embed=discord.Embed(title="개발자", description="RYZEN#3009", colour=discord.Colour.random())
        await ctx.reply(embed=embed)
    @commands.command(
        name = "핑"
    )
    async def ping(self, ctx):
        await ctx.send(embed = discord.Embed(title = "**Pong!**", description = f":ping_pong: {round(self.bot.latency) * 1000}ms", color= 0x0000ff))
    @commands.command(name="출처")
    async def chul(self, ctx):
        embed=discord.Embed(title="깃헙", description=f"[서포트서버](https://discord.gg/Jk6VRvsnqa) \n[짱구봇 초대](https://discord.com/api/oauth2/authorize?client_id=915546504054333450&permissions=8&scope=bot) \n옵션&생일&입장메시지&메일&레벨링&초대정보&하트인증등의 코드는 팀에서 개발된 하린봇의 코드를 사용했음을 알려드립니다. \n[하린봇깃헙](https://github.com/spacedev-official/harin)", colour=discord.Colour.random())
        await ctx.send(embed=embed)
def setup(bot):
    bot.add_cog(general(bot))
