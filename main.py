import discord

from config import Config

bot = discord.Bot()


@bot.event
async def on_ready():
    print(f"Logged in as {bot.user.name}#{bot.user.discriminator} (ID: {bot.user.id})")


@bot.command()
async def ping(ctx: discord.ApplicationContext):
    await ctx.respond(f"Pong! ({bot.latency * 1000:.0f}ms)")


bot.run(Config.BOT_TOKEN)
bot.run(Config.BOT_TOKEN)
