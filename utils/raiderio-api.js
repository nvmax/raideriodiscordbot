const axios = require('axios');

// Default regions to try
const DEFAULT_REGIONS = ['us', 'eu', 'kr', 'tw'];

/**
 * Get character profile from Raider.io API
 * @param {string} name - Character name
 * @param {string} realm - Realm name
 * @param {string} region - Region (us, eu, kr, tw)
 * @returns {Promise<Object>} Character data
 */
async function getCharacterProfile(name, realm, region = 'us') {
  try {
    // Fields to request from the API
    const fields = [
      'gear',
      'guild',
      'raid_progression',
      'mythic_plus_scores_by_season:current',
      'mythic_plus_best_runs',
      'mythic_plus_ranks'
    ].join(',');

    // Make the API request
    const response = await axios.get('https://raider.io/api/v1/characters/profile', {
      params: {
        region,
        realm,
        name,
        fields
      },
      headers: {
        'Accept': 'application/json',
        'User-Agent': 'RaiderBot Discord Bot'
      }
    });

    return response.data;
  } catch (error) {
    console.error(`Error fetching character profile: ${error.message}`);
    return null;
  }
}

/**
 * Try to find a character in multiple regions
 * @param {string} name - Character name
 * @param {string} realm - Realm name
 * @param {Array<string>} regions - Regions to try
 * @returns {Promise<Object>} Character data
 */
async function findCharacterInRegions(name, realm, regions = DEFAULT_REGIONS) {
  for (const region of regions) {
    console.log(`Trying to find ${name} on ${realm} in ${region.toUpperCase()} region...`);
    const characterData = await getCharacterProfile(name, realm, region);
    
    if (characterData) {
      console.log(`Character found in ${region.toUpperCase()} region!`);
      return characterData;
    }
  }
  
  console.log(`Character not found in any region.`);
  return null;
}

module.exports = {
  getCharacterProfile,
  findCharacterInRegions,
  DEFAULT_REGIONS
};
