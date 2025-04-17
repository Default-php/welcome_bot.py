# OmniBot 🤖

OmniBot is a versatile Discord bot developed in Python using `discord.py`. It enhances server engagement with personalized welcome messages, an XP & leveling system, interactive text commands, and Reddit integration for sharing memes.

## 🚀 Features

- Personalized welcome messages on member join
- XP and leveling system to reward user activity
- Interactive commands: `$hello`, `$test`, `$info`, `$level`, `$meme`
- Reddit API integration via PRAW to fetch and post random memes
- Easy configuration and scalable for future enhancements

## 🛠️ Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/your_username/OmniBot.git
   ```
2. Change into the project directory:
   ```bash
   cd OmniBot
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Create a `.env` file in the root directory with the following entries:
   ```env
   DISCORD_TOKEN=your_discord_bot_token
   REDDIT_CLIENT_ID=your_reddit_client_id
   REDDIT_CLIENT_SECRET=your_reddit_client_secret
   REDDIT_USER_AGENT=your_reddit_user_agent
   ```
5. Run the bot:
   ```bash
   python OmniBot.py
   ```

## 🔧 Configuration

- **Discord**: Create a bot under the [Discord Developer Portal](https://discord.com/developers/applications), enable **Server Members** and **Message Content** intents, then invite it to your server with required permissions.
- **Reddit**: Register a script application at [Reddit Apps](https://www.reddit.com/prefs/apps) to obtain `client_id`, `client_secret`, and set a `user_agent`.

## 📌 Future Improvements

- Additional interactive commands and moderation tools
- Database support for persistent user data
- Role rewards tied to user levels

---

Contributions and suggestions are welcome! 🚀



