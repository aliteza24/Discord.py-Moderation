import discord
from discord.ui import Button, View
from discord.ext import commands
import os
import asyncio
import json


client = commands.Bot(command_prefix="//", intents=discord.Intents.all())


@client.event
async def on_ready():
    print("Bot is Ready")



async def load():
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            await client.load_extension(f"cogs.{filename[:-3]}")


@client.event
async def on_guild_join(guild):
    with open("cogs/json/welcome.json", "r") as f:
        data = json.load(f)

    data[str(guild.id)] = {}
    data[str(guild.id)]["Channel"] = None
    data[str(guild.id)]["Message"] = None
    data[str(guild.id)]["AutoRole"] = None
    data[str(guild.id)]["ImageUrl"] = None

    with open("cogs/json/welcome.json", "w") as f:
        json.dump(data, f, indent=4)


@client.event
async def on_guild_remove(guild):
    with open("cogs/json/welcome.json", "r") as f:
        data = json.load(f)

    data.pop(str(guild.id))

    with open("cogs/json/welcome.json", "w") as f:
        json.dump(data, f, indent=4)



class Test(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)


    @discord.ui.button(label="Test", style=discord.ButtonStyle.red)
    async def test(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.channel.send(content="Click Kon")

    @discord.ui.button(label="Test2", style=discord.ButtonStyle.blurple)
    async def test2(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.channel.send(content="Xcity")

    @discord.ui.button(label="Tes432", style=discord.ButtonStyle.gray)
    async def test3(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.channel.send(content="mmd")


@commands.command(name="buttonmenu")
async def buttonmenu(interaction: discord.Interaction):
    await interaction.response.send_message(content="Button injas", view=Test())




@client.event
async def on_ready():
    print(f"Success")


@client.event
async def on_guild_join(guild):
    with open("cogs/json/warns.json", "r") as f:
        data = json.load(f)

    data[str(guild.id)] = {}

    for member in guild.members:
        data[str(guild.id)][str(member.id)] = {}
        data[str(guild.id)][str(member.id)]["Infractions"] = 0

        with open("cogs/json/warns.json", "w") as f:
            json.dump(data, f, indent=4)


@client.event
async def on_guild_remove(guild):
    with open("cogs/json/warns.json", "r") as f:
        data = json.load(f)

        data.pop(str(guild.id))

        with open("cogs/json/warns.json", "w") as f:
            json.dump(data, f, indent=4)


@client.command()
async def userinfo(ctx, member: discord.Member=None):
    if member is None:
        member = ctx.author
    elif member is not None:
        member = member

    info_embed = discord.Embed(title=f"{member.name}'s User inFormation", description="All information about user.", color=member.color)
    info_embed.set_thumbnail(url=member.avatar)
    info_embed.add_field(name="Name : ", value=member.name, inline=False)
    info_embed.add_field(name="Nick Name : ", value=member.display_name, inline=False)
    info_embed.add_field(name="Discriminator : ", value=member.discriminator, inline=False)
    info_embed.add_field(name="ID : ", value=member.id, inline=False)
    info_embed.add_field(name="Top Role", value=member.top_role, inline=False)
    info_embed.add_field(name="Roles : ", value=member.roles, inline=False)
    info_embed.add_field(name="Status : ", value=member.status, inline=False)
    info_embed.add_field(name="Bot / User?", value=member.bot, inline=False)
    info_embed.add_field(name="Activity : ", value=member.activity, inline=False)
    info_embed.add_field(name="Creation Date : ", value=member.created_at.__format__("%A, %d %B %Y @ %H:%M:%S"), inline=False)

    await ctx.send(embed=info_embed)



async def main():
    async with client:
        await load()
        await client.start("BOT TOKEN HERE")


asyncio.run(main())
