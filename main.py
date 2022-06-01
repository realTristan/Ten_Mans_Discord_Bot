from discord.ext import commands
from discord_components import *
from _sql import *
import discord, os

intents = discord.Intents(messages=True, guilds=True, reactions=True, members=True, presences=True)
client = commands.Bot(command_prefix='=', intents=intents)
client.remove_command('help')
    
# // REMOVE MEMBER FROM DATABASE WHEN THEY LEAVE THE SERVER
# //////////////////////////////////////////////////////////////
@client.event
async def on_member_remove(member):
    if await SqlData.exists(f"SELECT * FROM users WHERE guild_id = {member.guild.id} AND user_id = {member.id}"):
        await SqlData.execute(f"DELETE FROM users WHERE guild_id = {member.guild.id} AND user_id = {member.id}")

# // ON GUILD JOIN
# ////////////////////
@client.event
async def on_guild_join(guild):
    if not await SqlData.exists(f"SELECT * FROM settings WHERE guild_id = {guild.id}"):
        await SqlData.execute(f"INSERT INTO settings (guild_id, reg_role, match_categories, reg_channel, match_logs, mod_role, admin_role, self_rename) VALUES ({guild.id}, 0, 0, 0, 0, 0, 0, 0)")
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=f"{len(client.guilds)} Servers"))
   
# // ON GUILD REMOVE
# ////////////////////
@client.event
async def on_guild_remove(guild):
    for table in ["settings", "users", "lobbies", "lobby_settings", "matches", "maps", "bans", "elo_roles"]:
        if await SqlData.exists(f"SELECT * FROM {table} WHERE guild_id = {guild.id}"):
            await SqlData.execute(f"DELETE FROM {table} WHERE guild_id = {guild.id}")
   
# // ON BOT LAUNCH
# ///////////////////
@client.event
async def on_ready():
    DiscordComponents(client)
    print(f'Launched: {client.user.name} // {client.user.id}')
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=f"{len(client.guilds)} Servers"))

    # // LOAD THE COGS
    for filename in os.listdir(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'cogs')):
        if filename.endswith('.py'):
            client.load_extension(f'cogs.{filename[:-3]}')
            print(f'Loaded: cog.{filename[:-3]}')

client.run('YOUR BOT TOKEN')
