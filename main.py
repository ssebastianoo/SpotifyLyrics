import discord, config, os, aiohttp
from discord.ext import commands
from discord_slash import SlashCommand, SlashContext

os.environ["JISHAKU_NO_UNDERSCORE"] = "True"
os.environ["JISHAKU_NO_DM_TRACEBACK"] = "True"
os.environ["JISHAKU_HIDE"] = "True"

intents = discord.Intents.default()
intents.members = True
intents.presences = True
bot = commands.Bot(command_prefix=config.prefix, intents=intents)
slash = SlashCommand(bot, sync_commands=True, override_type=True)
bot.load_extension("jishaku")

@bot.event
async def on_ready():
    bot.session = aiohttp.ClientSession()
    print("ready as", bot.user)

for filename in os.listdir("./cogs"):
    if filename.endswith(".py"):
        bot.load_extension(f"cogs.{filename[:-3]}")

bot.run(config.token)
