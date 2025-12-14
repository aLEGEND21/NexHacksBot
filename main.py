import csv
import json

import discord
from discord import commands

from components import VerifyMessageView
from config import Config

bot = discord.Bot()

# Load each column as a key in a dictionary
attendee_data = {}
with open(Config.ATTENDEES_CSV_PATH, "r") as f:
    reader = csv.DictReader(f)
    for row in reader:
        for key, value in row.items():
            attendee_data.setdefault(key, [])
            attendee_data[key].append(value)


# Load all schools
valid_schools = []
with open("schools.json", "r") as f:
    valid_schools = json.loads(f.read())


@bot.event
async def on_ready():
    print(f"Logged in as {bot.user.name}#{bot.user.discriminator} (ID: {bot.user.id})")
    bot.add_view(
        VerifyMessageView(attendee_data, valid_schools)
    )  # Register persistent view


@bot.command(name="ping", description="View the bot's latency")
async def ping(ctx: discord.ApplicationContext):
    await ctx.respond(f"Pong! ({bot.latency * 1000:.0f}ms)")


@bot.command(
    name="send_verify_msg",
    description="Send the verification message to a specific channel",
)
@discord.option(
    name="channel",
    description="Text channel to send the verification message to",
)
@commands.default_permissions(administrator=True)
async def send_verify_msg(
    ctx: discord.ApplicationContext, channel: discord.TextChannel
):
    await ctx.defer()

    # Create embed
    em = discord.Embed(
        title="Get Verified",
        description="Click the button below to get verified and gain access to the server!",
        color=discord.Color.blurple(),
    )
    em.set_thumbnail(url=ctx.guild.icon.url)

    # Send message with view
    await channel.send(embed=em, view=VerifyMessageView(attendee_data, valid_schools))
    await ctx.respond(
        f":white_check_mark: Verification message sent to {channel.mention}",
        ephemeral=True,
    )


bot.run(Config.BOT_TOKEN)
bot.run(Config.BOT_TOKEN)
