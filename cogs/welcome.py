import aiosqlite
import discordSuperUtils
from discord.ext import commands
import emoji

class Welcome(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.ImageManager = discordSuperUtils.ImageManager()

    @commands.Cog.listener("on_member_join")
    async def member_welcome(self, member):
        database = await aiosqlite.connect("db/db.sqlite")
        cur = await database.execute("SELECT * FROM welcome WHERE guild = ?", (member.guild.id,))
        data = await cur.fetchone()
        if data is not None:
            img = await self.ImageManager.create_welcome_card(
                member,
                "https://media.discordapp.net/attachments/885113533300367390/915548254127669269/1d2958f6ae79a237.jpg",
                # discordSuperUtils.Backgrounds.DISCORD,#discordSuperUtils.ImageManager.load_asset("bgimg.png")
                f"어서오세요!, {member}님!",
                "서버 규칙을 확인해주시고 많은 이용부탁드립니다!",
                title_color=(127, 255, 0),
                description_color=(127, 255, 0),
                font_path="user.ttf"
            )
            channel = self.bot.get_channel(data[1])
            await channel.send(f"{member.mention}님이 오셨습니다! 반가워해주세요.",file=img)
    @commands.Cog.listener("on_member_remove")
    async def member_remove(self, member):
        database = await aiosqlite.connect("db/db.sqlite")
        cur = await database.execute("SELECT * FROM removes WHERE guild = ?", (member.guild.id,))
        data = await cur.fetchone()
        premium_cur = await database.execute("SELECT * FROM premium WHERE guild = ?", (member.guild.id,))
        premium_resp = await premium_cur.fetchone()
        if premium_resp == None:
            print("프리미엄 해제")    
        if data is not None:
                img = await self.ImageManager.create_welcome_card(
                    member,
                    "https://media.discordapp.net/attachments/921555509935480853/922013277112922152/i16280711964.png?width=400&height=225",
                    # discordSuperUtils.Backgrounds.DISCORD,#discordSuperUtils.ImageManager.load_asset("bgimg.png")
                    f"안녕히가세요, {member}님.",
                    "나가습니다..ㅠ",
                    title_color=(127, 255, 0),
                    description_color=(127, 255, 0),
                    font_path="user.ttf"
                )
                channel = self.bot.get_channel(data[1])
                await channel.send(f"{member.name}({member})님이 나가셨습니다.",file=img)

def setup(bot):
    bot.add_cog(Welcome(bot))
