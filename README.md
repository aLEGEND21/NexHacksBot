# NexHacks Discord Bot

A Discord bot created for the **NexHacks @ CMU** hackathon to help organize and manage the Discord server. The bot provides an automated verification system that allows registered attendees to verify their identity and gain access to the server.

## Features

- **Phone Number Verification**: Users verify their identity by entering their phone number, which is cross-referenced against the attendee registration data
- **Automatic Role Management**: Automatically assigns verified and hacker roles while removing unverified roles upon successful verification
- **Smart School Name Normalization**: Uses OpenAI's GPT-4o-mini to intelligently reformat school names to match a standardized list
- **Nickname Updates**: Automatically updates user nicknames to display their first name, last name, and school (e.g., "John Doe | Carnegie Mellon")
- **Verification Logging**: Logs all verification attempts (successful and failed) to a designated channel
- **Admin Commands**: Includes administrative commands for sending verification messages and exporting member data

## Prerequisites

- Python 3.13+
- Discord Bot Token
- OpenAI API Key
- Discord Server with the following:
  - A channel for verification messages
  - A channel for verification logs
  - Roles: `HACKER_ROLE_ID`, `VERIFIED_ROLE_ID`, `UNVERIFIED_ROLE_ID`

## Setup

### 1. Clone the Repository

```bash
git clone <repository-url>
cd NexHacksBot
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure Environment Variables

Create a `.env` file in the root directory with the following variables:

```env
BOT_TOKEN=your_discord_bot_token
HACKER_ROLE_ID=your_hacker_role_id
OPENAI_API_KEY=your_openai_api_key
UNVERIFIED_ROLE_ID=your_unverified_role_id
VERIFIED_ROLE_ID=your_verified_role_id
VERIFY_LOG_CHANNEL_ID=your_log_channel_id
```

### 4. Prepare Required Files

- **`attendees.csv`**: A CSV file containing attendee registration data with the following columns:

  - `What is your phone number?`
  - `What's your first name?`
  - `What's your last name?`
  - `What school/university do you go to?`

- **`schools.json`**: A JSON array containing the list of valid school names (already included in the repository)

### 5. Enable Discord Intents

Make sure to enable the **Server Members Intent** in your Discord Application settings:

1. Go to https://discord.com/developers/applications
2. Select your application
3. Navigate to the "Bot" section
4. Enable "SERVER MEMBERS INTENT" under "Privileged Gateway Intents"

## Usage

### Running Locally

```bash
python main.py
```

### Running with Docker

Build and run using Docker Compose:

```bash
docker-compose up -d
```

The bot will automatically restart if it crashes (configured with `restart: always`).

## Commands

### User Commands

- **Verify Button**: Click the "Verify" button in the verification message to start the verification process. You'll be prompted to enter your phone number.

### Admin Commands

- **`/send_verify_msg [channel]`**: Sends the verification message embed with a verify button to the specified channel. Requires administrator permissions.

- **`/get_names`**: Exports all guild member names (extracted from nicknames) to a text file. Owner-only command.

- **`/ping`**: Returns the bot's latency.

## How Verification Works

1. User clicks the "Verify" button in the verification message
2. A modal appears prompting for their phone number
3. The bot extracts digits from the phone number and checks it against the attendee data
4. If the phone number matches:
   - The user's school is retrieved from the attendee data
   - OpenAI reformats the school name to match the standardized list
   - The user's nickname is updated to "First Last | School"
   - Verified and Hacker roles are assigned
   - Unverified role is removed
   - A success message is sent
   - The verification is logged to the log channel
5. If the phone number doesn't match, an error message is sent and the failed attempt is logged

## Project Structure

```
NexHacksBot/
├── components/
│   ├── __init__.py
│   ├── verify_modal.py      # Verification modal component
│   └── verify_msg_view.py   # Verification button view component
├── scripts/
│   └── deploy.sh            # Deployment script
├── attendees.csv            # Attendee registration data
├── schools.json             # Valid school names list
├── config.py                # Configuration management
├── main.py                  # Main bot file
├── requirements.txt         # Python dependencies
├── Dockerfile               # Docker image configuration
├── compose.yml              # Docker Compose configuration
└── README.md               # This file
```

## Dependencies

- `py-cord`: Discord API wrapper
- `openai`: OpenAI API client for school name normalization
- `python-dotenv`: Environment variable management
- `audioop-lts`: Audio operations (dependency of py-cord)

## Security Notes

- The bot runs as a non-root user in Docker for security
- Environment variables are loaded from `.env` file (make sure not to commit this file)
- Phone numbers are stored and compared as digits-only for consistency
- Verification attempts are logged for audit purposes

## License

This project was created specifically for the NexHacks @ CMU hackathon.

## Contributing

This bot was created for a specific event. If you're adapting it for your own use, make sure to:

1. Update the school list in `schools.json`
2. Adjust role IDs and channel IDs in your `.env` file
3. Modify the owner ID check in `get_names` command if needed
4. Customize the verification message embed as desired
