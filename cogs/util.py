import io
import asyncio
from PycordPaginator import Paginator
import discord
from discord import colour
import platform
from discord.ext import commands
import datetime
from discord_components import (
    Select,
    SelectOption, Interaction
)
import aiosqlite

class util(commands.Cog):
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
        name = "서버정보"
    )
    async def server_info(self, ctx):
        guild = self.bot.get_guild(ctx.guild.id)
        if ctx.guild.premium_subscription_count == 1:
            embed = discord.Embed(colour=0xff00, title=f"<:boosting0:732546134018621460> {ctx.guild.name}", timestamp=ctx.message.created_at)
        elif ctx.guild.premium_tier == 1:
            embed = discord.Embed(colour=0xff00, title=f"<:boosting1:732546134542909500> {ctx.guild.name}", timestamp=ctx.message.created_at)
        elif ctx.guild.premium_tier == 2:
            embed = discord.Embed(colour=0xff00, title=f"<:boosting2:732546134379331584> {ctx.guild.name}", timestamp=ctx.message.created_at)
        elif ctx.guild.premium_tier == 3:
            embed = discord.Embed(colour=0xff00, title=f"<:boosting3:732546133850587208> {ctx.guild.name}", timestamp=ctx.message.created_at)
        else:
            embed = discord.Embed(colour=0xff00, title=f"{ctx.guild.name}", timestamp=ctx.message.created_at)
        embed.add_field(name="서버 이름", value=ctx.guild.name, inline=False)
        embed.add_field(name="서버 ID", value=ctx.guild.id, inline=False)
        embed.add_field(name="서버 주인", value=f"{ctx.guild.owner}({ctx.guild.owner.mention})", inline=False)
        embed.add_field(name="서버 국가", value=ctx.guild.region, inline=False)
        embed.add_field(name="서버 제작일", value = ctx.guild.created_at.strftime("20%y년 %m월 %d일"), inline=False)
        embed.add_field(name="서버 멤버 수", value = f'전체 유저 : {len(ctx.guild.members)}명\n └ 유저 : {len([x for x in guild.members if not x.bot])}명 | 봇 : {len([x for x in ctx.guild.members if x.bot])}개', inline=False)
        embed.add_field(name="서버 채널 수", value = f'전체 채널 : {len(ctx.guild.channels)}개\n └ 채팅채널 : {len(ctx.guild.text_channels)}개 | 음성채널 : {len(ctx.guild.voice_channels)}개 | 카테고리 : {len(ctx.guild.categories)}개', inline=False)
        embed.add_field(name="서버 이모지 수", value = f'{len(ctx.guild.emojis)}개', inline=False)

        if ctx.guild.afk_channel != None:
            embed.add_field(name=f'서버 잠수 채널', value=f'⭕ | 잠수 채널이 존재합니다.({ctx.guild.afk_channel.name} (타이머: {ctx.guild.afk_timeout}))', inline=False)
        else:
            embed.add_field(name=f'서버 잠수 채널', value=f'❌ | 잠수 채널이 존재하지 않습니다.', inline=False)
        if ctx.guild.system_channel != None:
            embed.add_field(name=f'서버 시스템 채널', value=f'⭕ | 시스템 채널이 존재합니다.({ctx.guild.system_channel.name} (<#{ctx.guild.system_channel.id}>))', inline=False)
        else:
            embed.add_field(name=f'서버 시스템 채널', value=f'❌ | 시스템 채널이 존재하지 않습니다.', inline=False)
        embed.add_field(name=f'서버 부스트 레벨', value=f'Level {ctx.guild.premium_tier}', inline=False)
        embed.add_field(name=f'서버 부스트 개수', value=f'Boost {ctx.guild.premium_subscription_count}', inline=False)
        if ctx.guild.is_icon_animated() is True:
            a = ctx.guild.icon_url_as(format="gif", size=2048)
            embed.set_thumbnail(url=a)
        elif ctx.guild.is_icon_animated() is False:
            a = ctx.guild.icon_url_as(format="png", size=2048)
            embed.set_thumbnail(url=a)
        try:
            embed.set_image(url=ctx.guild.banner_url_as(format='png'))
        except:
            pass
        embed.set_footer(text=f"{ctx.author}", icon_url=ctx.author.avatar_url)
        await ctx.send(embed=embed)



    @commands.command(name="프사")
    async def avatar(self, ctx, member: discord.Member = None):
        member_obj = member or ctx.author
        em = discord.Embed(
            title=f"{member}님의 프로필 사진",
            description=f"[링크]({member_obj.avatar_url})",
            colour=discord.Colour.random()
        )
        em.set_image(url=member_obj.avatar_url)
        await ctx.reply(embed=em)

    # @commands.command(name="유저정보")
    # async def userinfo(self, ctx, member: discord.Member = None):
    #     date = datetime.datetime.utcfromtimestamp(((int(ctx.author.id) >> 22) + 1420070400000) / 1000)
    #     embed = discord.Embed(color=0xffff00, title=f'{member.name} 님의 정보') 
    #     embed.add_field(name="`이름`", value=member.name, inline=False) 
    #     embed.add_field(name="`별명`", value=member.display_name) 
    #     embed.add_field(name="`디스코드 가입일`", value=str(date.year) + "년 " + str(date.month) + "월 " + str(date.day) + "일", inline=False) 
    #     embed.add_field(name="`서버 가입일`", value=f"{(member.joined_at).year}년 {(member.joined_at).month}월 {(member.joined_at).day}일", inline=False) 
    #     embed.add_field(name="`아이디`", value=member.id) 
    #     embed.add_field(name="`최상위 역할`", value=member.top_role.mention, inline=False) 
    #     embed.set_thumbnail(url=member.avatar_url) 
    #     await ctx.send(embed=embed) 

    # @commands.command(
    # name = "내정보"
    # )
    # async def my_info(self, ctx):
    #     date = datetime.datetime.utcfromtimestamp(((int(ctx.author.id) >> 22) + 1420070400000) / 1000)
    #     embed = discord.Embed(color=0xffff00, title=f'{ctx.author.name} 님의 정보') 
    #     embed.add_field(name="`이름`", value=ctx.author.name, inline=False) 
    #     embed.add_field(name="`별명`", value=ctx.author.display_name) 
    #     embed.add_field(name="`디스코드 가입일`", value=str(date.year) + "년 " + str(date.month) + "월 " + str(date.day) + "일", inline=False) 
    #     embed.add_field(name="`서버 가입일`", value=f"{(ctx.author.joined_at).year}년 {(ctx.author.joined_at).month}월 {(ctx.author.joined_at).day}일", inline=False) 
    #     embed.add_field(name="`아이디`", value=ctx.author.id) 
    #     embed.add_field(name="`최상위 역할`", value=ctx.author.top_role.mention, inline=False) 
    #     embed.set_thumbnail(url=ctx.author.avatar_url) 
    #     await ctx.send(embed=embed) 
    @commands.command(name="봇정보")
    async def botinfo(self, ctx):
        """
        Get some useful (or not) information about the bot.
        """

        # This is, for now, only temporary

        embed = discord.Embed(
            description="짱구봇 정보",
            color=0x42F56C
        )
        embed.set_thumbnail(url=self.bot.user.avatar_url)
        embed.set_image(
            url="https://media.discordapp.net/attachments/921555509935480853/921555519578189834/c265877614d80026.png?width=400&height=144")
        embed.add_field(
            name="주인:",
            value="Coma#3009(866297659362246706)",
            inline=True
        )
        embed.add_field(
            name="파이코드 버전:",
            value=f"{discord.__version__}",
            inline=True
        )
        embed.add_field(
            name="파이썬 버전:",
            value=f"{platform.python_version()}",
            inline=False
        )
        embed.add_field(
            name="OS Platform:",
            value=f"{platform.platform()}",
            inline=False
        )
        embed.add_field(name="접두사", value='짱구야 ', inline=True)
        embed.add_field(
            name="핑:",
            value=str(round(self.bot.latency * 1000)) + "ms",
            inline=True
        )
        embed.add_field(name="서버수", value=f"{(len(self.bot.guilds))}개의 서버에 있습니다!")
        await ctx.reply(embed=embed)
    @commands.group(name="뱃지", aliases=["배지"],invoke_without_command=True)
    async def badge(self,ctx):
        premium = "<:premium1:933686642919751710><:premium2:933686672028205076><:premium3:933686698838224936>\n<:badge:933686572379934790>\n짱구봇 프리미엄 사용시 부여되는 배지입니다."
        embde=discord.Embed(title="뱃지", colour=discord.Colour.random())
        embde.add_field(name="프리미엄 뱃지", value=f"{premium}")
        await ctx.reply(embed=embde)
    @badge.command(name="등록")
    @commands.is_owner()
    async def badge_add(self, ctx, user_id:int, badge_type):
        dicts = {
            "premium":"<:premium1:933686642919751710><:premium2:933686672028205076><:premium3:933686698838224936>",
        }
        user = await self.bot.fetch_user(user_id)
        db = await aiosqlite.connect("db/db.sqlite")
        cur = await db.execute("SELECT * FROM badge WHERE user = ? AND badge_type = ?", (user_id,badge_type))
        res = await cur.fetchone()
        if res is not None:
            return await ctx.reply("이미 소유하고 있어요.")
        user_em = discord.Embed(
            title="축하드립니다!🎉",
            description=f"관리자님이 {dicts[badge_type]}배지를 부여하셨어요!",
            colour=discord.Colour.random()
        )
        await db.execute("INSERT INTO badge(user,badge_type) VALUES (?,?)",(user_id,badge_type))
        await db.commit()
        await user.send(embed=user_em)
        await ctx.message.add_reaction("✅")

    @badge.command(name="제거")
    @commands.is_owner()
    async def badge_remove(self,ctx,user_id:int):
        dicts = {
            "premium_badge": self.bot.get_emoji(933686572379934790)
        }
        db = await aiosqlite.connect("db/db.sqlite")
        cur = await db.execute("SELECT * FROM badge WHERE user = ?", (user_id,))
        res = await cur.fetchall()
        msg = await ctx.send("제거할 배지를 선택하세요.",
                             components=[
                                 Select(placeholder="제거할 배지 선택",
                                        options=[
                                            SelectOption(label=i[1],
                                                         value=i[1], emoji=dicts[i[1]]) for i in res
                                        ], )

                             ],
                             )
        try:
            interaction = await self.bot.wait_for(
                "select_option", check=lambda inter: inter.user.id == ctx.author.id
            )
            value = interaction.values[0]
        except asyncio.TimeoutError:
            await msg.edit("시간이 초과되었어요!", components=[])
            return
        await db.execute("DELETE FROM badge WHERE user = ? AND badge_type = ?",(user_id, value))
        await db.commit()
        await msg.edit(content="✅", components = [])

    @commands.command(name="유저정보",aliases=['내정보'])
    async def myinfo(self, ctx, member:discord.Member = None):
        dicts = {
            "premium": "<:badge:933686572379934790>"
        }
        member = ctx.author if not member else member
        db = await aiosqlite.connect("db/db.sqlite")
        cur = await db.execute("SELECT * FROM badge WHERE user = ?",(member.id,))
        res = await cur.fetchall()
        if res != []:
            li = [dicts[i[1]] for i in res]
            vl = " ".join(li)
        else:
            vl = "<:botoff:933726671431950378>소유한 배지 없음"
        em = discord.Embed(
            title=f"{member}의 정보",
            colour=discord.Colour.random()
        )
        em.add_field(
            name="디스코드 가입일",
            value=f"{member.created_at.strftime('%Y-%m-%d  %H:%M:%S')}\n최초 가입일로부터 `{(ctx.message.created_at - member.created_at).days}`일 지남."
        )
        em.add_field(
            name="서버 가입일",
            value=member.joined_at.strftime('%Y-%m-%d  %H:%M:%S') + "\n최초 서버 가입일로 부터 `" + str((ctx.message.created_at - member.joined_at).days) + "`일 지남."
        )
        em.add_field(
            name="소유 역할",
            value=", ".join([role.mention for role in list(reversed(member.roles)) if not role.is_default()]),
            inline=False
        )
        em.add_field(
            name="소유 배지",
            value= vl
        )
        await ctx.reply(embed=em)
def setup(bot):
    bot.add_cog(util(bot))