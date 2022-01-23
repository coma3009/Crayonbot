from datetime import datetime, timezone

import aiosqlite
import discord
import discordSuperUtils
import pytz
from discord.ext import commands
import asyncio
from PycordPaginator import Paginator
def ordinal(num: int) -> str:
    """
    Returns the ordinal representation of a number
    Examples:
        11: 11th
        13: 13th
        14: 14th
        3: 3rd
        5: 5th
    :param num:
    :return:
    """

    return (
        f"{num}th"
        if 11 <= (num % 100) <= 13
        else f"{num}{['th', 'st', 'nd', 'rd', 'th'][min(num % 10, 4)]}"
    )


class birthday(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.ImageManager = discordSuperUtils.ImageManager()
        self.BirthdayManager = discordSuperUtils.BirthdayManager(self.bot)
        
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
    @commands.group(name="메모")
    async def memo(self, ctx):
        await ctx.send("메모를 등록해보세요!")
    @memo.command(name="삭제")
    async def delete_memo(self, ctx, reason):
        database = await aiosqlite.connect("db/db.sqlite")
        cur = await database.execute(
                'SELECT * FROM memo WHERE user = ?', (ctx.author.id,)
            )
        datas = await cur.fetchone()
        if datas != None:
            embed = discord.Embed(
                title = f"메모",
                description = f"{reason}제목은 메모에 작성되여있지 않아요",
                colour = discord.Colour.random(),
                timestamp = ctx.message.created_at
            )
            await ctx.send(embed=embed)
        await database.execute("DELETE FROM memo WHERE user = ?", (ctx.author.name))
        await database.commit()
        await ctx.reply("삭제완료")


    @memo.command(name="등록")
    async def setup_memo(self, ctx, reason):
        database = await aiosqlite.connect("db/db.sqlite")
        cur = await database.execute(
                'SELECT * FROM memo WHERE user = ?', (ctx.author.id,)
            )
        datas = await cur.fetchone()
        if datas != None:
            embed = discord.Embed(
                title = f"메모",
                description = f"{reason}제목은 메모에 작성되여있어요 \n내용: {datas[2]}",
                colour = discord.Colour.random(),
                timestamp = ctx.message.created_at
            )
            await ctx.send(embed=embed)
        msg=await ctx.reply(
                f"내용을 입력해주세요")
        try:
                message = await self.bot.wait_for("message",
                                                  check=lambda i: i.author.id == ctx.author.id and i.channel.id == ctx.channel.id,
                                                  timeout=60)
                message = message.content
        except asyncio.TimeoutError:
                await msg.edit("시간이 초과되었어요!", components=[])
                return
        await msg.edit("저장중이에요!", components=[])
        try:
                await database.execute(f"INSERT INTO memo(user,reason,reason) VALUES (?, ?, ?)",
                                       (ctx.author.id, reason, message))
                await database.commit()
        except Exception as e:
                await msg.edit("에러가 발생했어요! \n에러내역을 개발자에게 발송하였으니 곧 고쳐질거에요!")
                print(e)
                return
        await msg.edit(f"저장을 완료했어요!\n메모제목 - {reason}")
    @memo.command(name="등록")
    async def setup_memo(self, ctx):
        database = await aiosqlite.connect("db/db.sqlite")
        cur = await database.execute(
                'SELECT * FROM memo WHERE user = ?', (ctx.author.id,)
            )
        datas = await cur.fetchall()
        memo_list = []
        for i in datas:
            memo_list.append(f"```제목|{i[1]} \n내용|{i[2]}```")       
        e = Paginator(
                client=self.bot.components_manager,
                embeds=discordSuperUtils.generate_embeds(
                    memo_list,
                    title=f"{ctx.author.name}님의 메모!",
                    fields=10,
                    description="```메모를 삭제하실거면 \n짱구야 메모 삭제 [제목]을 해주시면 됩니다!```",
                ),
                channel=ctx.channel,
                only=ctx.author,
                ctx=ctx,
                use_select=False)
        await e.start()
       
def setup(bot):
    bot.add_cog(birthday(bot))
