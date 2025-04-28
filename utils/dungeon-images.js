const fs = require('fs');
const path = require('path');

/**
 * Maps dungeon names to local image files
 * @param {string} dungeonName - The name of the dungeon
 * @returns {string|null} - Path to the local image file or null if not found
 */
function getDungeonImagePath(dungeonName) {
  const imagesDir = path.join(__dirname, '..', 'Images');

  // Normalize dungeon name for matching
  const normalizedName = dungeonName.toLowerCase().replace(/[^a-z0-9]/g, '');

  // Map of normalized dungeon names to image filenames
  const dungeonImageMap = {
    // Current Season dungeons (Season 4) - exact names from API
    'cinderbrewmeadery': 'cinderbrew.jpg',
    'cinderbrew': 'cinderbrew.jpg',
    'brew': 'cinderbrew.jpg',

    'darkflamecleft': 'darkflamecleft.jpg',
    'darkflame': 'darkflamecleft.jpg',
    'dfc': 'darkflamecleft.jpg',

    'operationfloodgate': 'floodgate.jpg',
    'floodgate': 'floodgate.jpg',
    'flood': 'floodgate.jpg',

    'mechagonworkshop': 'mechagon.jpg',
    'mechagon': 'mechagon.jpg',
    'work': 'mechagon.jpg',

    'themotherlode': 'motherload.jpg',
    'motherlode': 'motherload.jpg',
    'ml': 'motherload.jpg',

    'prioryofthesacredflame': 'priory.jpg',
    'priory': 'priory.jpg',
    'psf': 'priory.jpg',

    'therookery': 'rookery.jpg',
    'rookery': 'rookery.jpg',
    'rook': 'rookery.jpg',

    'theaterofpain': 'theaterofpain.jpg',
    'theater': 'theaterofpain.jpg',
    'top': 'theaterofpain.jpg',

    // Add more mappings as needed
  };

  // Get the image filename from the map
  const imageFilename = dungeonImageMap[normalizedName];

  if (!imageFilename) {
    return null;
  }

  // Check if the file exists
  const imagePath = path.join(imagesDir, imageFilename);

  // Debug info
  console.log(`Looking for dungeon image: ${dungeonName}`);
  console.log(`Normalized name: ${normalizedName}`);
  console.log(`Image filename: ${imageFilename}`);
  console.log(`Full path: ${imagePath}`);
  const fileExists = fs.existsSync(imagePath);
  console.log(`File exists: ${fileExists}`);

  // List all files in the images directory
  try {
    const files = fs.readdirSync(imagesDir);
    console.log(`Files in ${imagesDir}:`, files);
  } catch (error) {
    console.error(`Error reading directory ${imagesDir}:`, error.message);
  }

  if (fs.existsSync(imagePath)) {
    return imagePath;
  }

  return null;
}

/**
 * Creates an attachment for a dungeon image
 * @param {string} dungeonName - The name of the dungeon
 * @param {number} index - Index for the attachment filename
 * @returns {Object|null} - AttachmentBuilder object or null if image not found
 */
function createDungeonImageAttachment(dungeonName, index) {
  const { AttachmentBuilder } = require('discord.js');

  const imagePath = getDungeonImagePath(dungeonName);
  if (!imagePath) {
    return null;
  }

  return new AttachmentBuilder(imagePath, { name: `dungeon${index}.jpg` });
}

module.exports = {
  getDungeonImagePath,
  createDungeonImageAttachment
};
