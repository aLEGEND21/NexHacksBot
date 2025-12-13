import re

import discord
from discord.ui import Modal

from config import Config


class VerificationModal(Modal):
    def __init__(self, valid_phone_numbers: set[str]):
        super().__init__(title="Verification Form")
        self.valid_phone_numbers = (
            valid_phone_numbers  # Store valid phone numbers to look up against
        )

        self.add_item(
            discord.ui.InputText(
                label="Enter your phone number",
                placeholder="e.g. (123) 456-7890",
                style=discord.InputTextStyle.short,
            )
        )

    async def callback(self, interaction: discord.Interaction):
        phone_number = self.children[0].value

        # Extract only digits from the input
        digits_only = re.sub(r"\D", "", phone_number)

        # If 10 digits, assume country code 1
        if len(digits_only) == 10:
            digits_only = "1" + digits_only

        if digits_only not in self.valid_phone_numbers:
            await interaction.response.send_message(
                f":x: {interaction.user.mention}, the phone number `{phone_number}` is not recognized. Please try again.",
                ephemeral=True,
            )
            return

        # Add the verified role and remove the unverified role
        await interaction.user.add_roles(discord.Object(id=Config.VERIFIED_ROLE_ID))
        await interaction.user.remove_roles(
            discord.Object(id=Config.UNVERIFIED_ROLE_ID)
        )
        await interaction.response.send_message(
            f":white_check_mark: {interaction.user.mention}, you have been verified and given access to the server!",
            ephemeral=True,
        )
