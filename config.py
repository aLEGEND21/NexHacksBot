import os

from dotenv import load_dotenv

load_dotenv()


class Config:
    # Environment Variables
    BOT_TOKEN = os.getenv("BOT_TOKEN")
    HACKER_ROLE_ID = int(os.getenv("HACKER_ROLE_ID"))
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    UNVERIFIED_ROLE_ID = int(os.getenv("UNVERIFIED_ROLE_ID"))
    VERIFIED_ROLE_ID = int(os.getenv("VERIFIED_ROLE_ID"))
    VERIFY_LOG_CHANNEL_ID = int(os.getenv("VERIFY_LOG_CHANNEL_ID"))

    # Misc Settings
    ATTENDEES_CSV_PATH = "attendees.csv"
