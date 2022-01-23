from dis import disco
from os import name
import discord
from discord import message
from discord import embeds
from discord.ext import commands
import aiosqlite
import os
import emoji
import psutil
import random
import asyncio
import traceback
import datetime
import time

from discord_components import Button, ButtonStyle, SelectOption, Select, component
from discord.ext.commands.core import Command, command


class game(commands.Cog, name = "게임 명령어", description = "게임 명령어 Cog입니다."):
    def __init__(self, bot):
        self.bot = bot
    async def cog_before_invoke(self, ctx: commands.Context):
        print(ctx.command)
        if ctx.command.name != '메일':
            database = await aiosqlite.connect("db/db.sqlite")
            cur = await database.execute(
                'SELECT * FROM uncheck WHERE user_id = ?', (ctx.author.id,)
            )

            if await cur.fetchone() is None:
                cur = await database.execute("SELECT * FROM mail")
                mails = await cur.fetchall()
                check = sum(1 for _ in mails)
                mal = discord.Embed(
                    title=f'📫짱구의 메일함 | {check}개 수신됨',
                    description="아직 읽지 않은 메일이 있어요.'`짱구야 메일`'로 확인하세요.\n주기적으로 메일함을 확인해주세요! 소소한 업데이트 및 이벤트개최등 여러소식을 확인해보세요.",
                    colour=ctx.author.colour,
                )

                return await ctx.send(embed=mal)
            cur = await database.execute('SELECT * FROM mail')
            mails = await cur.fetchall()
            check = sum(1 for _ in mails)
            # noinspection DuplicatedCode
            cur = await database.execute("SELECT * FROM uncheck WHERE user_id = ?", (ctx.author.id,))
            # noinspection DuplicatedCode
            check2 = await cur.fetchone()
            if str(check) != str(check2[1]):
                mal = discord.Embed(
                    title=f'📫짱구의 메일함 | {int(check) - int(check2[1])}개 수신됨',
                    description="아직 읽지 않은 메일이 있어요.'`짱구야 메일`'로 확인하세요.\n주기적으로 메일함을 확인해주세요! 소소한 업데이트 및 이벤트개최등 여러소식을 확인해보세요.",
                    colour=ctx.author.colour,
                )

                await ctx.send(embed=mal)
    @commands.command(
        name = "가위바위보"
    )
    async def rsp_cmd(self, ctx):
        try:
            m = await ctx.send(f"<@{ctx.author.id}> 안 내면 진다 가위 바위 보", components = [
                [
                    Button(label = "가위", emoji="✌", style=ButtonStyle.green, id="gawi"),
                    Button(label = "바위", emoji="✊", style=ButtonStyle.green, id="qkdnl"),
                    Button(label = "보", emoji="🖐", style=ButtonStyle.green, id="qh"),
                    Button(label = "취소", emoji = "❌", style = ButtonStyle.red, id = "cancel"),
                ]
            ])
            def check(res):
                return res.user == ctx.author and res.channel == ctx.channel
            
            try:
                res = await self.bot.wait_for("button_click", check = check, timeout = 25)
                if res.component.id == "cancel":
                    return await m.edit(embed = discord.Embed(title = "가위바위보 취소", description = "나랑 가위바위보 안해줄꺼야?.......", colour=discord.Colour.red()), components = [])
            except asyncio.TimeoutError:
                await m.edit(f'<@{ctx.author.id}>\n 어? 안냈내? 내가 이겨따!!^^', components = [])
            else:
                if res.component.id == "gawi":
                    a = ['가위','보','바위']
                    c = random.choice(a)
                    if c == '가위':
                        embed = discord.Embed(title=f"쳇. 비겼네......;;",color=discord.Colour.green(), timestamp=ctx.message.created_at)
                        embed.add_field(name=f"{ctx.author}", value=f"가위✌", inline=True)
                        embed.add_field(name=f"{self.bot.user.name}", value=f"가위✌", inline=True)
                        embed.set_footer(text=f"{ctx.author}", icon_url=ctx.author.avatar_url)
                        await m.edit(embed=embed, components=[])
                    if c == '보':
                        embed = discord.Embed(title=f"ㄲㅂ. 내가 이겨야 하는데... 그래 내가 한판 봐줬다. 니가 이겼어",color=discord.Colour.red(), timestamp=ctx.message.created_at)
                        embed.add_field(name=f"{ctx.author}", value=f"가위✌", inline=True)
                        embed.add_field(name=f"{self.bot.user.name}", value=f"보🤚", inline=True)
                        embed.set_footer(text=f"{ctx.author}", icon_url=ctx.author.avatar_url)
                        await m.edit(embed=embed, components=[])
                    if c == '바위':
                        embed = discord.Embed(title=f"거봐 내가 이긴다고 했지? 에휴. 허접이네",color=discord.Colour.blue(), timestamp=ctx.message.created_at)
                        embed.add_field(name=f"{ctx.author}", value=f"가위✌", inline=True)
                        embed.add_field(name=f"{self.bot.user.name}", value=f"바위✊", inline=True)
                        embed.set_footer(text=f"{ctx.author}", icon_url=ctx.author.avatar_url)
                        await m.edit(embed=embed, components=[])
                elif res.component.id == "qkdnl":
                    a = ['가위','보','바위']
                    c = random.choice(a)
                    if c == '가위':
                        embed = discord.Embed(title=f"ㄲㅂ. 내가 이겨야 하는데... 그래 내가 한판 봐줬다. 니가 이겼어",color=discord.Colour.red(), timestamp=ctx.message.created_at)
                        embed.add_field(name=f"{ctx.author}", value=f"바위✊", inline=True)
                        embed.add_field(name=f"{self.bot.user.name}", value=f"가위✌", inline=True)
                        embed.set_footer(text=f"{ctx.author}", icon_url=ctx.author.avatar_url)
                        await m.edit(embed=embed, components=[])
                    if c == '보':
                        embed = discord.Embed(title=f"거봐 내가 이긴다고 했지? 에휴. 허접이네",color=discord.Colour.blue(), timestamp=ctx.message.created_at)
                        embed.add_field(name=f"{ctx.author}", value=f"바위✊", inline=True)
                        embed.add_field(name=f"{self.bot.user.name}", value=f"보🤚", inline=True)
                        embed.set_footer(text=f"{ctx.author}", icon_url=ctx.author.avatar_url)
                        await m.edit(embed=embed, components=[])
                    if c == '바위':
                        embed = discord.Embed(title=f"쳇. 비겼네......;;",color=discord.Colour.green(), timestamp=ctx.message.created_at)
                        embed.add_field(name=f"{ctx.author}", value=f"바위✊", inline=True)
                        embed.add_field(name=f"{self.bot.user.name}", value=f"바위✊", inline=True)
                        embed.set_footer(text=f"{ctx.author}", icon_url=ctx.author.avatar_url)
                        await m.edit(embed=embed, components=[])
                elif res.component.id == "qh":
                    a = ['가위','보','바위']
                    c = random.choice(a)
                    if c == '가위':
                        embed = discord.Embed(title=f"거봐 내가 이긴다고 했지? 에휴. 허접이네",color=discord.Colour.blue(), timestamp=ctx.message.created_at)
                        embed.add_field(name=f"{ctx.author}", value=f"보🤚", inline=True)
                        embed.add_field(name=f"{self.bot.user.name}", value=f"가위✌", inline=True)
                        embed.set_footer(text=f"{ctx.author}", icon_url=ctx.author.avatar_url)
                        await m.edit(embed=embed, components=[])
                    if c == '보':
                        embed = discord.Embed(title=f"쳇. 비겼네......;;",color=discord.Colour.green(), timestamp=ctx.message.created_at)
                        embed.add_field(name=f"{ctx.author}", value=f"보🤚", inline=True)
                        embed.add_field(name=f"{self.bot.user.name}", value=f"보🤚", inline=True)
                        embed.set_footer(text=f"{ctx.author}", icon_url=ctx.author.avatar_url)
                        await m.edit(embed=embed, components=[])
                    if c == '바위':
                        embed = discord.Embed(title=f"ㄲㅂ. 내가 이겨야 하는데... 그래 내가 한판 봐줬다. 니가 이겼어",color=discord.Colour.red(), timestamp=ctx.message.created_at)
                        embed.add_field(name=f"{ctx.author}", value=f"보🤚", inline=True)
                        embed.add_field(name=f"{self.bot.user.name}", value=f"바위✊", inline=True)
                        embed.set_footer(text=f"{ctx.author}", icon_url=ctx.author.avatar_url)
                        await m.edit(embed=embed, components=[])
        except:
            print(traceback.format_exc())
                    
    @commands.command(
        name = "주사위"
    )
    async def dice(self, ctx):
        await ctx.send(f"{random.randint(2, 12)}가 나왔습니다!")
    @commands.command(
        name = "뽑기"
    )
    async def dice(self, ctx, number:int):
        embed=discord.Embed(title="뽑기")
        embed.add_field(name=f"1~{number}중에", value=f"{random.randint(1, number)}가 나왔습니다")
        await ctx.send(embed=embed)





def setup(bot):
    bot.add_cog(game(bot))