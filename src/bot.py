import discord
import os
from cogs.tags import Tags
from cogs.voice import Voice
from dotenv import load_dotenv
from discord.ext import commands

# Quit if the BOT_TOKEN environment variable has not been set.
load_dotenv()
if 'BOT_TOKEN' not in os.environ:
    print('BOT_TOKEN environment variable not set, quitting...')
    quit()

# Message content intent required.
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='?', intents=intents, help_command=None)


@bot.event
async def on_ready():
    await bot.add_cog(Tags(bot))
    await bot.add_cog(Voice(bot))


@bot.command()
async def joined(ctx, *, member: discord.Member):
    await ctx.send(f'{member} joined on {member.joined_at}')


@bot.command()
async def src(ctx):
    await ctx.reply("https://github.com/kdaniel2410/discord-bot")


bot.run(os.environ['BOT_TOKEN'])
