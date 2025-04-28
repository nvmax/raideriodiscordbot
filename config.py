"""
Configuration file for the Discord bot.
"""

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Raider.io API base URL
RAIDERIO_API_URL = "https://raider.io/api/v1"
RAIDERIO_API_KEY = os.getenv("RAIDERIO_API_KEY")

# Bot command prefix
COMMAND_PREFIX = "!"

# Bot description
BOT_DESCRIPTION = "A Discord bot that provides information about World of Warcraft characters from Raider.io"

# Default regions to try in order
DEFAULT_REGIONS = ["us", "eu", "kr", "tw"]

# Get emoji IDs from environment variables
HORDE_EMOJI_ID = os.getenv("HORDE_EMOJI_ID", "1366508841042444368")
ALLIANCE_EMOJI_ID = os.getenv("ALLIANCE_EMOJI_ID", "1366508892741308638")
MECHAGON_EMOJI_ID = os.getenv("MECHAGON_EMOJI_ID", "1366478770353078344")
CINDERBREW_EMOJI_ID = os.getenv("CINDERBREW_EMOJI_ID", "1366478766469156945")
DARKFLAME_EMOJI_ID = os.getenv("DARKFLAME_EMOJI_ID", "1366478767400161391")
FLOODGATE_EMOJI_ID = os.getenv("FLOODGATE_EMOJI_ID", "1366478768880746527")
MOTHERLODE_EMOJI_ID = os.getenv("MOTHERLODE_EMOJI_ID", "1366478771359715508")
PRIORY_EMOJI_ID = os.getenv("PRIORY_EMOJI_ID", "1366478772295041041")
ROOKERY_EMOJI_ID = os.getenv("ROOKERY_EMOJI_ID", "1366478773934886912")
THEATER_EMOJI_ID = os.getenv("THEATER_EMOJI_ID", "1366478775184916480")

# Custom Discord emojis for dungeons
DUNGEON_EMOJIS = {
    # Current Season dungeons (Season 2) - custom Discord emojis
    'Cinderbrew Meadery': f'<:cinderbrew:{CINDERBREW_EMOJI_ID}>',
    'Darkflame Cleft': f'<:darkflamecleft:{DARKFLAME_EMOJI_ID}>',
    'Operation: Floodgate': f'<:floodgate:{FLOODGATE_EMOJI_ID}>',
    'Mechagon Workshop': f'<:mechagon:{MECHAGON_EMOJI_ID}>',
    'The MOTHERLODE!!': f'<:motherload:{MOTHERLODE_EMOJI_ID}>',
    'Priory of the Sacred Flame': f'<:priory:{PRIORY_EMOJI_ID}>',
    'The Rookery': f'<:rookery:{ROOKERY_EMOJI_ID}>',
    'Theater of Pain': f'<:theaterofpain:{THEATER_EMOJI_ID}>',
}

# Faction emojis
FACTION_EMOJIS = {
    'horde': f'<:horde:{HORDE_EMOJI_ID}>',
    'alliance': f'<:alliance:{ALLIANCE_EMOJI_ID}>',
}

# Fallback emojis if custom emojis aren't available
FALLBACK_EMOJIS = {
    'Cinderbrew Meadery': '🍺',
    'Darkflame Cleft': '🔥',
    'Operation: Floodgate': '💧',
    'Mechagon Workshop': '🤖',
    'The MOTHERLODE!!': '💰',
    'Priory of the Sacred Flame': '📜',
    'The Rookery': '🐦',
    'Theater of Pain': '🎭',
    'horde': '🔴',
    'alliance': '🔵',
}

# Maximum number of M+ runs to display
MAX_MYTHIC_PLUS_RUNS = 3

# Whether to show affixes in dungeon run details
SHOW_AFFIXES = False
