/**
 * Database Configuration
 * 
 * Connects to the same MongoDB instance used by the Python backend
 * Uses environment variables for connection string
 */

const { MongoClient } = require('mongodb');
require('dotenv').config();

let client = null;
let db = null;

/**
 * Get MongoDB connection string from environment or use default
 * Default matches the Python backend configuration
 */
const MONGODB_URI = process.env.MONGODB_URI || 
  'mongodb+srv://cursorrp_db_user:ka1r5cs2fPu1fcIk@cluster0.7fr4den.mongodb.net/elearning?retryWrites=true&w=majority&appName=Cluster0';

/**
 * Connect to MongoDB database
 * 
 * @returns {Promise<Db>} MongoDB database instance
 */
async function connectDatabase() {
  if (db) {
    return db;
  }

  try {
    client = new MongoClient(MONGODB_URI, {
      serverSelectionTimeoutMS: 5000,
      connectTimeoutMS: 10000,
      socketTimeoutMS: 10000
    });

    await client.connect();
    db = client.db();
    console.log('[ILPG] Connected to MongoDB successfully');
    return db;
  } catch (error) {
    console.error('[ILPG] MongoDB connection error:', error);
    throw error;
  }
}

/**
 * Get database instance (lazy connection)
 * 
 * @returns {Promise<Db>} MongoDB database instance
 */
async function getDatabase() {
  if (!db) {
    await connectDatabase();
  }
  return db;
}

/**
 * Close database connection
 */
async function closeDatabase() {
  if (client) {
    await client.close();
    client = null;
    db = null;
    console.log('[ILPG] MongoDB connection closed');
  }
}

module.exports = {
  connectDatabase,
  getDatabase,
  closeDatabase
};










