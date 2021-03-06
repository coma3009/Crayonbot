import traceback
from typing import Optional

import aiosqlite
import discord
from discord.ext import commands
import time
import discordSuperUtils
from discordSuperUtils import MusicManager
from tools.database_tool import DataBaseTool
import datetime
from bot import MyBot
from py_cord_components import (
    Button,
    Interaction
)
def parse_duration(duration: Optional[float]) -> str:
    return (
        time.strftime("%H:%M:%S", time.gmtime(duration))
        if duration != "LIVE"
        else duration
    )
# Custom Check Error
class NoVoiceConncted(commands.CheckFailure):
    pass


class BotAlreadyConncted(commands.CheckFailure):
    pass


class InvalidIndex(commands.CheckFailure):
    pass

# Custom Check Error
class NoVoiceConncted(commands.CheckFailure):
    pass


class BotAlreadyConncted(commands.CheckFailure):
    pass


class InvalidIndex(commands.CheckFailure):
    pass


# Custom Checks
def ensure_voice_state():
    async def predicate(ctx):
        if not ctx.author.voice or not ctx.author.voice.channel:
            raise commands.NoVoiceConncted()

        if ctx.voice_client:
            if ctx.voice_client.channel != ctx.author.voice.channel:
                raise commands.BotAlreadyConncted()

        return True

    return commands.check(predicate)


# Format view count
def parse_count(count):
    original_count = count

    count = float("{:.3g}".format(count))
    magnitude = 0
    matches = ["", "K", "M", "B", "T", "Qua", "Qui"]

    while abs(count) >= 1000:
        if magnitude >= 5:
            break

        magnitude += 1
        count /= 1000.0

    try:
        return "{}{}".format(
            "{:f}".format(count).rstrip("0").rstrip("."), matches[magnitude]
        )
    except IndexError:
        return original_count


# Index converter/validator
def indexer(index: int):
    if index <= 0:
        raise InvalidIndex

    return index - 1


# Music commands
class Musicsetup(commands.Cog, discordSuperUtils.CogManager.Cog, name="Musicsetup"):
    """
    ???????????? ??????
    """
    def __init__(self, bot: MyBot):
        self.bot = bot
        self.music_stat = {}
        # self.client_secret = "" # spotify client_secret
        # self.client_id = "" # spotify client_id

        # Get your's from here https://developer.spotify.com/

        self.MusicManager = MusicManager(self.bot, spotify_support=False)

        # self.MusicManager = MusicManager(bot,
        #                                  client_id=self.client_id,
        #                                  client_secret=self.client_secret,
        #                                  spotify_support=True)

        # If using spotify support use this instead ^^^

        self.ImageManager = discordSuperUtils.ImageManager()
        super().__init__()

    async def queue(self, ctx):
        try:
            if queue := await self.MusicManager.get_queue(ctx):
                if len(queue.queue) == 1:
                    return ["????????? ????????????"]
                return [
                    f"{x.title} Requester: {x.requester.display_name if x.requester else 'Autoplay'}"for x in queue.queue
                ]

        except discordSuperUtils.QueueEmpty:
            return ["????????? ????????????"]
    async def restart(self, ctx, interaction:Interaction):  # This returns a player object
        # Extracting useful data from player object
        player = await self.MusicManager.now_playing(ctx)
        db = await aiosqlite.connect("db/db.sqlite")
        conn = await db.execute("SELECT * FROM music WHERE guild = ?", (ctx.guild.id,))
        resp = await conn.fetchone()
        thumbnail = player.data["videoDetails"]["thumbnail"]["thumbnails"][-1]["url"]
        uploader = player.data["videoDetails"]["author"]
        url = player.url
        requester = player.requester.mention if player.requester else "Autoplay"
        embed = discord.Embed(
            colour=discord.Colour.random(),
            timestamp=datetime.datetime.now(datetime.timezone.utc),
        )
        duration_played = round(
                await self.MusicManager.get_player_played_duration(ctx, player)
            )

        embed.set_author(name=f"{player.title} upload by {uploader}",url=player.url)
        embed.add_field(name="???????????????", value=requester)
        embed.add_field(name="?????? ????????????", value=parse_duration(duration_played))
        embed.add_field(name="????????????", value=parse_duration(player.duration))
        embed.add_field(name="?????????", value=uploader)
        embed.add_field(name="URL", value=f"[?????????]({url})")
        loop = (await self.MusicManager.get_queue(ctx)).loop
        if loop == discordSuperUtils.Loops.LOOP:
            loop_status = "???? ????????? ??????."
        elif loop == discordSuperUtils.Loops.QUEUE_LOOP:
            loop_status = "???? ????????? ??????."
        else:
            loop_status = "???? ????????????"
        embed.add_field(name="????????????", value=loop_status)
        shuffle = (await self.MusicManager.get_queue(ctx)).shuffle
        shuffle_status = "???? ?????????" if shuffle else "???? ????????????"
        embed.add_field(name="????????????", value=shuffle_status)
        embed.set_image(url=thumbnail)
        embed.set_thumbnail(url=r"https://i.imgur.com/ufxvZ0j.gif")
        queue_resp = await self.queue(ctx)
        queue_res = "\n".join(queue_resp)
        await (
            await ctx.channel.fetch_message(resp[2])
        ).edit(
            content=f'** **\n**__????????? ??????__**:\n{queue_res}',
            embed=embed,
        )

    # Play function
    async def play_cmd(self, ctx, query):
        db = await aiosqlite.connect("db/db.sqlite")
        conn = await db.execute("SELECT * FROM music WHERE guild = ?", (ctx.guild.id,))
        resp = await conn.fetchone()
        async with ctx.typing():
            player = await self.MusicManager.create_player(query, ctx.author)

        if player:
            if not ctx.voice_client or not ctx.voice_client.is_connected():
                await self.MusicManager.join(ctx)

            await self.MusicManager.queue_add(players=player, ctx=ctx)

            if not await self.MusicManager.play(ctx):
                queue_resp = await self.queue(ctx)
                try:
                    queue_res = "\n".join(queue_resp)
                except:
                    queue_res = "????????? ??????"
                msg = await ctx.channel.fetch_message(resp[2])
                await msg.edit(
                    content=f'** **\n**__????????? ??????__**:\n{queue_res}',
                    embed=msg.embeds[0],
                )
                await ctx.send(f"`{player[0].title}`(???)??? ???????????? ???????????????.",delete_after=5)
            else:
                await ctx.send("???",delete_after=5)
        else:
            await ctx.send("Query not found.",delete_after=5)

    def default_music_embed(self):
        em = discord.Embed(
            title="?????? ?????? ?????? ?????? ????????? ?????????.",
            colour=discord.Colour.dark_purple()
        )
        em.set_image(url="https://cdn.discordapp.com/attachments/921555509935480853/921555519578189834/c265877614d80026.png?width=400&height=144")
        em.set_footer(text="?????? ????????? ?????? ???????????? ??? ?????????!")
        em.add_field(name="????????????",value="-",inline=False)
        em.add_field(name="????????????",value="-",inline=False)
        return em
    async def set_default(self,ctx=None):
        db = await aiosqlite.connect("db/db.sqlite")
        conn = await db.execute("SELECT * FROM music WHERE guild = ?", (ctx.guild.id,))
        resp = await conn.fetchone()
        msg = await (self.bot.get_channel(resp[1])).fetch_message(resp[2])
        await msg.edit(
            content="** **\n**__????????? ??????__**:\n??????????????? ???????????? ??? ????????? ???????????? URL??? ??????????????????.",
            embed=self.default_music_embed(),
            components=[
                [
                    Button(emoji="???", custom_id="music_pr"),
                    Button(emoji="???", custom_id="music_stop"),
                    Button(emoji="???", custom_id="music_previous"),
                    Button(emoji="???", custom_id="music_skip"),
                    Button(emoji="????", custom_id="music_shuffle")
                ],
                [
                    Button(emoji="????", custom_id="music_volumedown"),
                    Button(label="10%", emoji="????", disabled=True),
                    Button(emoji="????", custom_id="music_volumeup"),
                    Button(emoji="????", custom_id="music_queueloop"),
                    Button(emoji="????", custom_id="music_oneloop")
                ],
                [
                    Button(label="????????????", emoji="??????", custom_id="music_restart"),
                    Button(emoji="????", custom_id="music_auto"),
                    Button(emoji="????", custom_id="music_join"),
                    Button(emoji="???", custom_id="music_cancel", style=4)
                ]
            ]
        )


    # DSU Error handler
    @discordSuperUtils.CogManager.event(discordSuperUtils.MusicManager)
    async def on_music_error(self, ctx, error):
        # sourcery skip: remove-redundant-fstring
        errors = {
            discordSuperUtils.NotPlaying: "?????? ?????? ????????? ??????????????? ?????????...",
            discordSuperUtils.NotConnected: f"?????? ?????????????????? ????????????????????????!",
            discordSuperUtils.NotPaused: "????????? ???????????????????????????!",
            discordSuperUtils.QueueEmpty: "???????????? ???????????????!",
            discordSuperUtils.AlreadyConnected: "?????? ?????????????????? ??????????????????!",
            discordSuperUtils.SkipError: "????????? ?????? ?????????!",
            discordSuperUtils.UserNotConnected: "??????????????? ??????????????? ????????????????????????!",
            discordSuperUtils.InvalidSkipIndex: "????????? ?????? ?????????????????????!",
        }

        for error_type, response in errors.items():
            if isinstance(error, error_type):
                await ctx.send(response,delete_after=5)
                break

        print("unexpected error")
        raise error


    # On music play event
    @discordSuperUtils.CogManager.event(discordSuperUtils.MusicManager)
    async def on_play(self, ctx, player):  # This returns a player object
        db = await aiosqlite.connect("db/db.sqlite")
        conn = await db.execute("SELECT * FROM music WHERE guild = ?", (ctx.guild.id,))
        resp = await conn.fetchone()
        # Extracting useful data from player object
        self.music_stat[ctx.guild.id] = "resume"
        thumbnail = player.data["videoDetails"]["thumbnail"]["thumbnails"][-1]["url"]
        uploader = player.data["videoDetails"]["author"]
        url = player.url
        requester = player.requester.mention if player.requester else "Autoplay"
        embed = discord.Embed(
            colour=discord.Colour.random(),
            timestamp=datetime.datetime.now(datetime.timezone.utc),
        )
        duration_played = round(
                await self.MusicManager.get_player_played_duration(ctx, player)
            )

        embed.set_author(name=f"{player.title} upload by {uploader}",url=player.url)
        embed.add_field(name="???????????????", value=requester)
        embed.add_field(name="?????? ????????????", value=parse_duration(duration_played))
        embed.add_field(name="????????????", value=parse_duration(player.duration))
        embed.add_field(name="?????????", value=uploader)
        embed.add_field(name="URL", value=f"[?????????]({url})")
        loop = (await self.MusicManager.get_queue(ctx)).loop
        if loop == discordSuperUtils.Loops.LOOP:
            loop_status = "???? ????????? ??????."
        elif loop == discordSuperUtils.Loops.QUEUE_LOOP:
            loop_status = "???? ????????? ??????."
        else:
            loop_status = "???? ????????????"
        embed.add_field(name="????????????", value=loop_status)
        shuffle = (await self.MusicManager.get_queue(ctx)).shuffle
        shuffle_status = "???? ?????????" if shuffle else "???? ????????????"
        embed.add_field(name="????????????", value=shuffle_status)
        embed.set_image(url=thumbnail)
        embed.set_thumbnail(url=r"https://i.imgur.com/ufxvZ0j.gif")
        queue_resp = await self.queue(ctx)
        queue_res = "\n".join(queue_resp)
        await (
            await ctx.channel.fetch_message(resp[2])
        ).edit(
            content=f'** **\n**__????????? ??????__**:\n{queue_res}',
            embed=embed,
        )

    # On queue end event
    @discordSuperUtils.CogManager.event(discordSuperUtils.MusicManager)
    async def on_queue_end(self, ctx):
        print(f"The queue has ended in {ctx}")
        await self.set_default(ctx)
        self.music_stat[ctx.guild.id] = None
        # You could wait and check activity, etc...

    # On inactivity disconnect event
    @discordSuperUtils.CogManager.event(discordSuperUtils.MusicManager)
    async def on_inactivity_disconnect(self, ctx):
        print(f"I have left {ctx} due to inactivity")


    async def pause_resume(self, ctx):
        if self.music_stat[ctx.guild.id] == "pause":
            if await self.MusicManager.resume(ctx):
                self.music_stat[ctx.guild.id] = "resume"
                return {"type":True,"stat":"resume"}
        elif await self.MusicManager.pause(ctx):
            self.music_stat[ctx.guild.id] = "pause"
            return {"type":True,"stat":"pause"}


    async def volume(self, ctx, interaction:Interaction,type):
        if current_volume := await self.MusicManager.volume(ctx):
            if type == "down":
                volume = int(current_volume) - 5
                if int(current_volume) == 5:
                    return await interaction.send(content="?????? ???????????? ????????? ??????????????????.",ephemeral=False,delete_after=5)
            else:
                if int(current_volume) == 100:
                    return await interaction.send(content="100?????? ??????????????????",ephemeral=False,delete_after=5)
                else:
                    volume = int(current_volume) + 5

            if await self.MusicManager.volume(ctx, volume):
                await interaction.edit_origin(
                    components=[
                                       [
                                            Button(emoji="???",custom_id="music_pr"),
                                            Button(emoji="???", custom_id="music_stop"),
                                            Button(emoji="???", custom_id="music_previous"),
                                            Button(emoji="???", custom_id="music_skip"),
                                            Button(emoji="????", custom_id="music_shuffle")
                                       ],
                                       [
                                           Button(emoji="????", custom_id="music_volumedown"),
                                           Button(label=f"{volume}%",emoji="????", custom_id="music_volumestat",disabled=True),
                                           Button(emoji="????", custom_id="music_volumeup"),
                                           Button(emoji="????", custom_id="music_queueloop"),
                                           Button(emoji="????", custom_id="music_oneloop")
                                       ],
                                       [
                                            Button(label="????????????", emoji="??????", custom_id="music_restart"),
                                            Button(emoji="????", custom_id="music_auto"),
                                            Button(emoji="????", custom_id="music_join"),
                                            Button(emoji="???", custom_id="music_cancel", style=4)
                                        ]
                                    ]
                )
            await interaction.send(content=f"?????? ???????????? ??????????????? - {current_volume}%",ephemeral=False,delete_after=5)
    async def loop(self, ctx,interaction:Interaction):
        is_loop = await self.MusicManager.loop(ctx)

        if is_loop is not None:
            await interaction.send(content=f"????????? ??????????????? {'???? ?????????' if is_loop else '???? ????????????'}?????????.\n???????????? ?????????????????? ????????? ?????? ?????????.",ephemeral=False,delete_after=5)

    async def queueloop(self, ctx,interaction:Interaction):
        is_loop = await self.MusicManager.queueloop(ctx)

        if is_loop is not None:
            await interaction.send(content=f"????????? ??????????????? {'???? ?????????' if is_loop else '???? ????????????'}?????????.\n???????????? ?????????????????? ????????? ?????? ?????????.",ephemeral=False,delete_after=5)

    async def skip(self, ctx,interaction:Interaction, index: int = None):
        if queue := (await self.MusicManager.get_queue(ctx)):

            requester = (await self.MusicManager.now_playing(ctx)).requester

            # Checking if the song is autoplayed
            if requester is None:
                await interaction.send(content="?????????????????? ????????? ???????????????.",ephemeral=False,delete_after=5)
                await self.MusicManager.skip(ctx, index)
            # Checking if queue is empty and autoplay is disabled
            if not queue.queue and not queue.autoplay:
                await interaction.send(content="???????????? ????????????????????? ?????????????????????.",ephemeral=False,delete_after=5)

            else:
                skipped_player = await self.MusicManager.skip(ctx, index)

                await interaction.send(content="??????????????? ???????????????!",ephemeral=False,delete_after=5)
                if not skipped_player.requester:
                    await ctx.send("Autoplaying next song.")
    async def previous(self, ctx,interaction:Interaction, index: int = None):

        if previous_player := await self.MusicManager.previous(
                ctx, index, no_autoplay=True
        ):
            await interaction.send(content=f"`{previous_player[0].title}`??? ???????????????!",ephemeral=False,delete_after=5)

    async def autoplay(self, ctx,interaction:Interaction):
        is_autoplay = await self.MusicManager.autoplay(ctx)

        if is_autoplay is not None:
            await interaction.send(content=f"????????? ???????????? ????????? {'???? ?????????' if is_autoplay else '???? ????????????'}?????????.\n???????????? ?????????????????? ????????? ?????? ?????????.",ephemeral=False,delete_after=5)

    async def shuffle(self, ctx,interaction:Interaction):
        is_shuffle = await self.MusicManager.shuffle(ctx)

        if is_shuffle is not None:
            await interaction.send(content=f"??????????????? {'???? ?????????' if is_shuffle else '???? ????????????'}?????????.\n???????????? ?????????????????? ????????? ?????? ?????????.",ephemeral=False,delete_after=5)

    async def join(self, interaction:Interaction):
        try:
            user = self.bot.get_guild(interaction.guild_id).get_member(interaction.user.id)
            await user.voice.channel.connect()
            await interaction.send("??????????????? ????????? ???????????????.",ephemeral=False,delete_after=5)
        except:
            print(str(traceback.format_exc()))
            await interaction.send("?????? ????????? ????????????.",ephemeral=False,delete_after=5)

    # async def playlists(self, interaction:Interaction):
    #     user = interaction.user
    #     user_playlists = await MusicManager.get_user_playlists(user)
    #
    #     if not user_playlists:
    #         await interaction.send(f"{user.mention}?????? ????????????????????? ?????? ????????????.",ephemeral=False,delete_after=5)
    #         return
    #
    #     formatted_playlists = [
    #         f"""**Title:** '{user_playlist.playlist.title}'
    #         Total Songs: {len(user_playlist.playlist.songs)}
    #         ID: `{user_playlist.id}`"""
    #         for user_playlist in user_playlists
    #     ]
    #
    #     embeds = discordSuperUtils.generate_embeds(
    #         formatted_playlists,
    #         f"{user}?????? ??????????????????",
    #         f"{user.mention}?????? ???????????? ????????? ???????????????.",
    #         15,
    #         string_format="{}",
    #     )
    #
    #     for embed in embeds:
    #         embed.timestamp = datetime.datetime.utcnow()
    #
    #     try:
    #         await user.send(embed=embeds)
    #     except discord.Forbidden:
    #         await interaction.respond(content="??????DM??? ?????????????????? ????????? ????????????. DM????????? ??????????????????.")

    # async def add(self, ctx, interaction:Interaction):
    #     if player := await self.MusicManager.now_playing(ctx):
    #         added_playlist = await MusicManager.add_playlist(ctx.author, player.url)
    #
    #         if not added_playlist:
    #             await interaction.respond("URL??? ??????????????????.")
    #             return
    #
    #         await interaction.respond(f"?????? ID??? ??????????????? ???????????????. `{added_playlist.id}`")



    topic = """
??? ????????????/????????????
??? ??????.
??? ?????????.
??? ??????.
???? ????????? ????????????.
???? ????????? ????????????.
???? ????????????.
??? ????????? ????????? ??? ???????????? ????????????.
???? ?????? ??????.
???? ?????? ???.
???? ????????? ????????????.
???? ??? ??????.
    """


    @commands.command(name="????????????")
    async def msetup(self,ctx):
        try:
            db = await aiosqlite.connect("db/db.sqlite")
            music_check = await DataBaseTool(db).check_db_music(ctx.guild)
            premium_cur = await db.execute("SELECT * FROM premium WHERE guild = ?",(ctx.guild.id,))
            premium_resp = await premium_cur.fetchone()
            if premium_resp == None:
                em = discord.Embed(title="????????????",colour=discord.Colour.random())
                em.add_field(name="??????", value="??????????????? ????????????????????????!")
            if not music_check:
                return await ctx.reply("??? ?????? ??????????????????????????????!")
            else:
                channel = await ctx.guild.create_text_channel(name="music setup", topic=self.topic)
                await channel.send("https://cdn.discordapp.com/icons/856829534926143538/4df4eac52287d066ded88084d1b728eb.webp?size=160")
                msg = await channel.send(content="** **\n**__????????? ??????__**:\n??????????????? ???????????? ??? ????????? ???????????? URL??? ??????????????????.",
                                        embed=self.default_music_embed(),
                                        components=[
                                            [
                                                Button(emoji="???", custom_id="music_pr"),
                                                Button(emoji="???", custom_id="music_stop"),
                                                Button(emoji="???", custom_id="music_previous"),
                                                Button(emoji="???", custom_id="music_skip"),
                                                Button(emoji="????", custom_id="music_shuffle")
                                            ],
                                            [
                                                Button(emoji="????", custom_id="music_volumedown"),
                                                Button(label="10%", emoji="????", disabled=True),
                                                Button(emoji="????", custom_id="music_volumeup"),
                                                Button(emoji="????", custom_id="music_queueloop"),
                                                Button(emoji="????", custom_id="music_oneloop")
                                            ],
                                            [
                                                Button(label="????????????", emoji="??????", custom_id="music_restart"),
                                                Button(emoji="????", custom_id="music_auto"),
                                                Button(emoji="????", custom_id="music_join"),
                                                Button(emoji="???", custom_id="music_cancel", style=4)
                                            ]
                                        ]
                                        )
                db = await aiosqlite.connect("db/db.sqlite")
                await DataBaseTool(db).add_music_data(ctx.guild,channel,msg)
                await ctx.send(
                    f"??????????????? ????????????({channel.mention})??? ???????????????!\n?????? ????????? ????????? ????????? ????????? ????????????????????? ??????????????????!")
        except:
            print(traceback.format_exc())
    @commands.Cog.listener("on_message")
    async def music_message(self,message):
        if message.author.bot:
            return
        ctx = await self.bot.get_context(message)
        db = await aiosqlite.connect("db/db.sqlite")
        conn = await db.execute("SELECT * FROM music WHERE guild = ?",(message.guild.id,))
        resp = await conn.fetchone()
        if not resp == None:
            if message.channel.id == resp[1]:
                await message.delete()
                await Musicsetup.play_cmd(self, ctx, message.content)

    @commands.Cog.listener(name="on_button_click")
    async def music_button_control(self,interaction:Interaction):
        ctx = await self.bot.get_context(interaction.message)
        db = await aiosqlite.connect("db/db.sqlite")
        conn = await db.execute("SELECT * FROM music WHERE guild = ?", (interaction.guild_id,))
        resp = await conn.fetchone()
        if interaction.custom_id.startswith("music_") and interaction.message.id == resp[2]:
            if not interaction.user.voice or not interaction.user.voice.channel:
                return await interaction.send("??????????????? ????????????????????????!",ephemeral=False,delete_after=5)
            if interaction.custom_id == "music_cancel":
                if await self.MusicManager.leave(ctx):
                    await self.set_default(ctx)
                    await interaction.send(content="???????????? ??????????????? ????????? ???????????????!",ephemeral=False,delete_after=5)
            elif interaction.custom_id == "music_pr":
                resp = await self.pause_resume(ctx)
                if resp['type']:
                    if resp['stat'] == "resume":
                        await interaction.send(content="????????? ???????????????!",ephemeral=False,delete_after=5)
                    else:
                        await interaction.send(content="????????? ?????????????????????.",ephemeral=False,delete_after=5)
            elif interaction.custom_id == "music_stop":
                await self.MusicManager.cleanup(voice_client=None, guild=ctx.guild)
                ctx.voice_client.stop()
                await interaction.send("????????? ???????????????.",ephemeral=False,delete_after=5)
            elif interaction.custom_id == "music_skip":
                await self.skip(ctx,interaction)
            elif interaction.custom_id == "music_shuffle":
                await self.shuffle(ctx,interaction)
            elif interaction.custom_id == "music_volumedown":
                await self.volume(ctx,interaction,type="down")
            elif interaction.custom_id == "music_volumeup":
                await self.volume(ctx,interaction,type="up")
            elif interaction.custom_id == "music_queueloop":
                await self.queueloop(ctx,interaction)
            elif interaction.custom_id == "music_oneloop":
                await self.loop(ctx,interaction)
            elif interaction.custom_id == "music_previous":
                await self.previous(ctx,interaction)
            elif interaction.custom_id == "music_auto":
                await self.autoplay(ctx,interaction)
            elif interaction.custom_id == "music_join":
                await self.join(interaction)
            elif interaction.custom_id == "music_restart":
                await self.restart(ctx, interaction)


def setup(bot):
    bot.add_cog(Musicsetup(bot))