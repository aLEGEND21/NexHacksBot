import os

from dotenv import load_dotenv

load_dotenv()


class Config:
    # Environment Variables
    BOT_TOKEN = os.getenv("BOT_TOKEN")
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

    # Misc Settings
    ATTENDEES_CSV_PATH = "attendees.csv"
    UNVERIFIED_ROLE_ID = 1448126838235861013
    VERIFIED_ROLE_ID = 1448137431990800567
    VERIFY_LOG_CHANNEL_ID = 1449196934211567667
