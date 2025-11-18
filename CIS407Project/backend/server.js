// imports 
const sqlite3 = require('sqlite3').verbose();
const crypto = require('crypto');
const express = require('express'); // <-- Import Express

//Server Setup
const app = express(); 
app.use(express.json()); // server reads JSON from requests
const PORT = 5000; // server port

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
// this is just a note for myself for postman testing: http://localhost:5000/register
app.post('/register', async (req, res) => {
   
    const { username, email, password } = req.body;

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
// this is just a note for myself for postman testing:  http://localhost:5000/login
app.post('/login', async (req, res) => {
    const { username, password } = req.body;

    if (!username || !password) {
        return res.status(400).json({ error: 'Username and password are required' });
    }

    try {
       
        const result = await loginUser(username, password);
       
        res.status(200).json(result);

    } catch (error) {
        
        res.status(400).json({ error: error.toString() });
    }
});

//Menu Endpoint
// this is just a note for myself for postman testing: GET http://localhost:5000/menu
app.get('/menu', (req, res) => {

    const sql = "SELECT * FROM menu_items";

    db.all(sql, [], (err, rows) => {
        if (err) {
            
            return res.status(400).json({ error: err.message });
        }
        
        res.json(rows);
    });
});

//Place Order Endpoint 
// this is just a note for myself for postman testing: POST  http://localhost:3000/order
app.post('/order', (req, res) => {
    const { userId, items, totalAmount } = req.body;

    // Basic validation
    if (!userId || !items || items.length === 0) {
        return res.status(400).json({ error: 'Missing userId or items' });
    }

  
    const sqlOrder = "INSERT INTO orders (user_id, total_amount) VALUES (?, ?)";
    
    db.run(sqlOrder, [userId, totalAmount], function(err) {
        if (err) {
            return res.status(400).json({ error: err.message });
        }

        const newOrderId = this.lastID; // 

        // this part adds to our order_items table to link items to the order
        const sqlItem = "INSERT INTO order_items (order_id, item_id, quantity, price_per_item) VALUES (?, ?, ?, ?)";
        const stmt = db.prepare(sqlItem);

        items.forEach(item => {
            stmt.run(newOrderId, item.itemId, item.quantity, item.price);
        });

        stmt.finalize(); 

        res.status(201).json({ 
            message: 'Order placed successfully!', 
            orderId: newOrderId 
        });
    });
});

//  START THE SERVER
app.listen(PORT, () => {
    console.log(`Server is running and listening on http://localhost:${PORT}`);
});