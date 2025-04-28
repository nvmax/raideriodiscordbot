"""
Main entry point for the Discord bot.
"""

import os
import logging
import asyncio
import discord
from discord.ext import commands
from dotenv import load_dotenv

from config import BOT_DESCRIPTION, COMMAND_PREFIX

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

# Define intents
intents = discord.Intents.default()
# The message_content intent is privileged and requires enabling in the developer portal
# For this bot, we don't actually need it since we're using slash commands
# If you want to use it, enable it in the Discord Developer Portal
# intents.message_content = True

# Create bot instance
bot = commands.Bot(
    command_prefix=COMMAND_PREFIX,
    description=BOT_DESCRIPTION,
    intents=intents
)

@bot.event
async def on_ready():
    """Event triggered when the bot is ready."""
    logger.info(f'{bot.user.name} has connected to Discord!')

    # Sync application commands
    try:
        synced = await bot.tree.sync()
        logger.info(f"Synced {len(synced)} command(s)")
    except Exception as e:
        logger.error(f"Failed to sync commands: {e}")

async def load_extensions():
    """Load all cogs."""
    for filename in os.listdir('./cogs'):
        if filename.endswith('.py'):
            try:
                await bot.load_extension(f'cogs.{filename[:-3]}')
                logger.info(f'Loaded extension: {filename[:-3]}')
            except Exception as e:
                logger.error(f'Failed to load extension {filename[:-3]}: {e}')

async def main():
    """Main function to start the bot."""
    async with bot:
        await load_extensions()
        await bot.start(TOKEN)

if __name__ == '__main__':
    asyncio.run(main())
