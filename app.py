import discord

import discord, datetime, json 
from discord.ui import InputText, Modal
from discord.commands import Option
from discord.ui import Button, View, Select
import asyncio
import pymysql 
intents = discord.Intents.all()
client = discord.Bot(intents=intents)

Table_name = 테이블네임

class MyModal(discord.ui.Modal):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(
            discord.ui.InputText(
                label="뉴비인증코드",
                placeholder="뉴비인증코드",
            ),
            *args,
            **kwargs,
        )
    async def callback(self, interaction: discord.Interaction):
        conn = pymysql.connect(host='localhost', user='root', password='password', charset='utf8') 
        cur = conn.cursor() 
        try:
            code = int(self.children[0].value)
        except ValueError:
            return await interaction.user.send("예시: **뉴비인증#312512**")
        
        await cur.execute(f'select code from {Table_name} where code = "{code}"')
        check = await cur.fetchone()

        if len(code) == 0:
            return await interaction.user.send(f"{interaction.user.mention}, 예시: **뉴비인증#312512**")
        elif check is None:
            return await interaction.user.send(f"{interaction.user.mention}, 예시: **뉴비인증#312512**")
        else:
            await cur.execute(f'select * from {Table_name} where state = "0" and code = "{code}"')
            check1 = await cur.fetchone()

            await cur.execute(f'select * from {Table_name} where state = "1" and code = "{code}"')
            check2 = await cur.fetchone()

            await cur.execute(f'select * from {Table_name} where state = "2" and code = "{code}"')
            check3 = await cur.fetchone()

            if check1 is not None:
                await cur.execute(f'update {Table_name} set state = "1" where code = "{code}"')
                await interaction.user.send('%a 인증 완료'.format(interaction.author.mention))
                return await interaction.user.add_roles(discord.utils.get(interaction.guild.roles, id=역할아이디))
            elif check2 is not None:
                await interaction.user.send('%a 인증 완료'.format(interaction.author.mention))
                return await interaction.user.add_roles(discord.utils.get(interaction.guild.roles, id=역할아이디))


@client.event()
async def on_message(message):
    if message.author.id == 837963769098928169:
        if message.content == '!뉴비':
            main_view = View()
            main_view.add_item(Button(label="카리너서버 뉴비 인증", tyle=discord.ButtonStyle.primary, custom_id="newbie"))
            main_view.stop()
            await message.channel.send("@everyone",embed=discord.Embed(color=0x5865F2, title="뉴비인증 티켓", description="인증 원하시면 아래 버튼을 눌러 인증양식을 작성해주세요."), view=main_view)
    
    if message.contnet =='** **':
        await message.delte()

@client.listen("on_interaction")
async def on_interaction(interaction):
    if not interaction.is_component():
        return
    if not interaction.data["component_type"] == 2:
        return
    custom_id = interaction.data["custom_id"]
    
    if custom_id == "newbie":
        view = MyModal()
        await interaction.response.send_modal(view)
        await interaction.response.send_message(f"** **")



client.run("4")