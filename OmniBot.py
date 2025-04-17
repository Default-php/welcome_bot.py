import discord
from discord.ext import commands
import praw
import random
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

reddit = praw.Reddit(
    client_id = os.getenv("REDDIT_CLIENT_ID"),
    client_secret = os.getenv("REDDIT_CLIENT_SECRET"),
    user_agent = os.getenv("REDDIT_USER_AGENT")
)
    
def get_random_post(subreddit_name):
    subreddit = reddit.subreddit(subreddit_name)
    posts = list(subreddit.hot(limit=50))
    filtered = filter(lambda p: not p.stickied and not p.over18, posts)
    return random.choice(list(filtered))

# Verify that the token was loaded correctly
if not TOKEN:
    raise ValueError("The token was not found in the .env file")

# Configure necessary intents
intents = discord.Intents.default()
intents.members = True  # Required to detect new members
intents.message_content = True  # Allows the bot to read message content

# Create bot instance
bot = commands.Bot(command_prefix="$", intents=intents)

# Dictionary to store user XP and level data
# Uses user ID (converted to string) as the key
user_data = {}

# Constants for XP system
XP_MIN = 5            # Minimum XP granted per message
XP_MAX = 15           # Maximum XP granted per message
XP_THRESHOLD = 100    # XP required per level (adjustable scale)


# Reddit API connection check
def reddit_connection_check():
    try:
        reddit.subreddit("MemesESP").title 
        print("✅ Successfully connected to the Reddit API.")
    except Exception as e:
        print("❌ Failed to connect to Reddit API:", e)

reddit_connection_check()

# Event triggered when the bot is ready
@bot.event
async def on_ready():
    print(f'✅ Bot is online as {bot.user}')
    print("✅ Commands loaded successfully.")

# Event triggered when a new user joins the server
@bot.event
async def on_member_join(member):
    # Set up the welcome channel
    channel_id = 1343767017043525666    # Here you have to put the id of the channel where you want to send the welcome message
    channel = bot.get_channel(channel_id)

    if channel:
        await channel.send(f'🎉 Welcome {member.mention} to {member.guild.name}! Enjoy your stay! 🚀')

# Simple greeting command
@bot.command()
async def hello(ctx):
    await ctx.send("Hello! What do you need?")
    
# Test command to check if the bot is running
@bot.command()
async def test(ctx):
    await ctx.send("OmniBot is working correctly.")

# Fetches a meme from Reddit using the PRAW API and sends it to the channel
@bot.command()
async def meme(ctx):
    post = get_random_post("MemesESP")
    await ctx.send(f"**{post.title}**\n{post.url}")

# Command to display bot information
@bot.command()
async def info(ctx):
    embed = discord.Embed(
        title="🤖 OmniBot - Information",
        description="OmniBot is designed to enhance the Discord server experience by providing automatic welcome messages and interactive features.",
        color=discord.Color.blue()
    )

    embed.add_field(
        name="📌 Current Features",
        value="- Personalized welcome messages.\n"
              "- Interactive commands like `$hello`, `$info`, `$level`, $meme and `$test`.\n"
              "- XP and Leveling system.",
        inline=False
    )

    embed.add_field(
        name="🚀 Future Improvements",
        value="- More interactive commands.\n"
              "- Advanced moderation features.\n"
              "- Custom ranking roles based on levels.",
        inline=False
    )

    embed.add_field(
        name="👨‍💻 Developer",
        value="Alfonso González\n"
              "Systems Engineering Student\n"
              "Passionate about Data Science.",
        inline=False
    )

    embed.set_footer(text="Thank you for using OmniBot! 🚀")
    await ctx.send(embed=embed)
    
# Event to process messages for XP and leveling system
@bot.event
async def on_message(message):
    # Ignore messages from other bots 
    if message.author.bot:
        return

    user_id = str(message.author.id)
    # Assign a random XP amount within the defined range
    xp_gain = random.randint(XP_MIN, XP_MAX)
    
    # Initialize user data if not already stored
    if user_id not in user_data:
        user_data[user_id] = {"xp": 0, "level": 1}
    
    # Add earned XP to the user's total
    user_data[user_id]["xp"] += xp_gain

    # Calculate XP needed for next level (current level * XP_THRESHOLD)
    current_level = user_data[user_id]["level"]
    xp_needed = current_level * XP_THRESHOLD

    # Check if user has reached the required XP to level up
    if user_data[user_id]["xp"] >= xp_needed:
        user_data[user_id]["level"] += 1
        await message.channel.send(
            f"🎉 {message.author.mention} has leveled up to level {user_data[user_id]['level']}!"
        )
    
    # Process other commands the bot might have
    await bot.process_commands(message)

# Command to check a user's level and XP
@bot.command()
async def level(ctx, member: discord.Member = None):
    if member is None:
        member = ctx.author  # Default to the user who issued the command
    user_id = str(member.id)
    if user_id in user_data:
        level_num = user_data[user_id]["level"]
        xp_total = user_data[user_id]["xp"]
        await ctx.send(f"{member.mention} is at level {level_num} with {xp_total} XP.")
    else:
        await ctx.send(f"{member.mention} has not earned any XP yet.")

# Start the bot
bot.run(TOKEN)
