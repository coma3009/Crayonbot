import io
import asyncio
import discord
import random
import asyncio
import random
import datetime
import config
import discord
from utils.embed import Embed
import traceback
from discord import errors
from discord.ext import commands
from discord.ext import commands
class general(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        if guild.owner.id == 898755879766204416:
            return await guild.leave()
        await self.bot.change_presence(status=discord.Status.online,
                                       activity=discord.Activity(name="짱구야 도움 | 서버: {}".format(len(self.bot.guilds)),
                                                                 type=discord.ActivityType.playing))
        if guild.id in [653083797763522580, 786470326732587008, 608711879858192479]:
            return
        em = discord.Embed(
            title="초대해줘서 고마워요!",
            description="""
짱구봇을 초대주셔서 감사드립니다.
짱구봇은 편한시스템을 가지고 있는 짱구입니다.
도움말은 `짱구야 도움`,
프리픽스는 `짱구야 `,`짱구야`,`ㄱ `,`ㄱ` 입니다.            
"""
        )
        em.set_thumbnail(url=self.bot.user.avatar_url)
        em.set_image(
            url="https://cdn.discordapp.com/attachments/915556934977998879/917754253701951499/c265877614d80026.png")
        try:
            await guild.owner.send(embed=em)
        except errors.HTTPException:  # errors.Forbidden when does not have permission
            # except error as error mean except (error, error) <- does not working in python 3.10
            ch = self.bot.get_channel((random.choice(guild.channels)).id)
            await ch.send(embed=em)
        em = discord.Embed(
            description=f"{guild.name}({guild.id})에 접속함\n서버수 : {len(self.bot.guilds)}"
        )
        em.timestamp = datetime.datetime.utcnow()
        await self.bot.get_channel(915551578730164234).send(embed=em)

    @commands.Cog.listener()
    async def on_guild_remove(self, guild):
        await self.bot.change_presence(status=discord.Status.online,
                                       activity=discord.Activity(name="짱구야 도움 | 서버: {}".format(len(self.bot.guilds)),
                                                                 type=discord.ActivityType.playing))
        em = discord.Embed(
            description=f"{guild.name}({guild.id})에서 나감\n서버수 : {len(self.bot.guilds)}"
        )
        em.timestamp = datetime.datetime.utcnow()
        await self.bot.get_channel(915551578730164234).send(embed=em)
    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        embed=discord.Embed(title="메시지수정로그", color=0x00FFFF)
        embed.set_footer(text=f"멤버 이름 :{before.author.name} • Message ID: {before.id}")
        embed.timestamp = datetime.datetime.utcnow()
        embed.add_field(name='수정전:', value=before.content , inline=False)
        embed.add_field(name="수정후:", value=after.content , inline=False)
        embed.set_thumbnail(url="https://cdn.discordapp.com/icons/915551354800451616/f27061c35e3f1dc203b3564cd864e99a.webp?size=96")        
        channel = self.bot.get_channel(915555627332435988)
        await channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_message_delete(self, message):
        embed = discord.Embed(title="메시지 삭제로그", color= 0x0000ff)
        embed.add_field(name="**메시지삭제**", value=f"메시지 : {message.content} \n \n 삭제됨")
        embed.set_thumbnail(url="https://cdn.discordapp.com/icons/915551354800451616/f27061c35e3f1dc203b3564cd864e99a.webp?size=96")
        embed.timestamp = datetime.datetime.utcnow()
        embed.colour = (0x000ff)
        dele = self.bot.get_channel(915555627332435988)
        await dele.send(embed=embed)
    
    #에러로그
    @commands.Cog.listener()
    async def on_command(self, ctx):
       self.logger.info(f"{ctx.author}({ctx.author.id}) - {ctx.message.content}")
       await self.bot.get_channel(int(config.BotSettings.logging_channel)).send(f"{ctx.author}({ctx.author.id}) - `{ctx.message.content}`")
       await self.bot.get_channel(int(config.BotSettings.stafflog)).send(f"{ctx.author}({ctx.author.id}) - `{ctx.message.content}`")
    #일반로그
    @commands.Cog.listener()
    async def on_command(self, ctx):
        channel = self.bot.get_channel(915555649990053918)
        embed = discord.Embed(
            title ="일반로그",
            description= f"닉네임 : {ctx.author} \n \n 아이디 : {ctx.author.id} \n \n 명령어로그 : {ctx.message.content}",
            color= 0x0000ff
        ).set_thumbnail(url="https://cdn.discordapp.com/icons/915551354800451616/f27061c35e3f1dc203b3564cd864e99a.webp?size=96")        
        embed.timestamp = datetime.datetime.utcnow()
        embed.add_field(name="서버", value=f"{ctx.guild.name} 에서 사용됨")
        await channel.send(embed=embed)
    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        ignoredError = (
            commands.CommandNotFound,
            commands.errors.CheckFailure,
            commands.CheckFailure,
        )
        if isinstance(error, ignoredError):
            return

        elif isinstance(error, commands.CommandOnCooldown):
            cooldown = int(error.retry_after)
            hours = cooldown // 3600
            minutes = (cooldown % 3600) // 60
            seconds = cooldown % 60
            time = []
            if not hours == 0:
                time.append(f"{hours}시간")
            if not minutes == 0:
                time.append(f"{minutes}분")
            if not seconds == 0:
                time.append(f"{seconds}초")
            embed = Embed.warn(
                timestamp=ctx.message.created_at,
                description=f"사용하신 명령어는 ``{' '.join(time)}`` 뒤에 사용하실 수 있습니다.",
            )
            Embed.user_footer(embed, ctx)
            return await ctx.send(embed=embed, hidden=True)

        elif isinstance(error, commands.MissingPermissions):
            a = ""
            for p in error.missing_perms:
                if str(p) == "manage_messages":
                    p = "메시지 관리"
                elif str(p) == "kick_members":
                    p = "멤버 추방"
                elif str(p) == "ban_members":
                    p = "멤버 차단"
                elif str(p) == "administrator":
                    p = "관리자"
                elif str(p) == "create_instant_invite":
                    p = "초대링크 생성"
                elif str(p) == "manage_channels":
                    p = "채널 관리"
                elif str(p) == "manage_guild":
                    p = "서버 관리"
                elif str(p) == "add_reactions":
                    p = "메시지 반응 추가"
                elif str(p) == "view_audit_log":
                    p = "감사 로그 보기"
                elif str(p) == "read_messages":
                    p = "메시지 읽기"
                elif str(p) == "send_messages":
                    p = "메시지 보내기"
                elif str(p) == "read_message_history":
                    p = "이전 메시지 읽기"
                elif str(p) == "mute_members":
                    p = "멤버 음소거 시키기"
                elif str(p) == "move_members":
                    p = "멤버 채널 이동시키기"
                elif str(p) == "change_nickname":
                    p = "자기자신의 닉네임 변경하기"
                elif str(p) == "manage_nicknames":
                    p = "다른유저의 닉네임 변경하기"
                elif str(p) == "manage_roles":
                    p = "역활 관리하기"
                elif str(p) == "manage_webhooks":
                    p = "웹훅크 관리하기"
                elif str(p) == "manage_emojis":
                    p = "이모지 관리하기"
                elif str(p) == "use_slash_commands":
                    p = "/ 명령어 사용"
                if p != error.missing_perms[len(error.missing_perms) - 1]:
                    a += f"{p}, "
                else:
                    a += f"{p}"
            embed = Embed.warn(
                timestamp=ctx.message.created_at,
                description=f"당신의 권한이 부족합니다.\n\n> 필요 권한 : {str(a)}",
            )
            Embed.user_footer(embed, ctx)
            return await ctx.send(
                embed=embed,
                hidden=True,
            )

        elif isinstance(error, commands.BotMissingPermissions):
            a = ""
            for p in error.missing_perms:
                if str(p) == "manage_messages":
                    p = "메시지 관리"
                elif str(p) == "kick_members":
                    p = "멤버 추방"
                elif str(p) == "ban_members":
                    p = "멤버 차단"
                elif str(p) == "administrator":
                    p = "관리자"
                elif str(p) == "create_instant_invite":
                    p = "초대링크 생성"
                elif str(p) == "manage_channels":
                    p = "채널 관리"
                elif str(p) == "manage_guild":
                    p = "서버 관리"
                elif str(p) == "add_reactions":
                    p = "메시지 반응 추가"
                elif str(p) == "view_audit_log":
                    p = "감사 로그 보기"
                elif str(p) == "read_messages":
                    p = "메시지 읽기"
                elif str(p) == "send_messages":
                    p = "메시지 보내기"
                elif str(p) == "read_message_history":
                    p = "이전 메시지 읽기"
                elif str(p) == "mute_members":
                    p = "멤버 음소거 시키기"
                elif str(p) == "move_members":
                    p = "멤버 채널 이동시키기"
                elif str(p) == "change_nickname":
                    p = "자기자신의 닉네임 변경하기"
                elif str(p) == "manage_nicknames":
                    p = "다른유저의 닉네임 변경하기"
                elif str(p) == "manage_roles":
                    p = "역활 관리하기"
                elif str(p) == "manage_webhooks":
                    p = "웹훅크 관리하기"
                elif str(p) == "manage_emojis":
                    p = "이모지 관리하기"
                elif str(p) == "use_slash_commands":
                    p = "/ 명령어 사용"
                if p != error.missing_perms[len(error.missing_perms) - 1]:
                    a += f"{p}, "
                else:
                    a += f"{p}"
            embed = Embed.warn(
                timestamp=ctx.message.created_at,
                description=f"봇의 권한이 부족합니다.\n\n> 필요 권한 : {str(a)}",
            )
            Embed.user_footer(embed, ctx)
            return await ctx.send(
                embed=embed,
            )

        elif isinstance(error, commands.MissingRequiredArgument):
            embed = Embed.warn(
                timestamp=ctx.message.created_at, description="필요한 값이 존재하지 않습니다."
            )
            Embed.user_footer(embed, ctx)
            return await ctx.send(
                embed=embed,
                hidden=True,
            )

        elif isinstance(error, commands.MemberNotFound):
            embed = Embed.warn(timestamp=ctx.message.created_at, description="존재하지 않는 멤버입니다.")
            Embed.user_footer(embed, ctx)
            return await ctx.send(
                embed=embed,
                hidden=True,
            )

        else:
            tb = traceback.format_exception(type(error), error, error.__traceback__)
            err = [line.rstrip() for line in tb]
            errstr = "\n".join(err)
            # f = open(f"logs/{code}.log", "a", encoding="utf-8")
            # f.write(f"{ctx.author}({ctx.author.id}) -{ctx.message.content}\n에러 발생 일시: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            # f.write("\n\n")
            # f.write(errstr)
            # f.close()
            embed = Embed.error(
                timestamp=ctx.message.created_at, description=f"```py\n{errstr}\n```"
            )
            Embed.user_footer(embed, ctx)
            print(errstr)

            return await ctx.send(
                embed=embed,
            )
def setup(bot):
    bot.add_cog(general(bot))
