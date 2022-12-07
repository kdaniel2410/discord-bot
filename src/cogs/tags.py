import discord
from datetime import datetime
from discord.ext import commands
from peewee import *
from models import Tag


class Tags(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def tag(self, ctx, target: str):
        try:
            tag = Tag.get(Tag.tag == target.lower())
            embed = discord.Embed(
                color=0x3584e4,
                description=tag.body,
                timestamp=datetime.now(),
                title=tag.tag.capitalize()
            )
            embed.set_footer(
                text=f'Requested by {ctx.author.name}', icon_url=ctx.author.avatar)
            await ctx.send(embed=embed)
        except DoesNotExist:
            await ctx.reply('That tag doesn\'t exist!')

    @commands.group()
    async def tags(self, ctx):
        if ctx.invoked_subcommand is None:
            with open('cogs/tags.txt') as f:
                embed = discord.Embed(
                    color=0x3584e4,
                    description=f.read(),
                    title='What the fuck are tags?',
                    timestamp=datetime.now()
                )
                embed.set_footer(
                    text=f'Requested by {ctx.author.name}', icon_url=ctx.author.avatar)
                await ctx.send(embed=embed)

    @tags.command()
    async def create(self, ctx, *args):
        try:
            Tag.create(
                tag=args[0].lower(),
                body=' '.join(args[1:]),
                created_by=ctx.author.id,
                guild_id=ctx.guild.id
            )
            await ctx.reply(f'Created! Send it with ``{ctx.prefix}tag {args[0].lower()}``')
        except IntegrityError:
            await ctx.reply('That tag is already in use!')

    @tags.command()
    async def delete(self, ctx, target: str):
        try:
            tag = Tag.get(Tag.tag == target.lower())
            if tag.created_by == ctx.author.id:
                tag.delete_instance()
                await ctx.reply(f'Deleted! Check on your other tags with ``{ctx.prefix}tags ls``')
            else:
                await ctx.reply('You can only delete your own tags!')
        except DoesNotExist:
            await ctx.reply('That tag doesn\'t exist!')

    @tags.command()
    async def ls(self, ctx):
        tags = Tag.select().where(Tag.created_by == ctx.author.id)
        if tags:
            tags_list = "\n".join(
                [f'{ctx.prefix}tag **{tag.tag}**' for tag in tags])
            embed = discord.Embed(
                color=0x3584e4,
                description=tags_list,
                title=f'Tag list',
                timestamp=datetime.now()
            )
            embed.set_footer(
                text=f'Requested by {ctx.author.name}', icon_url=ctx.author.avatar)
            await ctx.send(embed=embed)
        else:
            await ctx.reply('You haven\'t created any tags')
