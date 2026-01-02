/**
 * ILPG Server
 * 
 * Express server for Intelligent Learning Pathway Generator
 * 
 * Port: 5002 (separate from Flask 5000 and FastAPI 5001)
 * 
 * Integration:
 * - Connects to same MongoDB as Python backend
 * - Provides REST API for pathway generation
 * - Can be called from frontend or Python backend
 */

const express = require('express');
const cors = require('cors');
const path = require('path');
require('dotenv').config();

const { connectDatabase } = require('./config/database');
const pathwayRoutes = require('./routes/pathwayRoutes');

const app = express();
const PORT = process.env.ILPG_PORT || 5002;

// Middleware
app.use(cors({
  origin: [
    'http://localhost:3000',
    'http://localhost:5173',
    'http://localhost:5174',
    'http://127.0.0.1:5173',
    'http://127.0.0.1:5174'
  ],
  credentials: true
}));

app.use(express.json());
app.use(express.urlencoded({ extended: true }));

// Request logging
app.use((req, res, next) => {
  console.log(`[ILPG] ${req.method} ${req.path}`);
  next();
});

// Routes
app.use('/ilpg', pathwayRoutes);

// Health check endpoint
app.get('/health', (req, res) => {
  res.json({
    status: 'healthy',
    service: 'ilpg-service',
    version: '1.0.0',
    timestamp: new Date().toISOString()
  });
});

// Root endpoint
app.get('/', (req, res) => {
  res.json({
    service: 'Intelligent Learning Pathway Generator (ILPG)',
    version: '1.0.0',
    endpoints: {
      health: '/health',
      evaluate: 'POST /ilpg/evaluate',
      recalculate: 'POST /ilpg/recalculate',
      getPathway: 'GET /ilpg/:studentId',
      getHistory: 'GET /ilpg/:studentId/history'
    }
  });
});

// Error handling middleware
app.use((err, req, res, next) => {
  console.error('[ILPG] Error:', err);
  res.status(err.status || 500).json({
    error: err.message || 'Internal server error',
    service: 'ilpg-service'
  });
});

// 404 handler
app.use((req, res) => {
  res.status(404).json({
    error: 'Endpoint not found',
    service: 'ilpg-service'
  });
});

// Start server
async function startServer() {
  try {
    // Connect to database
    await connectDatabase();

    // Start Express server
    app.listen(PORT, () => {
      console.log(`[ILPG] Server running on http://localhost:${PORT}`);
      console.log(`[ILPG] Health check: http://localhost:${PORT}/health`);
    });
  } catch (error) {
    console.error('[ILPG] Failed to start server:', error);
    process.exit(1);
  }
}

// Handle graceful shutdown
process.on('SIGTERM', async () => {
  console.log('[ILPG] SIGTERM received, shutting down gracefully');
  const { closeDatabase } = require('./config/database');
  await closeDatabase();
  process.exit(0);
});

process.on('SIGINT', async () => {
  console.log('[ILPG] SIGINT received, shutting down gracefully');
  const { closeDatabase } = require('./config/database');
  await closeDatabase();
  process.exit(0);
});

// Start the server
startServer();

module.exports = app;










