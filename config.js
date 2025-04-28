/**
 * Configuration file for the Discord bot
 */

// Load environment variables
require('dotenv').config();

// Get emoji IDs from environment variables
const HORDE_EMOJI_ID = process.env.HORDE_EMOJI_ID || '1366508841042444368';
const ALLIANCE_EMOJI_ID = process.env.ALLIANCE_EMOJI_ID || '1366508892741308638';
const MECHAGON_EMOJI_ID = process.env.MECHAGON_EMOJI_ID || '1366478770353078344';
const CINDERBREW_EMOJI_ID = process.env.CINDERBREW_EMOJI_ID || '1366478766469156945';
const DARKFLAME_EMOJI_ID = process.env.DARKFLAME_EMOJI_ID || '1366478767400161391';
const FLOODGATE_EMOJI_ID = process.env.FLOODGATE_EMOJI_ID || '1366478768880746527';
const MOTHERLODE_EMOJI_ID = process.env.MOTHERLODE_EMOJI_ID || '1366478771359715508';
const PRIORY_EMOJI_ID = process.env.PRIORY_EMOJI_ID || '1366478772295041041';
const ROOKERY_EMOJI_ID = process.env.ROOKERY_EMOJI_ID || '1366478773934886912';
const THEATER_EMOJI_ID = process.env.THEATER_EMOJI_ID || '1366478775184916480';

module.exports = {
  // Custom emoji IDs for dungeons
  // Format: '<:emoji_name:emoji_id>'
  // Example: '<:darkflame:1234567890>'
  // Custom Discord emojis for dungeons
  dungeonEmojis: {
    // Current Season dungeons (Season 2) - custom Discord emojis using environment variables
    'Cinderbrew Meadery': `<:cinderbrew:${CINDERBREW_EMOJI_ID}>`,
    'Darkflame Cleft': `<:darkflamecleft:${DARKFLAME_EMOJI_ID}>`,
    'Operation: Floodgate': `<:floodgate:${FLOODGATE_EMOJI_ID}>`,
    'Mechagon Workshop': `<:mechagon:${MECHAGON_EMOJI_ID}>`,
    'The MOTHERLODE!!': `<:motherload:${MOTHERLODE_EMOJI_ID}>`,
    'Priory of the Sacred Flame': `<:priory:${PRIORY_EMOJI_ID}>`,
    'The Rookery': `<:rookery:${ROOKERY_EMOJI_ID}>`,
    'Theater of Pain': `<:theaterofpain:${THEATER_EMOJI_ID}>`,
  },

  // Faction emojis
  factionEmojis: {
    'horde': `<:horde:${HORDE_EMOJI_ID}>`,
    'alliance': `<:alliance:${ALLIANCE_EMOJI_ID}>`,
  },

  // Fallback emojis if custom emojis aren't available
  fallbackEmojis: {
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
  },

  // Default regions to try when looking up characters
  defaultRegions: ['us', 'eu', 'kr', 'tw'],

  // Maximum number of M+ runs to display
  maxMythicPlusRuns: 3,

  // Whether to show affixes in dungeon run details
  showAffixes: false,
};
