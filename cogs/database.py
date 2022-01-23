import discord
from discord import colour
from discord.ext import commands
import time
import random
import sqlite3
import discordSuperUtils
import requests
import traceback
import asyncio
import datetime
import time
import aiosqlite
from PycordPaginator import Paginator
from discord_components import Button, ButtonStyle, SelectOption, Select, component
con = sqlite3.connect(f'database.db')
cur = con.cursor()

admin = [0]
black = [0]
vip = [0]
users = [0]

class Database(commands.Cog, name = "봇 경제 명령어", description = "봇 경제 명령어"):
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
                    title=f'📫짱구 메일함 | {check}개 수신됨',
                    description="아직 읽지 않은 메일이 있어요.'`>메일`'로 확인하세요.\n주기적으로 메일함을 확인해주세요! 소소한 업데이트 및 이벤트개최등 여러소식을 확인해보세요.",
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
                    title=f'📫짱구 메일함 | {int(check) - int(check2[1])}개 수신됨',
                    description="아직 읽지 않은 메일이 있어요.'`>메일`'로 확인하세요.\n주기적으로 메일함을 확인해주세요! 소소한 업데이트 및 이벤트개최등 여러소식을 확인해보세요.",
                    colour=ctx.author.colour,
                )

                await ctx.send(embed=mal)
    @commands.command(name = f'가입')
    async def data_join(self, ctx):
        try:

            # await ctx.send(f'{ctx.author.mention}, [약관](https://blog.teamsb.cf/pages/tos)을 동의하시려면 이 채널에 `동의` 를 입력해 주세요.\n동의하지 않으신다면 그냥 무시하세요.')
            embed = discord.Embed(
                title = '가입',
                description = '이용 약관을 동의하시려면 이 채널에 `동의` 를 입력해 주세요.\n이용 약관을 동의하지 않으신다면 이 메시지를 무시하세요.',
                colour = discord.Colour.green()
            )
            await ctx.send(f'{ctx.author.mention}', embed = embed)

            def check(m):
                return m.content == '동의' and m.author.id == ctx.author.id

            try:
                msg = await self.bot.wait_for('message', timeout=60.0, check=check)
            except asyncio.TimeoutError:
                await ctx.send(f"<a:no:754265096813019167> {ctx.author.mention}, 시간이 초과되어 자동 종료되었습니다.")
            else:
                if msg.content == "동의":
                    try:
                        cur.execute(f'INSERT INTO USERS VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', (str(ctx.author.id), str(ctx.author.name), 0, 0, 0, 0, 0, 0, random.randint(1, 4), 0, "None", 0))
                        con.commit()
                    except sqlite3.IntegrityError:
                        await ctx.send(f'{ctx.author.mention}님은 이미 가입된 유저입니다.')
                        con.commit()
                        return None
                    except sqlite3.OperationalError:
                        await ctx.send(f'{ctx.author.mention}님 가입 진행중 데이터베이스에 문제가 생겼습니다. \n계속해서 같은 오류가 뜬다면 Bainble0211#6109에게 문의해 주세요!\n에러 : ```python\n{traceback.format_exc()}\n```')
                        con.commit()
                        return None
                    await ctx.send(f'{ctx.author.mention}님의 가입을 성공하였습니다!')
                        # else:
                        #     await ctx.send(f'{ctx.author.mention} 다른 것을 입력하셨거나, 무시하셔서 취소되었습니다.')
                        #     return None
        except:
            await ctx.send(traceback.format_exc())
    @commands.command(name = f'탈퇴')
    async def data_remoce(self, ctx):
        try:
            embed = discord.Embed(
                title = '탈퇴',
                description = '짱구 경제시스템을 탈퇴 하시겠습니까?',
                colour = discord.Colour.green()
            )
            embed1 = discord.Embed(
                title = '탈퇴',
                description = '취소하였습니다.',
                colour = discord.Colour.green()
            )
            embed2 = discord.Embed(
                title = '탈퇴',
                description = '시간 초과로 취소되었습니다.',
                colour = discord.Colour.green()
            )
            embed3 = discord.Embed(
                title = '탈퇴',
                description = '탈퇴완료',
                colour = discord.Colour.green()
            )
            msg = await ctx.send(embed=embed,
            components = [
                [
                    Button(label="네", emoji="✅", style=ButtonStyle.green, id="yes"),
                    Button(label="아니요", emoji="❎", style=ButtonStyle.red, id="no"),
                ]
            ]
        )
            def check(res):
                return ctx.author == res.user and res.channel == ctx.channel

            try:
                res = await self.bot.wait_for("button_click", check=check, timeout=60)
                if res.component.id == "no":
                    return await msg.edit(embed=embed1, components = [])
            except asyncio.TimeoutError:
                return await msg.edit(embed=embed2, components = [])
            cur.execute("DELETE FROM USERS WHERE id = '{}'".format(str(ctx.author.id)))
            con.commit()
            await msg.edit(embed=embed3, components = [])
        except:
            await ctx.send(traceback.format_exc())
    @commands.command(name = f'돈확인', aliases = ['인벤','인벤토리', '가방','ㄷ','돈'])
    async def member_inventory(self, ctx, user: discord.User = None):
        if user is None:
            i = 0
            res=cur.execute(f'SELECT * FROM USERS WHERE id=\'{ctx.author.id}\'')
            if res ==  None:
                return await ctx.reply("가입되지 않은 유저입니다.")
            for row in cur:
                i += 1
                user2 = row
            if i == 0:
                await ctx.send(f'{ctx.author.mention}님은 짱구 데이터베이스에 등록되어 있지 않습니다.')
                return None
            embed=discord.Embed(title=f"{ctx.author.name}님의 인벤토리", colour=discord.Colour.random())
            embed.add_field(name="소유한 돈", value=f"{user2[2]}")
            embed.add_field(name="통장", value=f"{user2[11]}")
            await ctx.send(embed=embed)
        else:
            i = 0
            res=cur.execute(f'SELECT * FROM USERS WHERE id=\'{user.id}\'')
            if res ==  None:
                return await ctx.reply("가입되지 않은 유저입니다.")
            for row in cur:
                i += 1
                user2 = row
            if i == 0:
                await ctx.send(f'{user.mention}님은 짱구 데이터베이스에 등록되어 있지 않습니다.')
                return None
            embed=discord.Embed(title=f"{user.name}님의 인벤토리", colour=discord.Colour.random())
            embed.add_field(name="소유한 금액", value=f"{user2[2]}")
            embed.add_field(name="통장", value=f"{user2[11]}")
            await ctx.send(embed=embed)
    @commands.command(
        name= "송금",
    )
    async def songgm(self, ctx, member: discord.Member, money: int):
        if money > 0 or member.bot is True:
            try:
                database = await aiosqlite.connect("database.db")
                now = datetime.datetime.now()
                cur1=await database.execute(f"SELECT * FROM USERS WHERE id=\'{ctx.author.id}\'")
                cur2=await database.execute(f"SELECT * FROM USERS WHERE id=\'{member.id}\'")
                datas = await cur1.fetchall()
                datas1 = await cur2.fetchall()
                em=discord.Embed(title="알림", description=f"날짜 : {now.year}년 {now.month}월 {now.day}일 \n시간 : {now.hour:02}시 {now.minute:02}분")
                em.add_field(name="송금된 금액", value=f"{money}원")
                em.add_field(name="받는 유저", value=f"{member.name}({member.mention})")
                embed=discord.Embed(title="송금완료", description = f"송금된 돈: {money}", colour=discord.Colour.random())
                for user in datas:
                    # await database.execute(f"UPDATE USERS SET money={user[2] + money} WHERE id=\'{member.id}\'")
                    # await asyncio.sleep(2)
                    await database.execute(f"UPDATE USERS SET money={user[2] - money} WHERE id=\'{ctx.author.id}\'")
                    await database.commit()
                    embed.add_field(name=f"보낸 사람: {ctx.author.name}", value=f" 현재 돈: {user[2] - money}")
                for user in datas1:
                    await database.execute(f"UPDATE USERS SET money={user[2] + money} WHERE id=\'{member.id}\'")
                    await database.commit()
                    embed.add_field(name=f"받은 사람: {member.name}" , value=f" 현재돈: {user[2] + money}")
                await ctx.author.send(embed=em)
                await ctx.reply(embed=embed)
            except:
                print(traceback.format_exc())
        else:
            await ctx.reply("돈을 음수로 주거나 봇에게 줄 수 없어요.")
    @commands.command(
        name= "입금",
    )
    async def bankmoneyadd(self, ctx, money: int):
        try:    
                
                cur.execute(f"SELECT * FROM USERS WHERE id=\'{ctx.author.id}\'")
                randmoney = money
                i = 0
                for row in cur:
                    i += 1
                user2 = row
                if int(money) > user2[2]:
                    await ctx.send('가진돈 보다 더 많은 돈으로는 입금할수 없어요!')
                    return None
                if int(money) == 0:
                    await ctx.send(f'0 보다 적은돈으로는 입금을 할수 없어요!')
                    return None
                now = datetime.datetime.now()
                em=discord.Embed(title="알림", description=f"날짜 : {now.year}년 {now.month}월 {now.day}일 \n시간 : {now.hour:02}시 {now.minute:02}분")
                em.add_field(name="입금된 금액", value=f"{money}원")
                em.add_field(name="통장금액", value=f"{user2[11] + randmoney}")
                # await database.execute(f"UPDATE USERS SET money={user[2] + money} WHERE id=\'{member.id}\'")
                # await asyncio.sleep(2)
                embed=discord.Embed(title="입금완료", description = f"입금된 돈: {money}", colour=discord.Colour.random())
                cur.execute(f"UPDATE USERS SET money={user2[2] - randmoney} WHERE id=\'{ctx.author.id}\'")
                cur.execute(f"UPDATE USERS SET bankmoney={user2[11] + randmoney} WHERE id=\'{ctx.author.id}\'")
                con.commit()
                await asyncio.sleep(4)
                embed.add_field(name=f"소유 금액: {ctx.author.name}", value=f" 소유 금액: {user2[2] - randmoney}")
                embed.add_field(name=f"통장: {ctx.author.name}" , value=f" 현재 통장 금액: {user2[11] + randmoney}")
                await ctx.author.send(embed=em)
                await ctx.reply(embed=embed)
        except:
            print(traceback.format_exc())
    @commands.command(
        name= "출금",
    )
    async def bankmoneydel(self, ctx, money: int):
        try:
                cur.execute(f"SELECT * FROM USERS WHERE id=\'{ctx.author.id}\'")
                i = 0
                for row in cur:
                    i += 1
                user2 = row
                if int(money) > user2[11]:
                    await ctx.send('가진돈 보다 더 많은 돈으로는 출금할수 없어요!')
                    return None
                if int(money) == 0:
                    await ctx.send(f'0 보다 적은돈으로는 출금을 할수 없어요!')
                    return None
                # await database.execute(f"UPDATE USERS SET money={user[2] + money} WHERE id=\'{member.id}\'")
                # await asyncio.sleep(2)
                now = datetime.datetime.now()
                embed=discord.Embed(title="출금완료", description = f"출금된 돈: {money}", colour=discord.Colour.random())
                randmoney = money
                cur.execute(f"UPDATE USERS SET money={user2[2] + randmoney} WHERE id=\'{ctx.author.id}\'")
                cur.execute(f"UPDATE USERS SET bankmoney={user2[11] - randmoney} WHERE id=\'{ctx.author.id}\'")
                con.commit()
                await asyncio.sleep(4)
                em=discord.Embed(title="알림", description=f"날짜 : {now.year}년 {now.month}월 {now.day}일 \n시간 : {now.hour:02}시 {now.minute:02}분")
                em.add_field(name="출금된 금액", value=f"{money}원")
                em.add_field(name="통장금액", value=f"{user2[11] - randmoney}")
                embed.add_field(name=f"소유 금액: {ctx.author.name}", value=f" 소유 금액: {user2[2] + randmoney}")
                embed.add_field(name=f"통장: {ctx.author.name}" , value=f" 현재 통장 금액: {user2[11] - randmoney}")
                await ctx.author.send(embed=em)
                await ctx.reply(embed=embed)
        except:
            print(traceback.format_exc())
    @commands.command(name = f'지원금', aliases = ['ㅈㅇㄱ'])
    async def data_givemoney(self, ctx):
        i = 0
        cur.execute(f'SELECT * FROM USERS WHERE id=\'{ctx.author.id}\'')
        for row in cur:
            user = row
            i += 1
        if i == 0:
            await ctx.send(f'{ctx.author.mention}님은 코인봇 서비스에 가입되어 있지 않습니다.')
            return None
        if not int(user[9] + 3600 - time.time()) <= 0:
            await ctx.send(f'{int(user[9] + 3600 - time.time())}초 동안 쿨타임이 적용되어있습니다')
            return None
        randmoney = random.randint(1, 1000)
        cur.execute(f'UPDATE USERS SET money={user[2] + randmoney}, cooltime={time.time()} WHERE id=\'{user[0]}\'')
        con.commit()
        await ctx.send(f'{ctx.author.mention}님에게 {randmoney}원이 적립되었습니다!')
    @commands.command(name="돈주기")
    @commands.is_owner()
    async def moneygive(self, ctx, user_id:int, money:int, *, reason = None):
        try:
            user1 = await self.bot.fetch_user(user_id)
            userid=user_id
            cur1=cur.execute(f'SELECT * FROM USERS WHERE id=\'{userid}\'')
            datas = cur1.fetchall()
            for user in datas:
                cur.execute(f"UPDATE USERS SET money={user[2] + money} WHERE id=\'{userid}\'")
                con.commit()
                await ctx.send(f"{user1}님에게 {money}원을 보냈습니다")
                embed=discord.Embed(title="알림",description="봇관리자로 부터 돈이 왔습니다. \n궁금한 사항이나 오류발견시 봇 디엠으로 문의넣어주세요.",colour=discord.Colour.random())
                embed.add_field(name="관리자가 보낸 돈", value=f"{money}원")
                embed.add_field(name="편지", value=f"{reason}")
                await user1.send(embed=embed)
        except:
            print(traceback.format_exc())
            await ctx.send((traceback.format_exc()))
    @commands.command(name = '도박', aliases = ["ㄷㅂ"])
    async def data_gambling(self, ctx, money):
        try:
            date = cur.execute("SELECT * FROM USERS WHERE ID = ?", (str(ctx.author.id),)).fetchone()
            if not date:
                await ctx.send(f'{ctx.author.mention}님! 도박을 하기 전에 코인봇 서비스에 가입해 주세요!\n가입 명령어 : `>가입`')
                return None


            if int(money) > date[2]:
                await ctx.send('가진돈 보다 더 많은 돈으로는 도박할수 없어요!')
                return None
            if int(money) == 0:
                await ctx.send(f'0 보다 적은돈으로는 도박을 할수 없어요!')
                return None

            
            cur.execute(f'SELECT * FROM USERS WHERE id=\'{ctx.author.id}\'')
            for row in cur:
                user2 = row
            original_money = user2[2]
            
            embed = discord.Embed(
                    title = f'정말로 {money}원을 가지고 도박 하시겠습니까?',
                    colour = discord.Colour.green()
                )
            tg = await ctx.send(f'{ctx.author.mention}', embed=embed)
            await tg.add_reaction("⭕")
            await tg.add_reaction("❌")

            def check(reaction, user):
                return (user == ctx.author and str(reaction) in ["⭕", "❌"] and tg.id == reaction.message.id)
            reaction, user = await self.bot.wait_for("reaction_add", check=check)
                
            if str(reaction) == '⭕':
                random_value = random.randint(1, 3)
                on = 0
                getmoney = 0
                if random_value == 1 or random_value == 3:
                    on = 1
                    getmoney = int(money + money)
                else:
                    on = 2
                    getmoney = int(money) * -1
                    lostmoney = int(money)

                #await ctx.send(f"{data}") # 유일하게 여기만 user에 노란줄이 없음 왜이럴까
                print(original_money)
                print(getmoney, date[0])
                print(type(original_money))
                # print(type(getmoney, date[0])) # 얘는 안나오잖아 아 뭔지 알았어
                print((int(original_money) + int(getmoney)))
                print(type(int(original_money) + int(getmoney)))
                # 왜 아무것도 출력이 안되지
                # ? 잠만 왜 저게 getmoney, date 두개가 한개 안에 들어가있어
                try:
                    cur.execute("UPDATE USERS SET money = ? WHERE id = ?",(int(original_money) + int(getmoney),ctx.author.id))  # ㅌㅌ ?
                except:
                    print(traceback.format_exc())
                #cur.execute("UPDATE USERS SET username = ? WHERE id = ?",(getmoney,date[0])) # 하셈
                    #cur.execute(f'UPDATE USERS SET MONEY = {user[2] + getmoney} WHERE id =\'{user[0]}\'') # 위에서는 user에서 노란줄이 뜨는데 여기만 안떠
                    # 실행해봐
                con.commit()

                if on == 1:
                    await ctx.send(f'{ctx.author.mention} 도박을 성공했어요! {getmoney} 원을 적립했어요!')
                    return None
                if on == 2:
                    await ctx.send(f'{ctx.author.mention} 도박을 실패했어요.... {lostmoney}원을 짱구이 가져갑니다.')
                    return None
            else:
                await ctx.send(f'{ctx.author.mention}, 도박을 취소했어요!')
                return None
        except:
            await ctx.send(traceback.format_exc())
    @commands.command(name = '유저목록', aliases = ["도박목록"])
    @commands.is_owner()
    async def ecoinfo(self, ctx):
        mi = cur.execute("SELECT * FROM USERS")
        datas = mi.fetchall()
        now = datetime.datetime.now()
        black_list = []
        for i in datas:
            black_list.append(f"```유저아이디|{i[0]} \n이름|{i[1]} \n돈|{i[2]} \n통장|{i[11]}```")
        e = Paginator(
                client=self.bot.components_manager,
                embeds=discordSuperUtils.generate_embeds(
                    black_list,
                    title=f"도박을 사용하는 유저들이 등록되어있어요.",
                    fields=10,
                    description=f"```현재 시간 \n {now.year}년 {now.month}월 {now.day}일 {now.hour:02}시 {now.minute:02}분 ```",
                ),
                channel=ctx.channel,
                only=ctx.author,
                ctx=ctx,
                use_select=False)
        await e.start()
def setup(bot):
    bot.add_cog(Database(bot))
