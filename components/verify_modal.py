import json
import re

import discord
from discord.ui import Modal
from openai import AsyncOpenAI

from config import Config

phone_number_key = "What is your phone number?"
fname_key = "What's your first name?"
lname_key = "What's your last name?"
school_key = "What school/university do you go to?"

# Create AsyncOpenAI client
openai_client = AsyncOpenAI(api_key=Config.OPENAI_API_KEY)


class VerificationModal(Modal):
    def __init__(self, attendee_data: dict[str, list[str]], valid_schools: list[str]):
        super().__init__(title="Verification Form")
        self.attendee_data = attendee_data
        self.valid_schools = valid_schools

        self.add_item(
            discord.ui.InputText(
                label="Enter your phone number",
                placeholder="e.g. (123) 456-7890",
                style=discord.InputTextStyle.short,
            )
        )

    async def callback(self, interaction: discord.Interaction):
        await interaction.response.defer()

        valid_phone_numbers = self.attendee_data[phone_number_key]
        phone_number = self.children[0].value

        # Extract only digits from the input
        digits_only = re.sub(r"\D", "", phone_number)

        # If 10 digits and not in the valid phone numbers, assume country code 1
        if len(digits_only) == 10 and digits_only not in valid_phone_numbers:
            digits_only = "1" + digits_only

        if digits_only not in valid_phone_numbers:
            await interaction.followup.send(
                f":x: {interaction.user.mention}, the phone number `{phone_number}` is not recognized. Please try again.",
                ephemeral=True,
            )

            # Log that the user failed to verify
            log_channel = interaction.guild.get_channel(Config.VERIFY_LOG_CHANNEL_ID)
            if log_channel:
                em = discord.Embed(
                    description=f"{interaction.user.mention} failed to verify with phone number `{phone_number}`.",
                    color=discord.Color.red(),
                    timestamp=discord.utils.utcnow(),
                )
                em.set_author(
                    name=f"Failed to Verify {interaction.user.name}",
                    icon_url=interaction.user.display_avatar.url,
                )
                em.set_footer(text=f"User ID: {interaction.user.id}")
                await log_channel.send(embeds=[em])

            return

        # Pull the school from the attendee data and have ChatGPT reformat it to be one of the ones from the
        # schools.json file
        idx = valid_phone_numbers.index(digits_only)
        school = self.attendee_data[school_key][idx]
        response = await openai_client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": f"You are a helpful assistant that reformats school names to be one of the ones from the below list: `{', '.join(self.valid_schools)}`",
                },
                {
                    "role": "user",
                    "content": f"Reformat the school name `{school}` to match one from the list. Return your response as a JSON object with a 'school' key containing the reformatted school name.",
                },
            ],
            response_format={"type": "json_object"},
        )
        fmt_school = json.loads(response.choices[0].message.content)["school"]

        # Update the user's nickname to be their first and last name
        first_name = self.attendee_data[fname_key][idx]
        last_name = self.attendee_data[lname_key][idx]
        await interaction.user.edit(nick=f"{first_name} {last_name} | {fmt_school}")

        # Add the verified role and remove the unverified role
        await interaction.user.add_roles(discord.Object(id=Config.VERIFIED_ROLE_ID))
        await interaction.user.remove_roles(
            discord.Object(id=Config.UNVERIFIED_ROLE_ID)
        )
        await interaction.followup.send(
            f":white_check_mark: {interaction.user.mention}, you have been verified and given access to the server!",
            ephemeral=True,
        )

        # Log that the user verified
        log_channel = interaction.guild.get_channel(Config.VERIFY_LOG_CHANNEL_ID)
        if log_channel:
            em = discord.Embed(
                description=f"{interaction.user.mention} verified with phone number `{digits_only}`.",
                color=discord.Color.green(),
                timestamp=discord.utils.utcnow(),
            )
            em.set_author(
                name=f"Verified {interaction.user.name}",
                icon_url=interaction.user.display_avatar.url,
            )
            em.set_footer(text=f"User ID: {interaction.user.id}")
            await log_channel.send(embeds=[em])
