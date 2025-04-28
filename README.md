# Raider.io Discord Bot

A Discord bot that provides information about World of Warcraft characters from Raider.io. This repository includes both JavaScript (Discord.js) and Python (Discord.py) implementations.

## Features

- `/raider` command for character lookup
- Displays character information including:
  - Basic character info (class, race, spec, faction)
  - Item level
  - Guild
  - Mythic+ score
  - Current spec realm ranking for Mythic+ (e.g., Protection Paladin)
  - Top 3 best Mythic+ runs with links to Raider.io
  - Dungeon-specific emojis next to each run
  - Dungeon runs displayed in a single embed with numbered entries and local images
  - Class icon displayed as the author icon
  - Latest raid progression
  - Total raid progression across all raids
  - Achievement points
  - Last updated timestamp

## Setup

### Common Steps (Both Versions)

1. Clone this repository
2. Create a Discord application and bot at [Discord Developer Portal](https://discord.com/developers/applications)
3. In the Bot section:
   - Under "Privileged Gateway Intents", enable the "Server Members Intent" and "Message Content Intent"
4. Copy your bot token and application ID
5. Create a `.env` file in the root directory and add your bot token and client ID:
   ```
   DISCORD_TOKEN=your_bot_token_here
   CLIENT_ID=your_application_id_here
   RAIDERIO_API_KEY=your_raiderio_api_key_here
   ```
6. Invite the bot to your server using the OAuth2 URL Generator in the Discord Developer Portal
   - Select the `bot` and `applications.commands` scopes
   - Select the `Send Messages`, `Use Slash Commands`, and `Use External Emojis` permissions

### JavaScript (Discord.js) Setup

1. Install Node.js dependencies:
   ```
   npm install
   ```
2. Register the slash commands:
   ```
   node deploy-commands.js
   ```
3. Run the bot:
   ```
   npm start
   ```

### Python (Discord.py) Setup

1. Create a virtual environment (recommended):
   ```
   python -m venv venv
   ```
2. Activate the virtual environment:
   - Windows: `venv\Scripts\activate`
   - macOS/Linux: `source venv/bin/activate`
3. Install Python dependencies:
   ```
   pip install -r requirements.txt
   ```
4. Run the bot:
   ```
   python bot.py
   ```

## Usage

1. Type `/raider` in any channel where the bot has access
2. Enter the character name and server in the format `CharacterName-ServerName`
3. The bot will display the character information in an embed with separate embeds for dungeon icons
4. If the character is not found in the US region, the bot will automatically try EU, KR, and TW regions

## Configuration

### Environment Variables
Both versions use environment variables for basic configuration:
- `DISCORD_TOKEN`: Your Discord bot token
- `CLIENT_ID`: Your Discord application ID
- `RAIDERIO_API_KEY`: Your Raider.io API key

### Custom Emojis
Both versions support custom Discord emojis for dungeon icons and faction icons:

1. Upload dungeon and faction icons to your Discord server as custom emojis
2. Get the emoji IDs (right-click on the emoji and select "Copy ID")
3. Update the code with your custom emoji IDs

#### Using Custom Faction Emojis

To use custom faction emojis, you need to modify the code directly:

All emoji IDs are now configured in the `.env` file for easy management:

#### Upload Icons from /images folder to your Discord server as custom emojis
#### Right-click on the emoji and select "Copy ID"
#### Replace the id with the one you recieve 

```
# Faction Emoji IDs
HORDE_EMOJI_ID=1366508841042444368
ALLIANCE_EMOJI_ID=1366508892741308638

# Dungeon Emoji IDs
MECHAGON_EMOJI_ID=1366478770353078344
CINDERBREW_EMOJI_ID=1366478766469156945
DARKFLAME_EMOJI_ID=1366478767400161391
FLOODGATE_EMOJI_ID=1366478768880746527
MOTHERLODE_EMOJI_ID=1366478771359715508
PRIORY_EMOJI_ID=1366478772295041041
ROOKERY_EMOJI_ID=1366478773934886912
THEATER_EMOJI_ID=1366478775184916480
```

Both versions load these values from the environment:

1. The JavaScript version loads them in `config.js`:
   ```javascript
   // Get emoji IDs from environment variables
   const HORDE_EMOJI_ID = process.env.HORDE_EMOJI_ID || '1366508841042444368';
   const ALLIANCE_EMOJI_ID = process.env.ALLIANCE_EMOJI_ID || '1366508892741308638';
   // ... other emoji IDs ...

   module.exports = {
     dungeonEmojis: {
       'Cinderbrew Meadery': `<:cinderbrew:${CINDERBREW_EMOJI_ID}>`,
       // ... other dungeon emojis ...
     },
     factionEmojis: {
       'horde': `<:horde:${HORDE_EMOJI_ID}>`,
       'alliance': `<:alliance:${ALLIANCE_EMOJI_ID}>`,
     },
     // ... other config options ...
   };
   ```

2. The Python version loads them in `config.py`:
   ```python
   # Get emoji IDs from environment variables
   HORDE_EMOJI_ID = os.getenv("HORDE_EMOJI_ID", "1366508841042444368")
   ALLIANCE_EMOJI_ID = os.getenv("ALLIANCE_EMOJI_ID", "1366508892741308638")
   # ... other emoji IDs ...

   # Faction emojis
   FACTION_EMOJIS = {
       'horde': f'<:horde:{HORDE_EMOJI_ID}>',
       'alliance': f'<:alliance:{ALLIANCE_EMOJI_ID}>',
   }
   ```

If you need to use different emoji IDs, simply update them in your `.env` file.

#### Dungeon Emojis Configuration
Update the configuration files with your custom dungeon emoji IDs:

##### JavaScript Configuration (config.js)
```javascript
dungeonEmojis: {
  'Darkflame Cleft': '<:darkflame:1366478767400161391>',
  'The Rookery': '<:rookery:1366478773934886912>',
  'Operation: Floodgate': '<:floodgate:1366478768880746527>',
  'Mechagon Workshop': '<:mechagon:1366478770353078344>',
  'The MOTHERLODE!!': '<:motherload:1366478771359715508>',
  'Priory of the Sacred Flame': '<:priory:1366478772295041041>',
  'Cinderbrew Meadery': '<:cinderbrew:1366478766469156945>',
  'Theater of Pain': '<:theaterofpain:1366478775184916480>',
  // etc.
},
```

##### Python Configuration (config.py)
```python
DUNGEON_EMOJIS = {
    'Darkflame Cleft': '<:darkflame:1366478767400161391>',
    'The Rookery': '<:rookery:1366478773934886912>',
    'Operation: Floodgate': '<:floodgate:1366478768880746527>',
    'Mechagon Workshop': '<:mechagon:1366478770353078344>',
    'The MOTHERLODE!!': '<:motherload:1366478771359715508>',
    'Priory of the Sacred Flame': '<:priory:1366478772295041041>',
    'Cinderbrew Meadery': '<:cinderbrew:1366478766469156945>',
    'Theater of Pain': '<:theaterofpain:1366478775184916480>',
    # etc.
}
```

### Fallback Emojis
If custom Discord emojis aren't available, both versions will use standard Unicode emojis as a fallback.

### Other Configuration Options

#### JavaScript (config.js)
```javascript
module.exports = {
  showAffixes: false,  // Set to true to show affixes for each dungeon run
  maxMythicPlusRuns: 3,  // Number of M+ runs to display
  defaultRegions: ['us', 'eu', 'kr', 'tw'],  // Regions to search for characters
  // other options...
};
```

#### Python (config.py)
```python
# Show affixes for each dungeon run
SHOW_AFFIXES = False

# Number of M+ runs to display
MAX_MYTHIC_PLUS_RUNS = 3

# Regions to search for characters
DEFAULT_REGIONS = ['us', 'eu', 'kr', 'tw']
```

## Troubleshooting

If you encounter any issues:

1. Make sure your Discord bot token and client ID are correct in the `.env` file
2. Check that the bot has the necessary permissions in your Discord server
3. Check the console for any error messages

### JavaScript-Specific Troubleshooting
1. Verify that the slash commands are registered by running `node deploy-commands.js`
2. Make sure all Node.js dependencies are installed with `npm install`

### Python-Specific Troubleshooting
1. Make sure all Python dependencies are installed with `pip install -r requirements.txt`
2. Ensure you're using Python 3.8 or higher
3. If using a virtual environment, make sure it's activated

### Common Errors

- **PrivilegedIntentsRequired**: If you see this error, it means you've enabled an intent in the code that isn't enabled in the Discord Developer Portal. Go to the [Discord Developer Portal](https://discord.com/developers/applications), select your application, go to the Bot section, and enable the required intents.

- **Character not found**: Make sure you're using the correct format (`CharacterName-ServerName`) and that the character exists on the specified server. The bot will try US, EU, KR, and TW regions by default.

- **Invalid token**: Make sure your Discord bot token is correct in the `.env` file.

- **API Issues**: If the Raider.io API is not responding or returning errors, try again later as there might be rate limiting or temporary service issues.

### Switching Between Versions
You can run either the JavaScript or Python version of the bot, but not both simultaneously with the same token. If you want to switch:

1. Stop the currently running bot
2. Start the other version using the appropriate command:
   - JavaScript: `npm start`
   - Python: `python bot.py`

## License

MIT
