import asyncio
import json
import os
import time
import traceback

import aiohttp
import aiosqlite
import discord
import discordSuperUtils
import requests
from PycordPaginator import Paginator
from discordSuperUtils import TwitchManager
from discord.ext import commands
from typing import List
from discord_components import Select, SelectOption, Button
from dotenv import load_dotenv
load_dotenv(verbose=True)


def mTwitchOauth2():
    key = ''
    try:
        key = requests.post("https://id.twitch.tv/oauth2/token?client_id=" + os.getenv('TWITCH_CLIENT_ID') +
                            "&client_secret=" + os.getenv('TWITCH_CLIENT_SECRET') + "&grant_type=client_credentials")
    except requests.exceptions.Timeout as te:
        print(te)
    except requests.exceptions.ConnectionError as ce:
        print(ce)
    except requests.exceptions.HTTPError as he:
        print(he)
    # Any Error except upper exception
    except requests.exceptions.RequestException as re:
        print(re)
    access_token = json.loads(key.text)["access_token"]
    print(access_token)
    return access_token
class twitch(commands.Cog):
    def __init__(self, bot):
        super().__init__()
        self.bot = bot
        self.live = {}
        self.access_token = mTwitchOauth2()
        self.TwitchManager = discordSuperUtils.TwitchManager(bot, os.getenv('TWITCH_CLIENT_ID'), self.access_token)
        self.bot.loop.create_task(self.twitch_loop())

    @staticmethod
    def add_stream_fields(embed: discord.Embed, stream: dict):
        embed.add_field(
            name="Title",
            value=f"[{stream['title']}](https://twitch.tv/{stream['user_name']})",
            inline=False,
        )
        embed.add_field(name="Game", value=stream["game_name"], inline=False)
        embed.add_field(name="Viewers", value=str(stream["viewer_count"]), inline=False)
        embed.add_field(
            name="Started At", value=stream["started_at"], inline=False
        )  # You can format it.
        embed.add_field(
            name="Mature",
            value="Yes" if stream["is_mature"] else "No",
            inline=False,
        )
        embed.add_field(name="Language", value=stream["language"].upper(), inline=False)
        embed.set_image(url=stream["thumbnail_url"].format(height=248, width=440))

    @staticmethod
    def loop_stream_fields(embed: discord.Embed, stream: dict):
        embed.add_field(
            name="Title",
            value=f"[{stream['title']}](https://twitch.tv/{stream['broadcaster_login']})",
            inline=False,
        )
        embed.add_field(name="Game", value=stream["game_name"], inline=False)
        embed.add_field(
            name="Started At", value=stream["started_at"], inline=False
        )  # You can format it.
        embed.add_field(name="Language", value=stream["broadcaster_language"].upper(), inline=False)
        embed.set_image(url=stream["thumbnail_url"].format(height=248, width=440))

    @commands.group(name="?????????", invoke_without_command=True)
    async def twitch_(self,ctx):
        db = await aiosqlite.connect("db/db.sqlite")
        twitch_cur = await db.execute("SELECT * FROM twitch WHERE guild = ?",(ctx.guild.id,))
        premium_cur = await db.execute("SELECT * FROM premium WHERE guild = ?",(ctx.guild.id,))
        twitch_resp = await twitch_cur.fetchall()
        premium_resp = await premium_cur.fetchone()
        if twitch_resp == []:
            return await ctx.reply("????????? ????????? ????????? ?????????! `????????? ????????? ?????? [????????? ??????] [????????? ??? ??????] [??????ID]`??? ???????????????!")
        if premium_resp == None:
            em = discord.Embed(title="????????? ?????? ?????? | ????????????(?????? ?????? 1??? ??????)",colour=discord.Colour.random())
            for i in twitch_resp:
                status = await self.TwitchManager.get_channel_status([i[3]])
                stream_info = next(iter(status), None)
                if not stream_info:
                    em.add_field(name=f"??????: {stream_info['user_name']}({i[3]})",value="???????????? ??????: <:Offline:911928110381953074>????????????")
                else:
                    em.add_field(
                        name=f"??????: {stream_info['user_name']}({i[3]})",value=f"???????????? ??????: <:streaming:911928055197478912>??????????????? [{stream_info['title']}](https://twitch.tv/{stream_info['user_name']})")
            return await ctx.reply(embed=em)
        formatted_leaderboard = []
        for i in twitch_resp:
            status = await self.TwitchManager.get_channel_status([i[3]])
            stream_info = next(iter(status), None)
            try:
                formatted_leaderboard.append(
                    f"??????: {stream_info['user_name']}({i[3]})\n???????????? ??????: <:streaming:911928055197478912>??????????????? [{stream_info['title']}](https://twitch.tv/{stream_info['user_name']})")
            except:
                formatted_leaderboard.append(f"??????: {i[3]}\n???????????? ??????: <:Offline:911928110381953074>????????????")

        e = Paginator(
            client=self.bot.components_manager,
            embeds=discordSuperUtils.generate_embeds(
                formatted_leaderboard,
                title="????????? ?????? ?????? | <:badge:904937799701110814>??????????????????(?????? ?????? 5??? ??????)",
                fields=3,
                description=f"{ctx.guild}??? ????????? ?????? ?????? ??????",
            ),
            channel=ctx.channel,
            only=ctx.author,
            ctx=ctx,
            use_select=False)
        await e.start()

    @twitch_.command(name="??????")
    async def twitch_lookup(self,ctx,*, channel: str):
        status = await self.TwitchManager.get_channel_status([channel])
        stream_info = next(iter(status), None)
        if not stream_info:
            await ctx.send(f"<:Offline:911928110381953074> '{channel}'??? ????????????????????? ?????????????????? ???????????????.")
            return

        embed = discord.Embed(title=f"<:streaming:911928055197478912> '{stream_info['user_name'] or channel}' ??? ????????????????????????!", color=0x00FF00)

        self.add_stream_fields(embed, stream_info)

        await ctx.reply(embed=embed)

    @twitch_.command(name="??????")
    async def twitch_add(self,ctx,role:discord.Role,notice_channel:discord.TextChannel,*, channel: str):
        db = await aiosqlite.connect("db/db.sqlite")
        twitch_cur = await db.execute("SELECT * FROM twitch WHERE guild = ?", (ctx.guild.id,))
        premium_cur = await db.execute("SELECT * FROM premium WHERE guild = ?", (ctx.guild.id,))
        twitch_resp = await twitch_cur.fetchall()
        premium_resp = await premium_cur.fetchone()
        if premium_resp == None:
            if twitch_resp == []:
                await db.execute("INSERT INTO twitch(guild, notice_channel, notice_role, channel) VALUES (?, ?, ?, ?)",
                                 (ctx.guild.id, notice_channel.id, role.id, channel))
                await db.commit()
                await self.TwitchManager.add_channel(ctx.guild, channel)
                return await ctx.reply(f"??????????????? '{channel}'??? ???????????????.")
            else:
                return await ctx.reply("??????????????? ????????????????????? ?????? ????????????????????????. ?????? ????????? ???????????? ??????????????? ??????????????????.")
        else:
            if twitch_resp == [] or len(list(twitch_resp)) <= 5:
                await db.execute("INSERT INTO twitch(guild, notice_channel, notice_role, channel) VALUES (?, ?, ?, ?)",
                                 (ctx.guild.id, notice_channel.id, role.id, channel))
                await db.commit()
                #await self.TwitchManager.add_channel(ctx.guild, channel)
                return await ctx.reply(f"??????????????? '{channel}'??? ???????????????.")
            else:
                return await ctx.reply("???! ????????? ?????? ????????? 5????????? ???????????? ????????????..????")

    @twitch_.command(name="??????")
    async def twitch_del(self,ctx):
        db = await aiosqlite.connect("db/db.sqlite")
        twitch_cur = await db.execute("SELECT * FROM twitch WHERE guild = ?", (ctx.guild.id,))
        twitch_resp = await twitch_cur.fetchall()
        if twitch_resp == []:
            return await ctx.reply("????????? ????????? ????????? ?????????! `????????? ????????? ?????? [??????ID]`??? ???????????????!")
        msg = await ctx.send(f"{ctx.author.mention}, ????????? ????????? ?????? ?????????????????? ????????? ???????????????.",
                             components=[
                                 Select(placeholder="?????? ?????? ?????? ??????",
                                        options=[
                                            SelectOption(label=i[3],
                                                         value=i[3]) for i in twitch_resp
                                        ], )

                             ],
                             )
        try:
            interaction = await self.bot.wait_for(
                "select_option", check=lambda inter: inter.user.id == ctx.author.id
            )
            value = interaction.values[0]
        except asyncio.TimeoutError:
            await msg.edit("????????? ??????????????????!", components=[])
            return
        ##await self.TwitchManager.remove_channel(ctx.guild, value)
        await db.execute("DELETE FROM twitch WHERE guild = ? AND channel = ?",(ctx.guild.id,value))
        await db.commit()
        await msg.edit("??????????????? ??????????????? ????????????!",components=[])

    @staticmethod
    async def channel_statues(url,headers):
        async with aiohttp.ClientSession(headers=headers) as cs2:
            async with cs2.get(url) as res2:
                pr2 = await res2.read()
                sid2 = pr2.decode('utf-8')
                return json.loads(sid2)

    async def twitch_loop(self):
        await self.bot.wait_until_ready()
        db = await aiosqlite.connect("db/db.sqlite")
        while not self.bot.is_closed():
            await asyncio.sleep(5)
            twitch_cur = await db.execute("SELECT * FROM twitch")
            datas = await twitch_cur.fetchall()
            headers = {'Client-Id': os.getenv("TWITCH_CLIENT_ID"),
                       'Authorization': "Bearer " + self.access_token}
            for i in datas:
                url = "https://api.twitch.tv/helix/users?login=" + i[3]
                async with aiohttp.ClientSession(headers=headers) as cs2:
                    async with cs2.get(url) as res2:
                        pr2 = await res2.read()
                        sid2 = pr2.decode('utf-8')
                        answer2 = json.loads(sid2)
                        try:
                            url2 = "https://api.twitch.tv/helix/search/channels?query=" + i[3]
                            jsons = await self.channel_statues(url2,headers)
                            for j in jsons['data']:
                                if j['display_name'] == answer2['data'][0]['display_name']:
                                    if j['is_live']:
                                        try:
                                            if self.live[j['broadcaster_login']]:
                                                pass
                                            else:
                                                self.live[j['broadcaster_login']] = True
                                                status = await self.TwitchManager.get_channel_status([j['broadcaster_login']])
                                                stream_info = next(iter(status), None)
                                                embed = discord.Embed(
                                                    title=f"<:streaming:911928055197478912> '{j['display_name']}'?????? ??????????????? ??????????????????!",
                                                    color=0x00FF00)

                                                #self.loop_stream_fields(embed, j)
                                                self.add_stream_fields(embed,stream_info)
                                                channel = self.bot.get_channel(i[1])
                                                await channel.send(content=f"<@&{i[2]}>",embed=embed,components=[Button(style=5,
                                                                                                                        url=f"https://twitch.tv/{j['broadcaster_login']}",
                                                                                                                        label=f"{j['display_name']}?????? ?????? ????????????",
                                                                                                                        emoji=self.bot.get_emoji(911928055197478912))])
                                        except:
                                            self.live[j['broadcaster_login']] = False
                                    else:
                                        try:
                                            if self.live[j['broadcaster_login']]:
                                                embed = discord.Embed(
                                                    title=f"<:Offline:911928110381953074> '{j['display_name']}'?????? ??????????????? ???????????????!",
                                                    color=0x00FF00)
                                                embed.add_field(
                                                    name="?????? ????????????",
                                                    value=f"[{j['display_name']}](https://twitch.tv/{j['broadcaster_login']})",
                                                    inline=False,
                                                )
                                                embed.set_image(
                                                    url=j["thumbnail_url"].format(height=248, width=440))
                                                channel = self.bot.get_channel(i[1])
                                                await channel.send(embed=embed,components=[Button(style=5,
                                                                                                    url=f"https://twitch.tv/{j['broadcaster_login']}",
                                                                                                    label=f"{j['display_name']}?????? ?????? ????????????")])
                                                self.live[j['broadcaster_login']] = False
                                        except:
                                            self.live[j['broadcaster_login']] = False
                        except:
                            user = await self.bot.fetch_user(281566165699002379)
                            await user.send(str(traceback.format_exc()))

def setup(bot):
    bot.add_cog(twitch(bot))