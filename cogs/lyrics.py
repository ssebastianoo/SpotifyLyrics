import discord
from urllib.parse import quote
from discord.ext import commands
from discord_slash import cog_ext, SlashContext
from discord_slash.utils.manage_commands import create_option

class Lyrics(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @cog_ext.cog_slash(name="lyrics", description="Get the lyrics of a song a member is listening to", options=[create_option(
            name="member",
            description="The member you want to get info about",
            option_type=6,
            required=False,
        )])
    async def settings_slash(self, ctx: SlashContext, member=None):
        if not member:
            member = ctx.guild.get_member(ctx.author.id)
        await self.lyrics(ctx, member)

    @commands.command()
    async def lyrics(self, ctx, member: discord.Member=None):
        member = member or ctx.author
        activities = [activity for activity in member.activities if activity.type == discord.ActivityType.listening]

        if len(activities) == 0:
            emb = discord.Embed(description=f"{member.mention} isn't listening to Spotify at the moment.", colour=discord.Colour.red())
            try: await ctx.reply(embed=emb, mention_author=False)
            except: await ctx.send(embed=emb)
            return

        activity = activities[0]
        title = activity.title
        artists = activity.artist
        query = quote(title + " " + artists)

        res = await self.bot.session.get(f"https://some-random-api.ml/lyrics?title={query}")
        data = await res.json()

        if data.get("error"):
            emb = discord.Embed(description=data.get("error"), colour=discord.Colour.red())
            try: await ctx.reply(embed=emb, mention_author=False)
            except: await ctx.send(embed=emb)
            return

        emb = discord.Embed(title=f"{data['author']} | {data['title']}", description=data["lyrics"], colour=activity.colour)
        emb.set_author(name=str(member), icon_url=str(member.avatar_url_as(static_format="png")))
        emb.set_thumbnail(url=activity.album_cover_url)

        try: await ctx.reply(embed=emb, mention_author=False)
        except: await ctx.send(embed=emb)

def setup(bot):
    bot.add_cog(Lyrics(bot))
