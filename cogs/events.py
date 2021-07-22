import discord
from discord.ext import commands

class Events(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):

        if isinstance(error, commands.CommandNotFound):
            return

        emb = discord.Embed(description=f"```py\n{error}\n```", colour=discord.Colour.red())
        try:
            await ctx.reply(embed=emb, mention_author=False)
        except:
            await ctx.send(embed=emb)

def setup(bot):
    bot.add_cog(Events(bot))
