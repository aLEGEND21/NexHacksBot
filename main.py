import csv

import discord
from discord import commands

from components import VerifyMessageView
from config import Config

bot = discord.Bot()


# Load valid phone numbers from the file
valid_phone_numbers = set()
with open(Config.ATTENDEES_CSV_PATH, "r") as f:
    reader = csv.DictReader(f)
    for row in reader:
        phone = row["What is your phone number?"].strip()
        if phone:
            valid_phone_numbers.add(phone)


@bot.event
async def on_ready():
    print(f"Logged in as {bot.user.name}#{bot.user.discriminator} (ID: {bot.user.id})")
    bot.add_view(VerifyMessageView(valid_phone_numbers))  # Register persistent view


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
    await channel.send(embed=em, view=VerifyMessageView(valid_phone_numbers))
    await ctx.respond(
        f":white_check_mark: Verification message sent to {channel.mention}",
        ephemeral=True,
    )


bot.run(Config.BOT_TOKEN)
