import discord
from urllib.parse import quote
from discord.ext import commands
from discord_slash import cog_ext, SlashContext
from discord_slash.utils.manage_commands import create_option

class Misc(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @cog_ext.cog_slash(name="invite", description="Invite the bot to your server")
    async def invite_slash(self, ctx: SlashContext):
        await self.invite(ctx)

    @commands.command()
    async def invite(self, ctx):
        "Invite the bot to your server"

        invite = discord.utils.oauth_url(self.bot.user.id, permissions=discord.Permissions(permissions=18432), scopes=('bot','applications.commands'))
        emb = discord.Embed(description=f"[Invite]({invite})", colour=discord.Colour.blurple())
        try:
            await ctx.reply(embed=emb, mention_author=False)
        except:
            await ctx.send(embed=emb)

def setup(bot):
    bot.add_cog(Misc(bot))
