
import traceback
import discord
from discord import embeds
from discord.ext import commands

import os
from discord.ext.commands.core import command
import pytz
import asyncio
import discord_components
import datetime
from discordSuperUtils import ModMailManager
from pycord_components import (
    Select,
    SelectOption,
    Button,
    ButtonStyle,
    Interaction
)
ticket_guild_id = 915551354800451616
category_id = 915561810411814973
close_ticket_category_id = 915561835267231774

# 오류 ~~~~ 37라인

class question(commands.Cog): # 야이 미친놈아 command.Cog가 뭐냐
    def __init__(self, bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        ctx = await self.bot.get_context(message)
        if message.author.bot:
            return
        # if message.content.startswith(["!", "#", "/", self.bot.command_prefix[0]]):
        #     return
        if message.content.startswith("!") or message.content.startswith("#") or message.content.startswith("ㅉ") or message.content.startswith("/") or message.content.startswith(self.bot.command_prefix[0]):
            return

        if str(message.channel.type) in "private":
            ticket_guild = self.bot.get_guild(ticket_guild_id)
            _lambda = list(
                filter(
                    lambda x: x.topic == str(ctx.author.id), ticket_guild.text_channels
                )
            )
            if _lambda:
                i = _lambda[0]
                if message.content == None: #?
                    if message.attachments:
                        lists = list(
                            map(
                                lambda attachment: f"[클릭해서 보기]({attachment.proxy_url})",
                                message.attachments,
                            )
                        )
                        await i.send(
                            embed=discord.Embed(
                                descripiton="(첨부파일을 보냈습니다)\n\n" + "\n".join(lists)
                            ).set_author(
                                icon_url=ctx.author.avatar_url,
                                name=f"{ctx.author} ({ctx.author.id})",
                            )
                        )
                        await message.add_reaction("✅")
                    elif message.stickers:
                        await i.send(
                            embed=discord.Embed(description="(스티커를 보냈습니다)")
                            .set_thumbnail(url=message.stickers[0].image_url)
                            .set_author(
                                icon_url=ctx.author.avatar_url,
                                name=f"{ctx.author} ({ctx.author.id})",
                            )
                        )
                        await message.add_reaction("✅")
                    else:
                        await i.send(
                            embed=discord.Embed(
                                description="(핸들링 되지 않은 메시지를 보냈습니다.)"
                            ).set_author(
                                icon_url=ctx.author.avatar_url,
                                name=f"{ctx.author} ({ctx.author.id})",
                            )
                        )
                        await message.add_reaction("✅")
                else:
                    await i.send(
                        embed=discord.Embed(description=message.content).set_author(
                            icon_url=ctx.author.avatar_url,
                            name=f"{ctx.author} ({ctx.author.id})",
                        )
                    )
                    await message.add_reaction("✅")
            else:
                if message.author.bot:
                    return
                open_ticket_category = ticket_guild.get_channel(category_id)
                embed1 = discord.Embed(title=f'문의',description =f"문의를 해주셔서 감사힙니다. \n 답변이 늦을수도 있으니 \n 기다려주세요. \n \n **문의한 모든 내용은 영구저장됩니다**" ,
                colour = discord.Colour.blue()
                )
                embed1.set_thumbnail(url="https://cdn.discordapp.com/avatars/915546504054333450/b26cea253b3433d2b84b7ec6b55b0a0e.webp?size=1024")
                embed1.add_field(name="**:warning:  주의사항**", value="`` 불필요한 문의는 제재 됩니다.`` \n \n ``관리자를 욕할시 처벌대상이 됩니다.`` \n \n ``관리자를 존중해주세요.``")
                await message.author.send(embed=embed1)
                embed2 = discord.Embed(title=f'카테고리' ,
                colour = discord.Colour.blue()
                )
                embed2.add_field(name="**카테고리**", value="아래 카테고리를 선택해서 버튼을 클릭해주세요.")
                embed2.add_field(name="🌀일반문의", value="일반문의는 어떤 제보나 신고를 하실때 \n 일반문의로 넣어주시면 됩니다")
                embed2.add_field(name="⛔오류제보", value="오류제보는 오류가 발생하거나 명령어 작동이 안될때 \n 오류제보로 넣어주시면 됩니다")
                embed2.add_field(name="❔궁금증", value="궁금증은 명령어를 어떻게 사용하는지 등 궁금할때  \n 궁금증으로 넣어주시면 됩니다")
                embed2.add_field(name="🚫신고", value="버그악용등 신고할때 \n 신고로 넣어주시면 됩니다")
                msg = await message.author.send(embed=embed2, components = [
                    Select(placeholder="문의",
                            options=[
                         SelectOption(label = "일반문의", emoji="🌀", description="일반문의는 어떤 제보나 신고를 하실때", value="il"),
                         SelectOption(label = "오류제보", emoji="⛔", description="오류제보는 오류가 발생하거나 명령어 작동이 안될때", value="war1"),
                         SelectOption(label = "궁금증", emoji="❔", description="궁금증은 명령어를 어떻게 사용하는지 등 궁금할때", value="qu"),
                         SelectOption(label = "신고", emoji="🚫", description="버그악용등 신고할때", value="sin"),
                         SelectOption(label = "문의취소", emoji = "❌", description="문의취소", value="cancel"),
                ]), 
                ],
                )
                embed3 = discord.Embed(title=f'문의',description =f"카테고리가 **일반문의**로 선택 됐습니다" ,
                colour = discord.Colour.blue()
                )
                embed4 = discord.Embed(title=f'문의',description =f"카테고리가 **오류제보**로 선택 됐습니다" ,
                colour = discord.Colour.blue()
                )
                embed5 = discord.Embed(title=f'문의',description =f"카테고리가 **궁금증**로 선택 됐습니다" ,
                colour = discord.Colour.blue()
                )
                embed6 = discord.Embed(title=f'문의',description =f"카테고리가 **신고**로 선택 됐습니다" ,
                colour = discord.Colour.blue()
                )
                now = datetime.datetime.now()
                year = now.year
                month = now.month
                date = now.day
                hour = now.hour
                minute = now.minute
                second = now.second
                open_time = f"{year}년 {month}월 {date}일 {hour}시 {minute}분 {second}초"
                try:
                    interaction = await self.bot.wait_for("select_option",
                                                        check=lambda i: i.user.id == ctx.author.id and i.message.id == msg.id,
                                                        timeout=60)
                    value = interaction.values[0]
                except asyncio.TimeoutError:
                    await msg.edit("시간이 초과되었어요!", components=[])
                    return
                if value  == "il":
                    ticket_channel = await open_ticket_category.create_text_channel(
                        f'일반-{message.author.dm_channel.id}({message.author.name})',
                        topic=f"{message.author.id}",
                        position = 1
                    )
                    await ticket_channel.send('<@866297659362246706>')
                    staff = ticket_guild.get_role(922067926247415848) # 이건 안넣냐
                    await ticket_channel.set_permissions(
                        staff,
                        read_messages=True,
                        send_messages=True,
                        read_message_history=True,
                    )
                    embed=discord.Embed(title="오토메시지",description=f"```fix\n티켓 개설일시: {open_time}```\n```티켓 개설 요청자: {message.author.name}({message.author.id})```",
                    color=0xf7fcfd)
                    embed.add_field(name="⛔ 연휴",
                                value="```연휴 일때 문의 왔을때```",
                                inline=False)
                    embed.add_field(name="🖨 느린 답변",
                                    value="```관리자들 비쁠때```",
                                    inline=False)
                    embed.add_field(name="❌ 티켓 종료",
                                    value="```현재 티켓을 종료해요.```",
                                    inline=False)

                    await ticket_channel.send(content=f"",
                                         embed=embed,
                                         components=[
                                            [
                                                Button(label="⛔ 연휴  ",custom_id="ticket_on",style=4),
                                                Button(label="🖨 느린 답변",custom_id="ticket_n",style=3),
                                                Button(label="❌ 티켓 종료",custom_id="ticket_clos",style=4)
                                            ]
                                         ])
                    await ticket_channel.send(
                        embed=discord.Embed(description=message.content).set_author(
                            icon_url=ctx.author.avatar_url,
                            name=f"{ctx.author} ({ctx.author.id})",
                        )
                    )
                    await message.add_reaction("✅")
                    await msg.edit(embed=embed3, components=[])
                if value  == "war1":
                    ticket_channel = await open_ticket_category.create_text_channel(
                        f'오류-{message.author.dm_channel.id}({message.author.name})',
                        topic=f"{message.author.id}",
                        position = 1
                    )# 이건 안넣냐
                    await ticket_channel.send('<@866297659362246706>')
                    staff = ticket_guild.get_role(922067926247415848) # 이건 안넣냐
                    await ticket_channel.set_permissions(
                        staff,
                        read_messages=True,
                        send_messages=True,
                        read_message_history=True,
                    )
                    embed=discord.Embed(title="오토메시지",description=f"```fix\n티켓 개설일시: {open_time}```\n```티켓 개설 요청자: {message.author.name}({message.author.id})```",
                    color=0xf7fcfd)
                    embed.add_field(name="⛔ 연휴",
                                value="```연휴 일때 문의 왔을때```",
                                inline=False)
                    embed.add_field(name="🖨 느린 답변",
                                    value="```관리자들 비쁠때```",
                                    inline=False)
                    embed.add_field(name="❌ 티켓 종료",
                                    value="```현재 티켓을 종료해요.```",
                                    inline=False)

                    await ticket_channel.send(content=f"",
                                         embed=embed,
                                         components=[
                                            [
                                                Button(label="⛔ 연휴  ",custom_id="ticket_on",style=4),
                                                Button(label="🖨 느린 답변",custom_id="ticket_n",style=3),
                                                Button(label="❌ 티켓 종료",custom_id="ticket_clos",style=4)
                                            ]
                                         ])
                    await ticket_channel.send(
                        embed=discord.Embed(description=message.content).set_author(
                            icon_url=ctx.author.avatar_url,
                            name=f"{ctx.author} ({ctx.author.id})",
                        )
                    )
                    await message.add_reaction("✅")
                    await msg.edit(embed=embed4, components=[])
                if value  == "qu":
                    ticket_channel = await open_ticket_category.create_text_channel(
                        f'궁금증-{message.author.dm_channel.id}({message.author.name})',
                        topic=f"{message.author.id}",
                        position = 1
                    )# 이건 안넣냐
                    await ticket_channel.send('<@866297659362246706>')
                    staff = ticket_guild.get_role(922067926247415848) # 이건 안넣냐
                    await ticket_channel.set_permissions(
                        staff,
                        read_messages=True,
                        send_messages=True,
                        read_message_history=True,
                    )
                    embed=discord.Embed(title="오토메시지",description=f"```fix\n티켓 개설일시: {open_time}```\n```티켓 개설 요청자: {message.author.name}({message.author.id})```",
                    color=0xf7fcfd)
                    embed.add_field(name="⛔ 연휴",
                                value="```연휴 일때 문의 왔을때```",
                                inline=False)
                    embed.add_field(name="🖨 느린 답변",
                                    value="```관리자들 비쁠때```",
                                    inline=False)
                    embed.add_field(name="❌ 티켓 종료",
                                    value="```현재 티켓을 종료해요.```",
                                    inline=False)

                    await ticket_channel.send(content=f"",
                                         embed=embed,
                                         components=[
                                            [
                                                Button(label="⛔ 연휴  ",custom_id="ticket_on",style=4),
                                                Button(label="🖨 느린 답변",custom_id="ticket_n",style=3),
                                                Button(label="❌ 티켓 종료",custom_id="ticket_clos",style=4)
                                            ]
                                         ])
                    await ticket_channel.send(
                        embed=discord.Embed(description=message.content).set_author(
                            icon_url=ctx.author.avatar_url,
                            name=f"{ctx.author} ({ctx.author.id})",
                        )
                    )
                    await message.add_reaction("✅")
                    await msg.edit(embed=embed5, components=[])
                if value  == "sin":
                    ticket_channel = await open_ticket_category.create_text_channel(
                        f'신고-{message.author.dm_channel.id}({message.author.name})',
                        topic=f"{message.author.id}",
                        position = 1
                    )# 이건 안넣냐
                    await ticket_channel.send('<@866297659362246706>')
                    staff = ticket_guild.get_role(922067926247415848) # 이건 안넣냐
                    await ticket_channel.set_permissions(
                        staff,
                        read_messages=True,
                        send_messages=True,
                        read_message_history=True,
                    )
                    embed=discord.Embed(title="오토메시지",description=f"```fix\n티켓 개설일시: {open_time}```\n```티켓 개설 요청자: {message.author.name}({message.author.id})```",
                    color=0xf7fcfd)
                    embed.add_field(name="⛔ 연휴",
                                value="```연휴 일때 문의 왔을때```",
                                inline=False)
                    embed.add_field(name="🖨 느린 답변",
                                    value="```관리자들 비쁠때```",
                                    inline=False)
                    embed.add_field(name="❌ 티켓 종료",
                                    value="```현재 티켓을 종료해요.```",
                                    inline=False)

                    await ticket_channel.send(content=f"",
                                         embed=embed,
                                         components=[
                                            [
                                                Button(label="⛔ 연휴  ",custom_id="ticket_on",style=4),
                                                Button(label="🖨 느린 답변",custom_id="ticket_n",style=3),
                                                Button(label="❌ 티켓 종료",custom_id="ticket_clos",style=4)
                                            ]
                                         ])
                    await ticket_channel.send(
                        embed=discord.Embed(description=message.content).set_author(
                            icon_url=ctx.author.avatar_url,
                            name=f"{ctx.author} ({ctx.author.id})",
                        )
                    )
                    await message.add_reaction("✅")
                    await msg.edit(embed=embed6, components=[])
                if value == "cancel":
                    try:
                        embed7=discord.Embed(title="문의취소", description="문의 취소완료",colour=discord.Colour.random())
                        await msg.edit(embed=embed7, components=[])
                    
                    except:
                        print(traceback.format_exc())
        elif str(message.channel.type) != "private":
            try:
                if message.channel.category.id == category_id:
                    await (await self.bot.fetch_user(int(message.channel.topic))).send(
                        embed=discord.Embed(
                            title="** 문의 답변 **",
                            description=f"**`관리자` {message.author.name}** : {message.content}",
                            colour = discord.Colour.blue(),
                            )
                        )
                    await message.add_reaction("✅")
            except:
                pass
    # @commands.command(name="티켓오픈")
    # @commands.is_owner()
    # async def on_message(self, ctx, user_id:int):
    #     user = await self.bot.fetch_user(user_id)
    #     ticket_guild = self.bot.get_guild(ticket_guild_id)
    #     open_ticket_category = ticket_guild.get_channel(category_id)
    #     ticket_channel = await open_ticket_category.create_text_channel(
    #                         f'일반-{user.id}{user.name}',
    #                         topic=f"{user_id}",
    #                         position = 1
    #                     )
    #     staff = ticket_guild.get_role(922067926247415848) # 이건 안넣냐
    #     await ticket_channel.set_permissions(
    #                     staff,
    #                     read_messages=True,
    #                     send_messages=True,
    #                     read_message_history=True,
    #                 )
    #     await asyncio.sleep(2)
    #     await user.send(
    #         embed = discord.Embed(title=f'문의',
    #         description ="안녕하세요 봇개발자로 부터 티켓이 열렸습니다.",
    #         colour = discord.Colour.blue(),
    #         ).set_thumbnail(url="https://cdn.discordapp.com/avatars/915546504054333450/b26cea253b3433d2b84b7ec6b55b0a0e.webp?size=1024")
            
    #     )
    #     await ctx.send("티켓오픈!")
    @commands.Cog.listener(name="on_button_click")
    async def ticket_auto_control(self,interaction:Interaction):
        custom_id = interaction.custom_id
        ctx = await self.bot.get_context(interaction.message)
        if custom_id == "ticket_on":
            if ctx.channel.category.id == category_id:
                    await (await self.bot.fetch_user(int(ctx.channel.topic))).send(
                        embed=discord.Embed(
                            title="** 문의 답변 **",
                            description=f"**시스템**\n현재 __공휴일__입니다. \n답변이 늦거나 공휴일이 끝난 후에 답변을 드리겠습니다. \n양해 부탁드립니다",
                            colour = discord.Colour.blue(),
                            )
                        )
                    await interaction.send("#전송완료",ephemeral=False)
        if custom_id == "ticket_n":
            if ctx.channel.category.id == category_id:
                    await (await self.bot.fetch_user(int(ctx.channel.topic))).send(
                        embed=discord.Embed(
                            title="** 문의 답변 **",
                            description=f"**시스템**\n현재 관리자가 __바쁜__ 관계로 답변이 늦을 수도 있습니다. \n양해 부탁드립니다",
                            colour = discord.Colour.blue(),
                            )
                        )
                    await interaction.send("#전송완료",ephemeral=False)
        if custom_id == "ticket_clos":
            ticket_guild = self.bot.get_guild(ticket_guild_id)
            ticket_channel = self.bot.get_channel(ctx.channel.id)
            await (await self.bot.fetch_user(int(ctx.channel.topic))).send(
                embed = discord.Embed(title=f'문의종료',
                description =f"문의를 해주셔서 감사합니다! \n**더욱 더 성장있는 짱구가 되겠습니다** \n**문의한 내용들은 영구적으로 보관되며 삭제가 불가능합니다** \n \n 감사합니다!",
                colour = discord.Colour.blue(),
                ).set_thumbnail(url="https://cdn.discordapp.com/avatars/915546504054333450/b26cea253b3433d2b84b7ec6b55b0a0e.webp?size=1024")
                
            )
            await ctx.channel.edit(
                topic="close-{}".format(ctx.channel.name),
                category=ticket_guild.get_channel(close_ticket_category_id),
                position = len(ctx.channel.category.channels)
            )
            await ctx.channel.edit(
                name = ctx.channel.topic
            )
            embed = discord.Embed(
                colour=0xFF00, title="문의종료", description=f"잠금 요청 유저 : {ctx.author}"
            )
            embed.set_footer(text=ctx.author.name, icon_url=ctx.author.avatar_url)
            await interaction.send(embed=embed,ephemeral=False)
            await ctx.send(embed=embed,ephemeral=False)
    @commands.command(name="문의종료", aliases=["종료", "close"])
    @commands.has_permissions(administrator=True)
    async def ticket_end(self, ctx):
        await ctx.message.delete()
        ticket_guild = self.bot.get_guild(ticket_guild_id)
        ticket_channel = self.bot.get_channel(ctx.channel.id)
        await (await self.bot.fetch_user(int(ctx.channel.topic))).send(
            embed = discord.Embed(title=f'문의종료',
            description =f"문의를 해주셔서 감사합니다! \n**더욱 더 성장있는 짱구가 되겠습니다** \n**문의한 내용들은 영구적으로 보관되며 삭제가 불가능합니다** \n \n 감사합니다!",
            colour = discord.Colour.blue(),
            ).set_thumbnail(url="https://cdn.discordapp.com/avatars/915546504054333450/b26cea253b3433d2b84b7ec6b55b0a0e.webp?size=1024")
            
        )
        await ctx.channel.edit(
            topic="close-{}".format(ctx.channel.name),
            category=ticket_guild.get_channel(close_ticket_category_id),
            position = len(ctx.channel.category.channels)
        )
        await ctx.channel.edit(
            name = ctx.channel.topic
        )
        embed = discord.Embed(
            colour=0xFF00, title="문의종료", description=f"잠금 요청 유저 : {ctx.author}"
        )
        embed.set_footer(text=ctx.author.name, icon_url=ctx.author.avatar_url)
        await ctx.send(embed=embed)
    # @commands.command(name="", aliases=["종료", "close"])
    # @commands.has_permissions(administrator=True)
    # async def ticket_option(self, ctx):
    #     await ctx.message.delete()
    #     ticket_guild = self.bot.get_guild(ticket_guild_id)
    #     ticket_channel = self.bot.get_channel(ctx.channel.id)
    #     await (await self.bot.fetch_user(int(ctx.channel.topic))).send(
    #         embed = discord.Embed(title=f'문의종료',
    #         description =f"문의를 해주셔서 감사합니다! \n**더욱 더 성장있는 짱구가 되겠습니다** \n**문의한 내용들은 영구적으로 보관되며 삭제가 불가능합니다** \n \n 감사합니다!",
    #         colour = discord.Colour.blue(),
    #         ).set_thumbnail(url="https://cdn.discordapp.com/avatars/915546504054333450/b26cea253b3433d2b84b7ec6b55b0a0e.webp?size=1024")
            
    #     )
    #     await ctx.channel.edit(
    #         topic="close-{}".format(ctx.channel.name),
    #         category=ticket_guild.get_channel(close_ticket_category_id),
    #         position = len(ctx.channel.category.channels)
    #     )
    #     await ctx.channel.edit(
    #         name = ctx.channel.topic
    #     )
    #     embed = discord.Embed(
    #         colour=0xFF00, title="문의종료", description=f"잠금 요청 유저 : {ctx.author}"
    #     )
    #     embed.set_footer(text=ctx.author.name, icon_url=ctx.author.avatar_url)
    #     await ctx.send(embed=embed)
    # @commands.command(name="문의종료", aliases=["종료", "close"])
    # @commands.has_permissions(administrator=True)
    # async def ticket_end(self, ctx):
    #     await ctx.message.delete()
    #     ticket_guild = self.bot.get_guild(ticket_guild_id)
    #     ticket_channel = self.bot.get_channel(ctx.channel.id)
    #     await (await self.bot.fetch_user(int(ctx.channel.topic))).send(
    #         embed = discord.Embed(title=f'문의종료',
    #         description =f"문의를 해주셔서 감사합니다! \n**더욱 더 성장있는 짱구가 되겠습니다** \n**문의한 내용들은 영구적으로 보관되며 삭제가 불가능합니다** \n \n 감사합니다!",
    #         colour = discord.Colour.blue(),
    #         ).set_thumbnail(url="https://cdn.discordapp.com/avatars/915546504054333450/b26cea253b3433d2b84b7ec6b55b0a0e.webp?size=1024")
            
    #     )
    #     await ctx.channel.edit(
    #         topic="close-{}".format(ctx.channel.name),
    #         category=ticket_guild.get_channel(close_ticket_category_id),
    #         position = len(ctx.channel.category.channels)
    #     )
    #     await ctx.channel.edit(
    #         name = ctx.channel.topic
    #     )
    #     embed = discord.Embed(
    #         colour=0xFF00, title="문의종료", description=f"잠금 요청 유저 : {ctx.author}"
    #     )
    #     embed.set_footer(text=ctx.author.name, icon_url=ctx.author.avatar_url)
    #     await ctx.send(embed=embed)
    # @commands.command(name="문의종료", aliases=["종료", "close"])
    # @commands.has_permissions(administrator=True)
    # async def ticket_end(self, ctx):
    #     await ctx.message.delete()
    #     ticket_guild = self.bot.get_guild(ticket_guild_id)
    #     ticket_channel = self.bot.get_channel(ctx.channel.id)
    #     await (await self.bot.fetch_user(int(ctx.channel.topic))).send(
    #         embed = discord.Embed(title=f'문의종료',
    #         description =f"문의를 해주셔서 감사합니다! \n**더욱 더 성장있는 짱구가 되겠습니다** \n**문의한 내용들은 영구적으로 보관되며 삭제가 불가능합니다** \n \n 감사합니다!",
    #         colour = discord.Colour.blue(),
    #         ).set_thumbnail(url="https://cdn.discordapp.com/avatars/915546504054333450/b26cea253b3433d2b84b7ec6b55b0a0e.webp?size=1024")
            
    #     )
    #     await ctx.channel.edit(
    #         topic="close-{}".format(ctx.channel.name),
    #         category=ticket_guild.get_channel(close_ticket_category_id),
    #         position = len(ctx.channel.category.channels)
    #     )
    #     await ctx.channel.edit(
    #         name = ctx.channel.topic
    #     )
    #     embed = discord.Embed(
    #         colour=0xFF00, title="문의종료", description=f"잠금 요청 유저 : {ctx.author}"
    #     )
    #     embed.set_footer(text=ctx.author.name, icon_url=ctx.author.avatar_url)
    #     await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(question(bot))
