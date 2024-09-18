import os
import random
import aiohttp

import discord
from discord import app_commands
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv(override=True)

DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
intents = discord.Intents.all()
intents.message_content = True
intents.members = True
bot = commands.Bot(command_prefix="!", intents=intents)

RAT_ROLE_ID = 1284698617357008961
RAT_GUILD_ID = 1275092743559057458
RAT_GENERAL_CHANNEL_ID = 1275092743991066750

TEST_ROLE_ID = 1285691080758792252
TEST_GUILD_ID = 969399636995493899
TEST_GENERAL_CHANNEL_ID = 969399637557538949

actions = {
    0: 'LOADING SUPER SOAKERS WITH RAT URINE...',
    1: 'HIDING THE GOOD CHEESE...',
    2: 'THIS ONE SMELLS SUSPICIOUSLY OF CAT...',
    3: 'I HEARD ONE OF THEM PUTS EMPTY MILK JUGS BACK INTO THE FRIDGE...',
    4: 'THAT ONE ON THE LEFT DEFINITELY HASN\'T SHOWERED...',
    5: 'DOBEE, MAN THE TURRETS, THIS ONE DOESN\'T LOOK FRIENDLY...'
}


@bot.tree.command(name='rats', description='Activate the rat signal.')
@app_commands.checks.has_role(RAT_ROLE_ID)
@app_commands.guilds(RAT_GUILD_ID)
async def rats(interaction: discord.Interaction) -> None:
    await interaction.response.defer()

    response = f'NON-RATS DETECTED. {random.choice(list(actions.values()))}\n\n'

    if interaction.guild:
        for member in interaction.guild.members:
            roles = [role.id for role in member.roles]
            if RAT_ROLE_ID not in roles and member.id != 1285679750748049408:
                response += f"<@{member.id}> - Ratometer rating: {len(member.display_name) * '🐀'}\n"

    await interaction.followup.send(response)


@bot.tree.command(name='wiki', description='Search the archives for data.')
@app_commands.describe(search='What are you looking for?')
@app_commands.checks.has_role(RAT_ROLE_ID)
@app_commands.guilds(RAT_GUILD_ID)
async def wiki(interaction: discord.Interaction, search: str) -> None:
    await interaction.response.defer()

    # input cleanup
    clean_search = search.strip().replace(' ', '_')

    # build the URL
    url = f'https://oldschool.runescape.wiki/w/{clean_search}'

    # does article exist?
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            # article exists
            if response.status == 200:
                await interaction.followup.send(f'HERE IS THE INFORMATION YOU RATQUESTED, YOUR RATTINESS: {url}')
            else:
                search_url = f'https://oldschool.runescape.wiki/?search={search.strip().replace(" ", "+")}'
                await interaction.followup.send(f'RATS!  I COULDN\'T SNIFF IT OUT IT.  TRY THIS: {search_url}')


@bot.event
async def on_ready():
    print('Rattata online.')
    await bot.tree.sync(guild=discord.Object(RAT_GUILD_ID))
    await bot.get_channel(TEST_GENERAL_CHANNEL_ID).send("A wild Rattata appears!")


if DISCORD_TOKEN:
    bot.run(DISCORD_TOKEN)
