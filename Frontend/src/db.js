// sql_scripts/db.js
const mysql = require('mysql2');
require('dotenv').config();

// Create a connection to the database
const db = mysql.createConnection({
  host: process.env.DB_HOST || '127.0.0.1',
  user: process.env.DB_USER || 'root',
  password: process.env.DB_PASSWORD || '279936',
  database: process.env.DB_NAME || 'cpdbs',
});

// Connect to the database
db.connect((err) => {
  if (err) {
    console.error('Database connection failed:', err.stack);
    return;
  }
  console.log('Connected to the database.');
});

module.exports = db;