import discord
from discord.ui import Button, View, button

from config import Config

from .verify_modal import VerificationModal


class VerifyMessageView(View):
    def __init__(self, attendee_data: dict[str, list[str]], valid_schools: list[str]):
        super().__init__(timeout=None)  # Persistent view
        self.attendee_data = attendee_data
        self.valid_schools = valid_schools

    @button(
        label="Verify", style=discord.ButtonStyle.blurple, custom_id="verify_button"
    )
    async def verify_button(self, button: Button, interaction: discord.Interaction):
        # Don't send the modal if the user already has the verified role
        if Config.VERIFIED_ROLE_ID in [role.id for role in interaction.user.roles]:
            await interaction.response.send_message(
                f":x: {interaction.user.mention}, you have already been verified.",
                ephemeral=True,
            )
            return

        # Send the verification modal
        modal = VerificationModal(
            attendee_data=self.attendee_data,
            valid_schools=self.valid_schools,
        )
        await interaction.response.send_modal(modal)
