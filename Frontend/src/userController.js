// src/userController.js
const express = require('express');
const { exec } = require('child_process');
const bcrypt = require('bcrypt');
const router = express.Router();
const path = require('path');
const db = require('./db');

// Registration Endpoint
router.post('/register', async (req, res) => {
  const { username, email, password } = req.body;

  try {
    // Hash the password
    const hashedPassword = await bcrypt.hash(password, 10);

    // Correct the script path
    const scriptPath = path.join(__dirname, '..', 'sql_scripts', 'main.py');

    exec(`python3 ${scriptPath} ${username} ${email} ${hashedPassword}`, (error, stdout, stderr) => {
      if (error) {
        console.error(`Script execution error: ${error.message}`);
        console.error(`Script stderr: ${stderr}`);
        return res.status(500).json({ message: 'Registration failed during data processing.' });
      }
      console.log(`Script output: ${stdout}`);
      return res.status(200).json({ message: `User ${username} registered successfully.` });
    });
  } catch (hashError) {
    console.error(`Hashing error: ${hashError.message}`);
    return res.status(500).json({ error: 'Error hashing password.' });
  }
});

// Login Endpoint
router.post('/login', (req, res) => {
  const { username, password } = req.body;

  const getUserQuery = 'SELECT * FROM users WHERE username = ?';
  db.query(getUserQuery, [username], async (err, results) => {
    if (err) {
      console.error(`Database error: ${err.message}`);
      return res.status(500).json({ error: err.message });
    }

    if (results.length === 0) {
      return res.status(400).json({ message: 'Invalid username or password.' });
    }

    const user = results[0];

    // Compare the password
    const match = await bcrypt.compare(password, user.password);
    if (!match) {
      return res.status(400).json({ message: 'Invalid username or password.' });
    }

    // Successful login
    res.status(200).json({ message: `Welcome back, ${username}!` });
  });
});

module.exports = router;