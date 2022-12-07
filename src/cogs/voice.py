import discord
import youtube_dl
from datetime import datetime
from discord.ext import commands

ytdl_format_options = {
    'format': 'bestaudio/best',
    'noplaylist': True,
}


class Voice(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.queue = {}

    @commands.command()
    async def music(self, ctx):
        with open('cogs/music.txt') as f:
            embed = discord.Embed(
                color=0x3584e4,
                description=f.read(),
                timestamp=datetime.now(),
                title="Music"
            )
            embed.set_footer(
                text=f'Requested by {ctx.author.name}', icon_url=ctx.author.avatar)
        await ctx.send(embed=embed)

    @commands.command()
    async def play(self, ctx, url: str):
        def next(ctx):
            try:
                url = self.queue[ctx.guild.id].pop(0)
            except IndexError:
                return
            player = discord.FFmpegPCMAudio(url)
            player = discord.PCMVolumeTransformer(player)
            ctx.guild.voice_client.play(player, after=lambda e: next(ctx))

        if ctx.voice_client is None:
            await ctx.author.voice.channel.connect()

        async with ctx.typing():
            with youtube_dl.YoutubeDL(ytdl_format_options) as ytdl:
                data = await self.bot.loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=False))
            if ctx.voice_client.is_playing():
                try:
                    self.queue[ctx.guild.id] += data["url"]
                except KeyError:
                    self.queue[ctx.guild.id] = [data["url"], ]
                return await ctx.reply(f'**{data["title"]}** added to queue')

            player = discord.FFmpegPCMAudio(data['url'])
            player = discord.PCMVolumeTransformer(player)
            ctx.guild.voice_client.play(player, after=lambda e: next(ctx))
            await ctx.reply(f'Now playing **{data["title"]}!**')

    @commands.command()
    async def disconnect(self, ctx):
        if ctx.voice_client.is_playing():
            self.queue[ctx.guild.id] = []
            ctx.voice_client.stop()
        await ctx.guild.voice_client.disconnect()
        await ctx.reply('Disonnected from voice channel')

    @commands.command()
    async def pause(self, ctx):
        if ctx.voice_client.is_playing():
            ctx.voice_client.pause()
            await ctx.reply('Playback has been paused')
        elif ctx.voice_client.is_paused():
            await ctx.reply('Playback is already paused')
        else:
            await ctx.reply('Nothing is playing')

    @commands.command()
    async def resume(self, ctx):
        if ctx.voice_client.is_paused():
            ctx.voice_client.resume()
            await ctx.reply('Playback has been resumed')
        elif ctx.voice_client.is_playing():
            await ctx.reply('Playback is already in progress')
        else:
            await ctx.reply('Nothing is playing')

    @commands.command()
    async def skip(self, ctx):
        if not self.queue[ctx.guild.id]:
            await ctx.reply('There are no more songs in the queue')
        else:
            ctx.voice_client.stop()
            await ctx.reply('Skipping to the next song...')

    @commands.command()
    async def stop(self, ctx):
        if ctx.voice_client.is_playing() or ctx.voice_client.is_paused():
            self.queue[ctx.guild.id] = []
            ctx.voice_client.stop()
            await ctx.reply('Playback has been stopped')
        else:
            await ctx.reply('There is nothing to stop')

    @commands.command()
    async def clear(self, ctx):
        self.queue[ctx.guild.id] = []
        await ctx.reply('The queue has been cleared!')
