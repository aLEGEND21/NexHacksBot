import csv
import json
import os

import discord
from discord import commands

from components import VerifyMessageView
from config import Config

# Enable guild_members intent
intents = discord.Intents.default()
intents.members = True
bot = discord.Bot(intents=intents)

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
    em.set_thumbnail(url=ctx.guild.icon.url if ctx.guild.icon else None)

    # Send message with view
    await channel.send(embed=em, view=VerifyMessageView(attendee_data, valid_schools))
    await ctx.respond(
        f":white_check_mark: Verification message sent to {channel.mention}",
        ephemeral=True,
    )


@bot.command(
    name="get_names",
    description="Export all guild member names to a text file (Owner only)",
)
async def get_names(ctx: discord.ApplicationContext):
    await ctx.defer(ephemeral=True)

    # Owner ID check
    OWNER_ID = 416730155332009984
    if ctx.author.id != OWNER_ID:
        return await ctx.respond(
            ":x: This command is restricted to the bot owner.", ephemeral=True
        )

    try:
        # Chunk the guild to fetch all members (requires guild_members intent)
        await ctx.guild.chunk()

        # Parse names and extract first and last name
        names_list = []
        for member in ctx.guild.members:
            display_name = member.display_name
            # Split by "|" to separate name from school
            if "|" in display_name:
                name_part = display_name.split("|")[0].strip()
                # Add to list if name part is not empty
                if name_part:
                    names_list.append(name_part)

        # Write to file
        with open("discord_members.txt", "w", encoding="utf-8") as f:
            for name in names_list:
                f.write(f"{name}\n")

        await ctx.respond(
            f":white_check_mark: Successfully exported {len(names_list)} member names to `discord_members.txt`",
            file=discord.File("discord_members.txt"),
            ephemeral=True,
        )

        os.remove("discord_members.txt")
    except Exception as e:
        await ctx.respond(
            f":x: An error occurred while fetching members: {str(e)}",
            ephemeral=True,
        )


bot.run(Config.BOT_TOKEN)
