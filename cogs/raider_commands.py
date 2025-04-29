"""
Cog for handling Raider.io related commands.
"""

import discord
from discord import app_commands
from discord.ext import commands
from discord.ui import Modal, TextInput
import logging
import dateutil.parser

from utils.raiderio_api import find_character_in_regions
from config import DEFAULT_REGIONS, DUNGEON_EMOJIS, FALLBACK_EMOJIS, FACTION_EMOJIS, MAX_MYTHIC_PLUS_RUNS, SHOW_AFFIXES

logger = logging.getLogger(__name__)

def get_class_color(class_name):
    """Get the color for a class."""
    class_colors = {
        'Warrior': 0xC79C6E,
        'Paladin': 0xF58CBA,
        'Hunter': 0xABD473,
        'Rogue': 0xFFF569,
        'Priest': 0xFFFFFF,
        'Death Knight': 0xC41F3B,
        'Shaman': 0x0070DE,
        'Mage': 0x69CCF0,
        'Warlock': 0x9482C9,
        'Monk': 0x00FF96,
        'Druid': 0xFF7D0A,
        'Demon Hunter': 0xA330C9,
        'Evoker': 0x33937F
    }
    return class_colors.get(class_name, 0x0099ff)

# This function is no longer needed as we're using the FACTION_EMOJIS dictionary from config.py

class CharacterLookupModal(Modal):
    """Modal for looking up a character on Raider.io."""

    def __init__(self):
        super().__init__(title="Character Lookup")

        # Add text input for character name and server
        self.character_input = TextInput(
            label="Character Name-Server",
            placeholder="Example: CharacterName-ServerName",
            required=True,
            min_length=3,
            max_length=40
        )
        self.add_item(self.character_input)

    async def on_submit(self, interaction: discord.Interaction):
        # Defer the response while we fetch the data
        await interaction.response.defer(ephemeral=False)

        # Parse the input to get character name and server
        input_value = self.character_input.value.strip()

        # Check if the input contains a hyphen
        if '-' not in input_value:
            await interaction.followup.send(
                "Invalid format. Please use the format: `CharacterName-ServerName`",
                ephemeral=True
            )
            return

        # Split the input by the first hyphen
        parts = input_value.split('-', 1)
        character_name = parts[0].strip()
        realm = parts[1].strip().lower()  # Keep it lowercase but don't replace spaces with hyphens

        # Try to find the character in all regions
        character_data = await find_character_in_regions(character_name, realm)

        if character_data:
            # Create the main embed
            main_embed = discord.Embed(
                title=f"{character_data['name']} - {character_data['realm']} ({character_data['region'].upper()})",
                url=character_data['profile_url'],
                color=get_class_color(character_data['class'])
            )

            # Add class icon as author
            class_name = character_data['class'].lower()
            # Format class name for URL - replace spaces with empty string and remove special characters
            formatted_class_name = class_name.replace(' ', '').replace("'", "").replace("-", "")
            logger.info(f"Using class name for icon URL: {formatted_class_name}")
            class_icon_url = f"https://wow.zamimg.com/images/wow/icons/large/classicon_{formatted_class_name}.jpg"

            # Set author with name only first, then try to add icon_url
            main_embed.set_author(
                name=f"{character_data['active_spec_name']} {character_data['class']}"
            )

            # Try to set icon_url separately with error handling
            try:
                main_embed.set_author(
                    name=f"{character_data['active_spec_name']} {character_data['class']}",
                    icon_url=class_icon_url
                )
                logger.info(f"Successfully set class icon URL: {class_icon_url}")
            except Exception as e:
                logger.error(f"Failed to set class icon URL: {e}")
                # Continue without the icon

            # Add character thumbnail
            if 'thumbnail_url' in character_data:
                try:
                    main_embed.set_thumbnail(url=character_data['thumbnail_url'])
                    logger.info(f"Successfully set thumbnail URL: {character_data['thumbnail_url']}")
                except Exception as e:
                    logger.error(f"Failed to set thumbnail URL: {e}")
                    # Continue without the thumbnail

            # Add basic character info
            main_embed.add_field(name="Class", value=character_data['class'], inline=True)
            main_embed.add_field(name="Race", value=character_data['race'], inline=True)
            main_embed.add_field(name="Spec", value=character_data['active_spec_name'], inline=True)

            # Add faction if available
            if 'faction' in character_data:
                faction = character_data['faction'].lower()
                # Use the FACTION_EMOJIS dictionary from config.py
                faction_emoji = FACTION_EMOJIS.get(faction)

                # Fallback to standard emoji if custom emoji not available
                if not faction_emoji:
                    faction_emoji = FALLBACK_EMOJIS.get(faction, "🔴" if faction == "horde" else "🔵")

                main_embed.add_field(
                    name="Faction",
                    value=f"{faction_emoji} {character_data['faction'].capitalize()}",
                    inline=True
                )

            # Add item level if available
            if 'gear' in character_data and 'item_level_equipped' in character_data['gear']:
                main_embed.add_field(
                    name="Item Level",
                    value=str(character_data['gear']['item_level_equipped']),
                    inline=True
                )

            # Add guild if available
            if 'guild' in character_data and character_data['guild']:
                guild_text = character_data['guild']['name']
                if 'realm' in character_data['guild'] and character_data['guild']['realm'] != character_data['realm']:
                    guild_text += f" ({character_data['guild']['realm']})"
                main_embed.add_field(
                    name="Guild",
                    value=guild_text,
                    inline=True
                )

            # Add Mythic+ score if available
            if 'mythic_plus_scores_by_season' in character_data and character_data['mythic_plus_scores_by_season']:
                current_season = character_data['mythic_plus_scores_by_season'][0]
                score = current_season['scores']['all']
                main_embed.add_field(
                    name=f"M+ Score ({current_season['season']})",
                    value=f"[{score}]({character_data['profile_url']})",
                    inline=True
                )

            # Add Mythic+ ranks if available
            if 'mythic_plus_ranks' in character_data:
                ranks = character_data['mythic_plus_ranks']
                role = character_data['active_spec_role'].lower() if 'active_spec_role' in character_data else None
                class_name = character_data['class']
                spec_name = character_data['active_spec_name']
                realm_name = character_data['realm']

                # Only show the class-role specific rank (e.g., Protection Paladin)
                class_role_key = f"class_{role}"
                if role and class_role_key in ranks:
                    rank_value = ranks[class_role_key]['realm']
                    main_embed.add_field(
                        name=f"{spec_name} {class_name} Realm Rank",
                        value=f"#{rank_value:,} on {realm_name}",
                        inline=True
                    )

            # Add best Mythic+ runs
            if 'mythic_plus_best_runs' in character_data and character_data['mythic_plus_best_runs']:
                # Get the top runs based on config
                max_runs = MAX_MYTHIC_PLUS_RUNS
                top_runs = sorted(character_data['mythic_plus_best_runs'], key=lambda x: x['score'], reverse=True)[:max_runs]

                # Create a field for the best M+ runs
                runs_text = ""

                # Add each run to the text with numbering
                for index, run in enumerate(top_runs):
                    # Convert dungeon name to title case
                    dungeon_name = ' '.join(word.capitalize() for word in run['dungeon'].replace('-', ' ').split())
                    level = run['mythic_level']

                    # Map dungeon names to appropriate emojis
                    dungeon_emoji = "🏰"  # Default castle emoji

                    # Try to get the custom Discord emoji first
                    custom_emoji = DUNGEON_EMOJIS.get(dungeon_name)

                    # Fallback to partial matching if exact match not found
                    if not custom_emoji:
                        if "Cinderbrew" in dungeon_name:
                            custom_emoji = DUNGEON_EMOJIS.get('Cinderbrew Meadery')
                        elif "Darkflame" in dungeon_name:
                            custom_emoji = DUNGEON_EMOJIS.get('Darkflame Cleft')
                        elif "Floodgate" in dungeon_name:
                            custom_emoji = DUNGEON_EMOJIS.get('Operation: Floodgate')
                        elif "Mechagon" in dungeon_name:
                            custom_emoji = DUNGEON_EMOJIS.get('Mechagon Workshop')
                        elif "MOTHERLODE" in dungeon_name:
                            custom_emoji = DUNGEON_EMOJIS.get('The MOTHERLODE!!')
                        elif "Priory" in dungeon_name:
                            custom_emoji = DUNGEON_EMOJIS.get('Priory of the Sacred Flame')
                        elif "Rookery" in dungeon_name:
                            custom_emoji = DUNGEON_EMOJIS.get('The Rookery')
                        elif "Theater" in dungeon_name or "Pain" in dungeon_name:
                            custom_emoji = DUNGEON_EMOJIS.get('Theater of Pain')

                    # If we have a custom emoji, use it, otherwise fall back to standard emoji
                    if custom_emoji:
                        dungeon_emoji = custom_emoji
                    else:
                        # Use fallback emoji
                        fallback_emoji = FALLBACK_EMOJIS.get(dungeon_name, "🏰")

                        # Try partial matching for fallback emoji
                        if fallback_emoji == "🏰":
                            if "Cinderbrew" in dungeon_name:
                                fallback_emoji = FALLBACK_EMOJIS.get('Cinderbrew Meadery')
                            elif "Darkflame" in dungeon_name:
                                fallback_emoji = FALLBACK_EMOJIS.get('Darkflame Cleft')
                            elif "Floodgate" in dungeon_name:
                                fallback_emoji = FALLBACK_EMOJIS.get('Operation: Floodgate')
                            elif "Mechagon" in dungeon_name:
                                fallback_emoji = FALLBACK_EMOJIS.get('Mechagon Workshop')
                            elif "MOTHERLODE" in dungeon_name:
                                fallback_emoji = FALLBACK_EMOJIS.get('The MOTHERLODE!!')
                            elif "Priory" in dungeon_name:
                                fallback_emoji = FALLBACK_EMOJIS.get('Priory of the Sacred Flame')
                            elif "Rookery" in dungeon_name:
                                fallback_emoji = FALLBACK_EMOJIS.get('The Rookery')
                            elif "Theater" in dungeon_name or "Pain" in dungeon_name:
                                fallback_emoji = FALLBACK_EMOJIS.get('Theater of Pain')

                        dungeon_emoji = fallback_emoji

                    # Add run number
                    runs_text += f"**#{index + 1}**\n"

                    # Add the emoji to the text
                    runs_text += f"{dungeon_emoji} "
                    logger.info(f"Using emoji for {dungeon_name}: {dungeon_emoji}")

                    # Add run info
                    if 'url' in run:
                        runs_text += f"**+{level}** [{dungeon_name}]({run['url']})"
                    else:
                        runs_text += f"**+{level}** {dungeon_name}"

                    # Add score if available
                    if 'score' in run:
                        runs_text += f"\nScore: {run['score']:.1f}"

                    # Add affixes if available and enabled in config
                    if SHOW_AFFIXES and 'affixes' in run and run['affixes']:
                        affix_names = ", ".join([affix['name'] for affix in run['affixes']])
                        runs_text += f"\nAffixes: {affix_names}"

                    # Add spacing between runs
                    runs_text += "\n\n"

                # Add the field to the main embed
                main_embed.add_field(
                    name="Best M+ Runs",
                    value=runs_text,
                    inline=False
                )

            # Add raid progression if available
            if 'raid_progression' in character_data:
                raid_prog = character_data['raid_progression']

                # Get the latest raid (first in the list)
                if raid_prog and len(raid_prog) > 0:
                    latest_raid_name = next(iter(raid_prog))
                    latest_raid = raid_prog[latest_raid_name]

                    if 'summary' in latest_raid and latest_raid['summary']:  # Only show if there's actual progress
                        main_embed.add_field(
                            name=f"Raid Progress ({latest_raid_name.replace('-', ' ').title()})",
                            value=latest_raid['summary'],
                            inline=False
                        )

                    # Add a field for total raid progress
                    total_normal = sum(raid['normal_bosses_killed'] for raid in raid_prog.values())
                    total_heroic = sum(raid['heroic_bosses_killed'] for raid in raid_prog.values())
                    total_mythic = sum(raid['mythic_bosses_killed'] for raid in raid_prog.values())

                    main_embed.add_field(
                        name="Total Raid Progress",
                        value=f"Normal: {total_normal} | Heroic: {total_heroic} | Mythic: {total_mythic}",
                        inline=False
                    )

            # Add achievement points if available
            if 'achievement_points' in character_data:
                main_embed.add_field(
                    name="Achievement Points",
                    value=f"{character_data['achievement_points']:,}",
                    inline=True
                )

            # Add last updated info
            footer_text = "Data provided by Raider.io"
            if 'last_crawled_at' in character_data:
                try:
                    last_updated = dateutil.parser.parse(character_data['last_crawled_at'])
                    footer_text = f"Data provided by Raider.io • Last updated: {last_updated.strftime('%Y-%m-%d %H:%M')} UTC"
                except Exception as e:
                    logger.error(f"Failed to parse last_crawled_at date: {e}")

            # Set footer with text only first
            main_embed.set_footer(text=footer_text)

            # Try to add icon_url separately with error handling
            try:
                main_embed.set_footer(
                    text=footer_text,
                    icon_url="https://cdnassets.raider.io/images/brand/Icon_Light_32.png"
                )
                logger.info("Successfully set footer icon URL")
            except Exception as e:
                logger.error(f"Failed to set footer icon URL: {e}")
                # Continue without the icon

            # Send the main embed
            await interaction.followup.send(embeds=[main_embed])
        else:
            regions_tried = ", ".join([r.upper() for r in DEFAULT_REGIONS])
            await interaction.followup.send(
                f"Character **{character_name}** not found on **{realm.replace('-', ' ').title()}** in {regions_tried} regions.",
                ephemeral=True
            )

# We no longer need the server selection classes since we're parsing the input directly

# This function is no longer needed as we've integrated its functionality directly into the on_submit method

class RaiderCommands(commands.Cog):
    """Commands for interacting with Raider.io."""

    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="raider", description="Look up a character on Raider.io")
    async def raider(self, interaction: discord.Interaction):
        """Command to look up a character on Raider.io."""

        # Create and show the modal
        modal = CharacterLookupModal()
        await interaction.response.send_modal(modal)

async def setup(bot):
    """Add the cog to the bot."""
    await bot.add_cog(RaiderCommands(bot))
