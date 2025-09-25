import discord
import time
from datetime import datetime
from discord.ext import commands
import tracemalloc
import json
from Leadbord import setup as play_setup

with open('config.json') as config_file:
    config = json.load(config_file)


TOKEN = config['token']
bot_Stuts = config['bot-status']








intents = discord.Intents.default()
intents = discord.Intents.all()
tracemalloc.start()
bot = commands.Bot(command_prefix='!', intents=intents)
bot.remove_command('help')
bot.start_time = time.time()
bot.last_restart_time = datetime.now().strftime("%m/%d/%Y %I:%M %p")




    
@bot.event
async def on_ready():
    global bot_invite_link
    bot_invite_link = discord.utils.oauth_url(bot.user.id, permissions=discord.Permissions(permissions=8))
    Stats = discord.Game(name=bot_Stuts, type=3)
    await bot.change_presence(status=discord.Status.online, activity=Stats)

    try:
        print(f'Logged in as {bot.user.name}')
        await bot.tree.sync() 
    except Exception as e:
        print(f"Error during setup: {str(e)}")



    command_count = len(bot.tree.get_commands())

    print(f"Bot logged in as {bot.user.name}")
    print(f"Bot is in {len(bot.guilds)} servers")
    print(f"Total commands registered: {command_count}")
    await bot.tree.sync()




@bot.tree.command(name="help", description="Shows all available commands")
async def help_command(interaction: discord.Interaction):
    current_time = datetime.now().strftime("%m/%d/%Y %I:%M %p")
    help_embed = discord.Embed(
        title="🆘 Bot Commands",
        description="Here are all the commands you can use:",
        color=discord.Color.from_rgb(38, 71, 38)
    )

    for command in bot.tree.get_commands():
        help_embed.add_field(name=f"``/{command.name}``", value=command.description, inline=False)

    help_embed.set_thumbnail(url=bot.user.avatar.url)
    help_embed.set_footer(text="Use the commands responsibly!")

    await interaction.response.send_message(embed=help_embed)
    print(f"Command Info: Help used by {interaction.user} on {current_time}")

def get_uptime(start_time):
    current_time = time.time()
    uptime_seconds = current_time - start_time
    uptime_str = time.strftime("%H:%M:%S", time.gmtime(uptime_seconds))
    return uptime_str
play_setup(bot)
bot.run(TOKEN)

