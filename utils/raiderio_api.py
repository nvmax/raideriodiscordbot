"""
Utility functions for interacting with the Raider.io API.
"""

import aiohttp
import logging
import os
from dotenv import load_dotenv
from config import RAIDERIO_API_URL, DEFAULT_REGIONS

# Load environment variables
load_dotenv()
RAIDERIO_API_KEY = os.getenv('RAIDERIO_API_KEY')

logger = logging.getLogger(__name__)

async def get_character_profile(character_name, realm, region="us", fields=None):
    """
    Get character profile information from Raider.io API.

    Args:
        character_name (str): The name of the character.
        realm (str): The realm/server the character is on.
        region (str, optional): The region (us, eu, etc.). Defaults to "us".
        fields (list, optional): Additional fields to include in the response.
                                Default fields are gear, guild, covenant, and raid_progression.

    Returns:
        dict: Character profile data or None if an error occurred.
    """
    # Use the simplest possible approach that we know works
    base_url = f"{RAIDERIO_API_URL}/characters/profile?region={region}&realm={realm}&name={character_name}"

    # Add fields if specified
    if fields:
        fields_str = ",".join(fields) if isinstance(fields, list) else fields
        base_url += f"&fields={fields_str}"
    else:
        # Default fields
        base_url += "&fields=gear,guild,raid_progression,mythic_plus_scores_by_season:current,mythic_plus_best_runs,mythic_plus_ranks"

    # Don't use the API key as it seems to be causing issues
    # if RAIDERIO_API_KEY:
    #     base_url += f"&api_key={RAIDERIO_API_KEY}"

    logger.info(f"Making request to: {base_url}")

    headers = {
        'Accept': 'application/json',
        'User-Agent': 'RaiderBot Discord Bot'
    }

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(base_url, headers=headers) as response:
                if response.status == 200:
                    data = await response.json()
                    logger.info(f"Success! Character found: {data['name']} on {data['realm']}")
                    return data
                else:
                    # Character not found or invalid parameters
                    logger.warning(f"Character not found: {character_name}-{realm} ({region})")
                    response_text = await response.text()
                    logger.debug(f"API Response: {response_text}")
                    return None
    except Exception as e:
        logger.error(f"Exception while fetching character data: {e}")
        return None

async def find_character_in_regions(character_name, realm, regions=None):
    """
    Try to find a character in multiple regions.

    Args:
        character_name (str): The name of the character.
        realm (str): The realm/server the character is on.
        regions (list, optional): List of regions to try. Defaults to DEFAULT_REGIONS.

    Returns:
        dict: Character profile data or None if not found in any region.
    """
    if regions is None:
        regions = DEFAULT_REGIONS

    for region in regions:
        logger.info(f"Trying to find {character_name} on {realm} in {region.upper()} region")
        character_data = await get_character_profile(character_name, realm, region)

        if character_data:
            logger.info(f"Character found in {region.upper()} region")
            return character_data

    logger.warning(f"Character {character_name} not found on {realm} in any region")
    return None
