import os

from dotenv import load_dotenv

load_dotenv()


class Config:
    # Environment Variables
    BOT_TOKEN = os.getenv("BOT_TOKEN")

    # Misc Settings
    ATTENDEES_CSV_PATH = "attendees.csv"
    UNVERIFIED_ROLE_ID = 1448126838235861013
    VERIFIED_ROLE_ID = 1448137431990800567
