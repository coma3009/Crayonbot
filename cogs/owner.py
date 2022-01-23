import discord
from discord.embeds import Embed
from discord.ext import commands, tasks
import random
import time
import uuid
from datetime import datetime
from dateutil.relativedelta import relativedelta
import traceback
from discord.ext.menus import Button
from discord_components import component
from discord_components import Button, ButtonStyle, SelectOption, Select
import pytz
import aiosqlite
import discordSuperUtils
import datetime
from PycordPaginator import Paginator

class Owner(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(
        name = "서버리스트",
        aliases = ['serverlist']
    )
    @commands.is_owner()
    async def owner_serverlist(self, ctx):
        with open("guilds.txt", 'w', -1, "utf-8") as a: # 'guilds.txt' 파일을 생성하고 그것을 'a' 로 지정한다
            a.write(str(self.bot.guilds)) # 'a' 에 봇이 접속한 서버들을 나열한다 
        file1 = discord.File("guilds.txt") # 'file1' 을 'guilds.txt' 로 정의한다
        await ctx.author.send(file=file1) # 명령어를 수행한 멤버의 DM으로 'file1' 을 발송한다
        os.remove("guilds.txt")
        await ctx.reply(f"DM으로 서버 리스트 발송을 완료했습니다!")

    @commands.command(
        name="Check-Error",
        aliases=["elog"],
        usage="elog [code]",
        help=" 짱구의 에러 로그를 확인할수 있습니다.",
        hidden=True,
    )
    @commands.is_owner()
    async def owner_elog(self, ctx, code):
        try:
            f = open(f"data/error_logs/{code}", "r", encoding="utf8")
            data = f.read()
            await ctx.send(f"```py\n{data}\n```")
            f.close()
        except:
            await ctx.send(
                content=code, file=discord.File(fp=data, filename=f"{code}.txt")
            )
    @commands.command(name="메일작성")
    @commands.is_owner()
    async def mail(self, ctx, *, va_lue):
        database = await aiosqlite.connect("db/db.sqlite")
        cur = await database.execute('SELECT * FROM mail')
        mails = await cur.fetchall()
        print(mails)
        check = 1
        # noinspection PyBroadException
        try:
            for _ in mails:
                check += 1
        except Exception as e:
            print(e)
        await database.execute(
            'INSERT INTO mail(id,value) VALUES (?,?)', (check, va_lue)
        )

        await database.commit()
        await ctx.send('성공적으로 메일을 발송하였습니다.')
    @commands.command(name="공지")
    @commands.is_owner()
    async def broadcasting(self, ctx, *, value):
        em = discord.Embed(
            title="짱구 봇 공지사항",
            description=value,
            colour=discord.Colour.random()
        )
        em.set_thumbnail(url=self.bot.user.avatar_url)
        em.set_image(
            url="https://media.discordapp.net/attachments/921555509935480853/921555519578189834/c265877614d80026.png?width=400&height=144")
        em.set_footer(text="특정 채널에 받고싶다면 '짱구야 설정'으로 설정하세요! 권한 확인 필수!")
        msg = await ctx.reply("발송중...")
        guilds = self.bot.guilds
        ok = []
        ok_guild = []
        success = 0
        failed = 0
        for guild in guilds:
            channels = guild.text_channels
            for channel in channels:
                if guild.id in [653083797763522580, 786470326732587008]:
                    break
                if (
                    channel.topic is not None
                    and str(channel.topic).find("-HOnNt") != -1
                ):
                    ok.append(channel.id)
                    ok_guild.append(guild.id)
                    break

        for guild in guilds:
            channels = guild.text_channels
            for _channel in channels:
                if guild.id in ok_guild:
                    break
                if guild.id in [653083797763522580, 786470326732587008]:
                    break
                random_channel = random.choices(channels)
                ok.append(random_channel[0].id)
                break
        for i in ok:
            channel = self.bot.get_channel(i)
            try:
                await channel.send(embed=em)
                success += 1
            except discord.Forbidden:
                failed += 1
        await msg.edit("발송완료!\n성공: `{ok}`\n실패: `{no}`".format(ok=success, no=failed))
    @commands.group(name="블랙",invoke_without_command=True)
    async def blacklist(self,ctx:commands.Context):
        database = await aiosqlite.connect("db/db.sqlite")
        cur = await database.execute("SELECT * FROM black WHERE user = ?", (ctx.author.id,))
        if await cur.fetchone() == None:
            return await ctx.reply(f"{ctx.author}님은 블랙리스트에 등록되어있지 않아요.")
        data = await cur.fetchone()
        await ctx.reply(f"블랙사유: {data[1]}")
    @blacklist.command(name= '추가', aliases=['black','블랙','blackadd'])
    @commands.is_owner()
    async def mod_black(self, ctx, user_id:int,*,reason):
        user = await self.bot.fetch_user(user_id)
        db = await aiosqlite.connect("db/db.sqlite")
        cur = await db.execute("SELECT * FROM black WHERE user = ?", (user_id,))
        datas = await cur.fetchone()
        if datas != None:
            embed = discord.Embed(
                title = f"블랙",
                description = f"{user}님은 블랙리스트에 등록되어있어요. \n사유: {datas[1]}",
                colour = discord.Colour.random(),
                timestamp = ctx.message.created_at
            )
            await ctx.send(embed=embed)
        await db.execute("INSERT INTO black(user,reason,username) VALUES (?,?,?)", (user_id, reason, user.name))
        await db.commit()
        embed2=discord.Embed(
            title="블랙",
            description = f"__봇관리자로 부터 블랙 등록되었음을 알려드립니다__ \n\n 관리자가 아래의 사유로 블랙을 등록하셨어요.\n\n 사유 : {reason}",
            colour=discord.Colour.random() )
       
        try:
            await user.send(embed=embed2)
        except:
            pass
        await ctx.reply("등록완료!")
    @blacklist.command(name= '삭제', aliases=['blackdel','제거'])
    @commands.is_owner()
    async def mod_black_del(self, ctx, user_id:int):
        user = await self.bot.fetch_user(user_id)
        db = await aiosqlite.connect("db/db.sqlite")
        cur = await db.execute("SELECT * FROM black WHERE user = ?", (user_id,))
        datas = await cur.fetchone()
        embed=discord.Embed(title="블랙", description=f"{user}님은 블랙리스트에 등록되어있지않아요.",colour=discord.Colour.random())
        if datas ==  None:
            return await ctx.send(embed=embed)
        await db.execute("DELETE FROM black WHERE user = ?", (user_id,))
        await db.commit()
        embed2=discord.Embed(title="블랙", description="__봇 관리자로부터 블랙해제됨.__\n\n 봇관리자가 블랙해제하셨어요.",colour=discord.Colour.random())
        try:
            await user.send(embed=embed2)
        except:
            print
        await ctx.reply("해제완료")
    @blacklist.command(name= '목록')
    @commands.is_owner()
    async def mod_black_jo(self, ctx):
        database = await aiosqlite.connect("db/db.sqlite")
        cur = await database.execute("SELECT * FROM black")
        datas = await cur.fetchall()
        black_list = []
        for i in datas:
            black_list.append(f"```유저아이디|{i[0]} \n사유|{i[1]} \n이름|{i[2]}```")       
        e = Paginator(
                client=self.bot.components_manager,
                embeds=discordSuperUtils.generate_embeds(
                    black_list,
                    title=f"블랙목록에 유저들이 등록되어있어요.",
                    fields=10,
                    description="```블랙해제를 하실거면 \n짱구야 블랙 제거 [유저아이디]를 해주시면 됩니다!```",
                ),
                channel=ctx.channel,
                only=ctx.author,
                ctx=ctx,
                use_select=False)
        await e.start()
            #await ctx.send(templates[1])
    @blacklist.command(name= '초기화', aliases=["reset"])
    @commands.is_owner()
    async def black_rest(self, ctx):
        db = await aiosqlite.connect("db/db.sqlite")
        await db.execute("DELETE FROM black")
        await db.commit()
        
        cur = await db.execute("SELECT * FROM black")
        datas = await cur.fetchall()
        if datas != None:
            await ctx.reply("초기화 완료")

    @commands.command(name="디엠")
    @commands.is_owner()
    async def dm(self, ctx, user_id:int, *, reason):
        try:
            user1 = await self.bot.fetch_user(user_id)
            embed=discord.Embed(title="알림", description="봇관리자로 부터 메시지가 왔습니다. \n궁금한 사항이나 오류발견시 봇 디엠으로 문의넣어주세요.", colour=discord.Colour.random())
            embed.add_field(name="메시지내용", value=f"{reason}")
            await user1.send(embed=embed)
            await ctx.send("전송완료!")
        except:
            print(traceback.format_exc())
            await ctx.send((traceback.format_exc()))
    @commands.command(name="서버탈퇴" ,aliases=['나와', '나가' '탈퇴'])
    @commands.is_owner()
    async def get_out(self, ctx, guild_id: int):
        if isinstance(ctx.channel, discord.abc.PrivateChannel) == True:
                msg2 = await ctx.send('서버 찾는중 ( ' + '0' + ' )')
                count = 0
                for guild in self.bot.guilds:
                    if guild.id == guild_id:
                        await guild.leave()
                        await ctx.send('`' + str(guild.name) + '` 에서 나왔어요!')
                        print(str(guild.name))
                    else:
                        pass
                    
                    count = count+1
                    show_count = str(count)
                    await msg2.edit(content = '서버 찾는중 ( ' + show_count + ' )')
        # for i in self.bot.guilds:
        #     for j in i.text_channels:
        #         if ("코인" in j.topic):
        #             try:
        #                 await j.send(embed=embed)
        #                 count += 1
        #                 channel.append(f"{i.name} - {j.name}")
        #             except:
        #                 for k in i.text_channels:
        #                     if ("봇" in k.name):
        #                         try:
        #                             await k.send(embed=embed)
        #                             count += 1
        #                             channel.append(f"{i.name} - {j.name}")
        #                         except:
        #                             for l in i.text_channels:
        #                                 if ("공지" in l.name):
        #                                     try:
        #                                         await i.send(embed = embed)
        #                                         count += 1
        #                                         channel.append(f"{i.name} - {l.name}")
        #                                     except:
        #                                         channel.append(f"{i.name} 전송 실패")
        #                                     break                                            
        #             else:
        #                 break
        # await ctx.send(f"{count}개의 길드에 공지를 전송했습니다!")
    @commands.group(name="프리미엄", invoke_without_command=True)
    async def premium(self,ctx):
        db = await aiosqlite.connect("db/db.sqlite")
        conn = await db.execute("SELECT * FROM premium WHERE guild = ?",(ctx.guild.id,))
        resp = await conn.fetchone()
        em = discord.Embed(
            title=f"{ctx.guild.name}의 프리미엄 상태",
            colour=discord.Colour.random()
        )
        em.add_field(name="뮤직 셋업 기능",value="히드라처럼 특정채널에서 노래를 재생해보세요!",inline=False)
        em.add_field(name="욕설 감지 무제한",value="욕설 감지제한이 1,000회였다면 이젠 무제한으로 욕설을 감지해보세요!",inline=False)
        em.add_field(name="트위치 채널 등록가능 개수 1 -> 5개", value="트위치 방송알림을 받기위해 등록하는 채널 개수 제한이 1개에서 5개로 늘어납니다!\n다양한 스트리머를 등록해 방송알림을 받아보세요!", inline=False)
        em.add_field(name="유튜브 채널 등록가능 개수 1 -> 5개", value="유튜브 방송알림을 받기위해 등록하는 채널 개수 제한이 1개에서 5개로 늘어납니다!\n다양한 스트리머를 등록해 방송알림을 받아보세요!", inline=False)
        if resp == None:
            em.add_field(name="프리미엄 상태",value="<a:cross:893675768880726017>프리미엄을 이용중인 서버가 아니거나 만료된 상태에요..😥\n자세한 사항&구매는 제 DM으로 `짱구봇에게 DM으로 문의넣어주세요`")
            em.add_field(name="가격", value="문화상품권:5,000원 \n계좌이체:4,000원")
        else:
            #endtime = str(time.mktime(datetime.strptime(resp[2], '%Y-%m-%d %H:%M:%S').timetuple()))[:-2]
            em.add_field(name="프리미엄 상태", value=f"<:badge:904937799701110814>만료일: <t:{resp[3]}>(<t:{resp[3]}:R>)")
        await ctx.reply(embed=em)

    @premium.command(name="등록")
    @commands.is_owner()
    async def add_premium(self,ctx,guild_id:int,year: int, month: int, day: int):
        code = uuid.uuid4()
        db = await aiosqlite.connect("db/db.sqlite")
        conn = await db.execute("SELECT * FROM premium WHERE guild = ?", (guild_id,))
        resp = await conn.fetchone()
        if resp == None:
            ending = datetime.datetime.now() + relativedelta(years=int(year), months=int(month), days=int(day))
            ending = ending.strftime('%Y/%m/%d %H:%M:%S')
            endtime = str(time.mktime(datetime.datetime.strptime(ending, '%Y/%m/%d %H:%M:%S').timetuple()))[:-2]
            await db.execute("INSERT INTO premium(guild, code, end_time, end_timestamp) VALUES (?, ?, ?, ?)",
                             (guild_id, str(code), str(ending), endtime))
            await db.commit()
            return await ctx.reply("✅")
        return await ctx.reply("이미 사용중이에요.")

    @premium.command(name="삭제")
    @commands.is_owner()
    async def del_premium(self, ctx, code: str, guild_id:int):
        db = await aiosqlite.connect("db/db.sqlite")
        conn = await db.execute("SELECT * FROM premium WHERE code = ?", (code,))
        resp = await conn.fetchone()
        if resp == None:
            return await ctx.reply("사용중인 길드가 아니에요.")
        await db.execute("DELETE FROM premium WHERE code = ?",(code,))
        await db.execute("DELETE FROM removes WHERE guild = ?", (guild_id,))
        await db.commit()
        return await ctx.reply("✅")

    @premium.command(name="조회")
    @commands.is_owner()
    async def getinfo_premium(self, ctx, code: str = None):
        db = await aiosqlite.connect("db/db.sqlite")
        if code == None:
            conn = await db.execute("SELECT * FROM premium")
            resp = await conn.fetchall()
            formatted_leaderboard = [
                f"길드(ID): {self.bot.get_guild(x[0])}({x[0]})\n코드: {x[1]}\n만료일: <t:{x[3]}>(<t:{x[3]}:R>)" for x in resp
            ]

            e = Paginator(
                client=self.bot.components_manager,
                embeds=discordSuperUtils.generate_embeds(
                    formatted_leaderboard,
                    title="프리미엄 리스트",
                    fields=15,
                    description=f"오너전용 프리미엄 정보 리스트",
                ),
                channel=ctx.channel,
                only=ctx.author,
                ctx=ctx,
                use_select=False)
            await e.start()
        else:
            conn = await db.execute("SELECT * FROM premium WHERE code = ?",(code,))
            resp = await conn.fetchone()
            em = discord.Embed(
                title=f"{self.bot.get_guild(resp[0])}({resp[0]})의 프리미엄 상태",
                description=f"코드: {resp[1]}\n프리미엄 만료일: <t:{resp[3]}>(<t:{resp[3]}:R>)",
                colour=discord.Colour.random()
            )
            return await ctx.reply(embed=em)
def setup(bot):
    bot.add_cog(Owner(bot))