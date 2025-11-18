// imports 
const sqlite3 = require('sqlite3').verbose();
const crypto = require('crypto');
const express = require('express'); // <-- Import Express

//Server Setup
const app = express(); // <-- Create the Express app
app.use(express.json()); // <-- IMPORTANT: This lets your server read JSON from requests
const PORT = 5000; // <-- The port your server will run on

// this connects to the database
const db = new sqlite3.Database('./food_app.db', (err) => {
    if (err) {
        console.error(err.message);
    }
    console.log('Connected to the food_app database.');
});


function hashPassword(password) {
    return crypto.createHash('sha256').update(password).digest('hex');
}

// registration
async function registerUser(username, email, password) {
    const lowerCaseUsername = username.toLowerCase();
    const passwordHash = hashPassword(password);

    return new Promise((resolve, reject) => {
        const checkSql = `SELECT * FROM users WHERE username = ? OR email = ?`;
        db.get(checkSql, [lowerCaseUsername, email], (err, row) => {
            if (err) return reject('Database error during check');
            if (row) return reject('Username or email is already in use');

            const insertSql = `INSERT INTO users (username, email, password_hash) VALUES (?, ?, ?)`;
            db.run(insertSql, [lowerCaseUsername, email, passwordHash], function(err) {
                if (err) return reject('Database error during insert');
                resolve({ message: `User ${lowerCaseUsername} registered successfully`, userId: this.lastID });
            });
        });
    });
}

// Login Function
async function loginUser(username, password) {
    const lowerCaseUsername = username.toLowerCase();

    return new Promise((resolve, reject) => {
        const selectSql = `SELECT * FROM users WHERE username = ?`;
        db.get(selectSql, [lowerCaseUsername], (err, user) => {
            if (err) return reject('Database error');
            if (!user) return reject('Invalid username or password');

            const providedHash = hashPassword(password);
            
            if (providedHash === user.password_hash) {
                resolve({ message: `Login successful! Welcome, ${user.username}`, userId: user.user_id });
            } else {
                reject('Invalid username or password');
            }
        });
    });
}


//  API ENDPOINTS 

// Registration Endpoint 
app.post('/register', async (req, res) => {
    // 'req.body' holds the JSON data your app sends
    const { username, email, password } = req.body;

    // A simple check to make sure you got all the data
    if (!username || !email || !password) {
        return res.status(400).json({ error: 'Username, email, and password are required' });
    }

    try {
        const result = await registerUser(username, email, password);
        res.status(201).json(result);

    } catch (error) {
        res.status(400).json({ error: error.toString() });
    }
});


// Login Endpoint 
app.post('/login', async (req, res) => {
    const { username, password } = req.body;

    if (!username || !password) {
        return res.status(400).json({ error: 'Username and password are required' });
    }

    try {
        // Use the login function you already wrote!
        const result = await loginUser(username, password);
        // Send a "200 OK" success response
        res.status(200).json(result);

    } catch (error) {
        // If loginUser rejected, send an error
        res.status(400).json({ error: error.toString() });
    }
});


//  START THE SERVER
app.listen(PORT, () => {
    console.log(`Server is running and listening on http://localhost:${PORT}`);
});