const { SlashCommandBuilder, EmbedBuilder } = require('discord.js');
const { findCharacterInRegions, DEFAULT_REGIONS } = require('../utils/raiderio-api');
const config = require('../config');

module.exports = {
  data: new SlashCommandBuilder()
    .setName('raider')
    .setDescription('Look up a character on Raider.io')
    .addStringOption(option =>
      option.setName('character')
        .setDescription('Character name and realm (e.g., CharacterName-RealmName)')
        .setRequired(true)),

  async execute(interaction) {
    await interaction.deferReply();

    // Get the character input
    const characterInput = interaction.options.getString('character');

    // Parse character name and realm
    const parts = characterInput.split('-');
    if (parts.length < 2) {
      return interaction.followUp('Please provide both character name and realm in the format: CharacterName-RealmName');
    }

    const characterName = parts[0].trim();
    const realm = parts.slice(1).join('-').trim();

    // Try to find the character in different regions
    const characterData = await findCharacterInRegions(characterName, realm, DEFAULT_REGIONS);

    if (!characterData) {
      const regionsTriedText = DEFAULT_REGIONS.map(r => r.toUpperCase()).join(', ');
      return interaction.followUp(`Character **${characterName}** not found on **${realm.replace('-', ' ')}** in ${regionsTriedText} regions.`);
    }

    // Create the main embed
    const mainEmbed = new EmbedBuilder()
      .setTitle(`${characterData.name} - ${characterData.realm} (${characterData.region.toUpperCase()})`)
      .setURL(characterData.profile_url)
      .setColor(getClassColor(characterData.class));

    // Add class icon as author
    const className = characterData.class.toLowerCase();
    const classIconUrl = `https://wow.zamimg.com/images/wow/icons/large/classicon_${className}.jpg`;
    mainEmbed.setAuthor({
      name: `${characterData.active_spec_name} ${characterData.class}`,
      iconURL: classIconUrl
    });

    // Add character thumbnail
    if (characterData.thumbnail_url) {
      mainEmbed.setThumbnail(characterData.thumbnail_url);
    }

    // Add basic character info
    mainEmbed.addFields(
      { name: 'Class', value: characterData.class, inline: true },
      { name: 'Race', value: characterData.race, inline: true },
      { name: 'Spec', value: characterData.active_spec_name, inline: true }
    );

    // Add faction if available
    if (characterData.faction) {
      const faction = characterData.faction.toLowerCase();
      // Use custom Discord emojis for factions
      // For Discord emojis, we need the format <:name:id>
      let factionEmoji;
      // Use the getFactionEmoji function to get the appropriate emoji
      factionEmoji = getFactionEmoji(faction);

      // Fallback to standard emoji if custom emoji not available or if you prefer
      // Uncomment the line below to use standard emojis instead
      // factionEmoji = faction === 'horde' ? '🔴' : '🔵';

      mainEmbed.addFields({
        name: 'Faction',
        value: `${factionEmoji} ${capitalizeFirstLetter(characterData.faction)}`,
        inline: true
      });
    }

    // Add item level if available
    if (characterData.gear && characterData.gear.item_level_equipped) {
      mainEmbed.addFields({
        name: 'Item Level',
        value: characterData.gear.item_level_equipped.toString(),
        inline: true
      });
    }

    // Add guild if available
    if (characterData.guild) {
      let guildText = characterData.guild.name;
      if (characterData.guild.realm && characterData.guild.realm !== characterData.realm) {
        guildText += ` (${characterData.guild.realm})`;
      }
      mainEmbed.addFields({
        name: 'Guild',
        value: guildText,
        inline: true
      });
    }

    // Add Mythic+ score if available
    if (characterData.mythic_plus_scores_by_season && characterData.mythic_plus_scores_by_season.length > 0) {
      const currentSeason = characterData.mythic_plus_scores_by_season[0];
      const score = currentSeason.scores.all;

      mainEmbed.addFields({
        name: `M+ Score (${currentSeason.season})`,
        value: `[${score}](${characterData.profile_url})`,
        inline: true
      });
    }

    // Add Mythic+ ranks if available
    if (characterData.mythic_plus_ranks) {
      const ranks = characterData.mythic_plus_ranks;
      const role = characterData.active_spec_role ? characterData.active_spec_role.toLowerCase() : null;
      const className = characterData.class;
      const specName = characterData.active_spec_name;
      const realmName = characterData.realm;

      // Only show the class-role specific rank (e.g., Protection Paladin)
      const classRoleKey = `class_${role}`;
      if (role && ranks[classRoleKey]) {
        const rankValue = ranks[classRoleKey].realm;
        mainEmbed.addFields({
          name: `${specName} ${className} Realm Rank`,
          value: `#${rankValue.toLocaleString()} on ${realmName}`,
          inline: true
        });
      }
    }

    // Add best Mythic+ runs
    if (characterData.mythic_plus_best_runs && characterData.mythic_plus_best_runs.length > 0) {
      // Get the top runs based on config
      const maxRuns = config.maxMythicPlusRuns || 3;
      const topRuns = characterData.mythic_plus_best_runs
        .sort((a, b) => b.score - a.score)
        .slice(0, maxRuns);

      // Create a field for the best M+ runs
      let runsText = '';

      // Add each run to the text with numbering
      topRuns.forEach((run, index) => {
        const dungeonName = run.dungeon.replace('-', ' ').replace(/\b\w/g, l => l.toUpperCase());
        const level = run.mythic_level;

        // Map dungeon names to appropriate emojis
        let dungeonEmoji = '🏰'; // Default castle emoji

        // Try to get the custom Discord emoji first
        let customEmoji = config.dungeonEmojis[dungeonName];

        // Fallback to partial matching if exact match not found
        if (!customEmoji) {
          if (dungeonName.includes('Cinderbrew')) {
            customEmoji = config.dungeonEmojis['Cinderbrew Meadery'];
          } else if (dungeonName.includes('Darkflame')) {
            customEmoji = config.dungeonEmojis['Darkflame Cleft'];
          } else if (dungeonName.includes('Floodgate')) {
            customEmoji = config.dungeonEmojis['Operation: Floodgate'];
          } else if (dungeonName.includes('Mechagon')) {
            customEmoji = config.dungeonEmojis['Mechagon Workshop'];
          } else if (dungeonName.includes('MOTHERLODE')) {
            customEmoji = config.dungeonEmojis['The MOTHERLODE!!'];
          } else if (dungeonName.includes('Priory')) {
            customEmoji = config.dungeonEmojis['Priory of the Sacred Flame'];
          } else if (dungeonName.includes('Rookery')) {
            customEmoji = config.dungeonEmojis['The Rookery'];
          } else if (dungeonName.includes('Theater') || dungeonName.includes('Pain')) {
            customEmoji = config.dungeonEmojis['Theater of Pain'];
          }
        }

        // If we have a custom emoji, use it, otherwise fall back to standard emoji
        if (customEmoji) {
          dungeonEmoji = customEmoji;
        } else {
          // Use fallback emoji
          dungeonEmoji = config.fallbackEmojis[dungeonName] || '🏰';

          // Try partial matching for fallback emoji
          if (dungeonEmoji === '🏰') {
            if (dungeonName.includes('Cinderbrew')) {
              dungeonEmoji = config.fallbackEmojis['Cinderbrew Meadery'];
            } else if (dungeonName.includes('Darkflame')) {
              dungeonEmoji = config.fallbackEmojis['Darkflame Cleft'];
            } else if (dungeonName.includes('Floodgate')) {
              dungeonEmoji = config.fallbackEmojis['Operation: Floodgate'];
            } else if (dungeonName.includes('Mechagon')) {
              dungeonEmoji = config.fallbackEmojis['Mechagon Workshop'];
            } else if (dungeonName.includes('MOTHERLODE')) {
              dungeonEmoji = config.fallbackEmojis['The MOTHERLODE!!'];
            } else if (dungeonName.includes('Priory')) {
              dungeonEmoji = config.fallbackEmojis['Priory of the Sacred Flame'];
            } else if (dungeonName.includes('Rookery')) {
              dungeonEmoji = config.fallbackEmojis['The Rookery'];
            } else if (dungeonName.includes('Theater') || dungeonName.includes('Pain')) {
              dungeonEmoji = config.fallbackEmojis['Theater of Pain'];
            }
          }
        }

        // Add run number
        runsText += `**#${index + 1}**\n`;

        // Add the emoji to the text
        runsText += `${dungeonEmoji} `;
        console.log(`Using emoji for ${dungeonName}: ${dungeonEmoji}`);

        // Add run info
        if (run.url) {
          runsText += `**+${level}** [${dungeonName}](${run.url})`;
        } else {
          runsText += `**+${level}** ${dungeonName}`;
        }

        // Add score if available
        if (run.score) {
          runsText += `\nScore: ${run.score.toFixed(1)}`;
        }

        // Add affixes if available and enabled in config
        if (config.showAffixes && run.affixes && run.affixes.length > 0) {
          const affixNames = run.affixes.map(affix => affix.name).join(', ');
          runsText += `\nAffixes: ${affixNames}`;
        }

        // Add spacing between runs
        runsText += '\n\n';
      });

      // Add the field to the main embed
      mainEmbed.addFields({
        name: 'Best M+ Runs',
        value: runsText,
        inline: false
      });

      // No attachments needed since we're using custom Discord emojis
    }

    // Add raid progression if available
    if (characterData.raid_progression) {
      const raidProg = characterData.raid_progression;

      // Get the latest raid (first in the list)
      if (Object.keys(raidProg).length > 0) {
        const latestRaidName = Object.keys(raidProg)[0];
        const latestRaid = raidProg[latestRaidName];

        if (latestRaid.summary) { // Only show if there's actual progress
          mainEmbed.addFields({
            name: `Raid Progress (${latestRaidName.replace('-', ' ').replace(/\b\w/g, l => l.toUpperCase())})`,
            value: latestRaid.summary,
            inline: false
          });
        }

        // Add a field for total raid progress
        const totalNormal = Object.values(raidProg).reduce((sum, raid) => sum + raid.normal_bosses_killed, 0);
        const totalHeroic = Object.values(raidProg).reduce((sum, raid) => sum + raid.heroic_bosses_killed, 0);
        const totalMythic = Object.values(raidProg).reduce((sum, raid) => sum + raid.mythic_bosses_killed, 0);

        mainEmbed.addFields({
          name: 'Total Raid Progress',
          value: `Normal: ${totalNormal} | Heroic: ${totalHeroic} | Mythic: ${totalMythic}`,
          inline: false
        });
      }
    }

    // Add achievement points if available
    if (characterData.achievement_points) {
      mainEmbed.addFields({
        name: 'Achievement Points',
        value: characterData.achievement_points.toLocaleString(),
        inline: true
      });
    }

    // Add last updated info
    if (characterData.last_crawled_at) {
      const lastUpdated = new Date(characterData.last_crawled_at);
      mainEmbed.setFooter({
        text: `Data provided by Raider.io • Last updated: ${lastUpdated.toISOString().replace('T', ' ').substring(0, 16)} UTC`,
        iconURL: 'https://cdnassets.raider.io/images/brand/Icon_Light_32.png'
      });
    } else {
      mainEmbed.setFooter({
        text: 'Data provided by Raider.io',
        iconURL: 'https://cdnassets.raider.io/images/brand/Icon_Light_32.png'
      });
    }

    // Send the main embed with custom Discord emojis
    console.log('Sending embed with custom Discord emojis');
    await interaction.followUp({
      embeds: [mainEmbed]
    });
  }
};

// Helper function to get class color
function getClassColor(className) {
  const classColors = {
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
  };

  return classColors[className] || 0x0099ff;
}

// Helper function to capitalize first letter
function capitalizeFirstLetter(string) {
  return string.charAt(0).toUpperCase() + string.slice(1);
}

// Helper function to get faction emoji
function getFactionEmoji(faction) {
  // Get the faction emoji from the config
  const config = require('../config.js');

  // Try to use the custom emoji from config
  const factionEmoji = config.factionEmojis[faction.toLowerCase()];

  // Fallback to standard emoji if custom emoji not available
  if (!factionEmoji) {
    return config.fallbackEmojis[faction.toLowerCase()] || (faction.toLowerCase() === 'horde' ? '🔴' : '🔵');
  }

  return factionEmoji;
}
