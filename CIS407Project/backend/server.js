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
    db.run('PRAGMA foreign_keys = ON');
});


function hashPassword(password) {
    return crypto.createHash('sha256').update(password).digest('hex');
}

function dbGet(sql, params = []) {
    return new Promise((resolve, reject) => {
        db.get(sql, params, (err, row) => {
            if (err) return reject(err);
            resolve(row);
        });
    });
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

function checkIsAdmin(req, res, next) {

    const requestedUserId = req.body.userId || req.query.userId;
    
    const adminUserId = 2; 

    if (requestedUserId && parseInt(requestedUserId) === adminUserId) {
        next(); 
    } else {
        res.status(403).json({ error: 'Access Denied: Must be authenticated as Admin.' });
    }
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
// this is just a note for myself for postman testing: POST  http://localhost:5000/order
app.post('/order', async (req, res) => {
    // CRITICAL: Ensure restaurantId is included in the request body
    const { userId, items, totalAmount, cardNumber, cardHolder, restaurantId } = req.body; 
    
    const orderTotal = parseFloat(totalAmount);

    if (!userId || !items || items.length === 0 || !totalAmount || !cardNumber || !cardHolder || !restaurantId || isNaN(orderTotal)) {
        return res.status(400).json({ error: 'Missing required fields: userId, items, totalAmount, cardNumber, cardHolder, or restaurantId.' });
    }

    // Function to handle rollbacks during the transaction process
    const handleRollback = (err, status = 500, msg) => {
        db.run("ROLLBACK;");
        console.error("TRANSACTION ROLLED BACK:", err ? err.message : msg);
        return res.status(status).json({ error: msg || 'A critical database error occurred. Transaction rolled back.' });
    };

    db.serialize(async () => {
        try {
            db.run("BEGIN TRANSACTION;");

            const driverSql = "SELECT delivery_person_id FROM restaurants WHERE restaurant_id = ?";
            const restaurant = await dbGet(driverSql, [restaurantId]);
            
            if (!restaurant) throw new Error('Selected restaurant not found.');
            const assignedDriverId = restaurant.delivery_person_id;

            // Check card balance and ownership
            const sqlCheckCard = `SELECT amount FROM payment_cards WHERE card_number = ? AND card_holder = ? AND user_id = ?;`;
            const card = await dbGet(sqlCheckCard, [cardNumber, cardHolder, userId]);
            
            if (!card) throw new Error('Card details failed verification.');
            
            // Check for sufficient funds
            if (card.amount < orderTotal) {
                return handleRollback(null, 402, `Transaction declined: Insufficient funds. Available: $${card.amount.toFixed(2)}`);
            }

            // Deduct funds
            const newBalance = card.amount - orderTotal;
            const sqlDeduct = `UPDATE payment_cards SET amount = ? WHERE card_number = ?;`;
           
            const fundDeductionResult = await new Promise((resolve, reject) => {
                db.run(sqlDeduct, [newBalance.toFixed(2), cardNumber], function(err) {
                    if (err) return reject(err);
                    resolve(this.changes);
                });
            });

            if (fundDeductionResult === 0) {
                 return handleRollback(null, 500, 'Fund deduction failed to update card balance.');
            }

            const sqlOrder = "INSERT INTO orders (user_id, total_amount, payment_method, payment_status, restaurant_id, delivery_person_id) VALUES (?, ?, 'card', 'paid', ?, ?);";
            
            const orderInsertionResult = await new Promise((resolve, reject) => {
                db.run(sqlOrder, [userId, orderTotal, restaurantId, assignedDriverId], function(err) {
                    if (err) return reject(err);
                    resolve(this.lastID);
                });
            });
            const newOrderId = orderInsertionResult; 

            const sqlItem = "INSERT INTO order_items (order_id, item_id, quantity, price_per_item) VALUES (?, ?, ?, ?)";
            const stmt = db.prepare(sqlItem);

            items.forEach(item => {
                stmt.run(newOrderId, item.itemId, item.quantity, item.price);
            });

            // Finalize statement and commit
            stmt.finalize(() => {
                db.run("COMMIT;", (commitErr) => {
                    if (commitErr) throw commitErr;
                    res.status(201).json({ 
                        message: `Order placed successfully! Driver ${assignedDriverId} assigned. New balance: $${newBalance.toFixed(2)}`, 
                        orderId: newOrderId 
                    });
                });
            });

        } catch (error) {
            handleRollback(error, 500, error.message);
        }
    });
});


// Order History Endpoint 
// Get Order History (With Items!)
// GET request to http://localhost:5000/my-orders/1
app.get('/my-orders/:userId', (req, res) => {
    const userId = req.params.userId;

    const sql = `
        SELECT 
            o.order_id, o.status, o.total_amount, o.order_time, o.payment_status,
            m.name, oi.quantity, oi.price_per_item
        FROM orders o
        JOIN order_items oi ON o.order_id = oi.order_id
        JOIN menu_items m ON oi.item_id = m.item_id
        WHERE o.user_id = ?
        ORDER BY o.order_time DESC
    `;

    db.all(sql, [userId], (err, rows) => {
        if (err) return res.status(400).json({ error: err.message });

        const ordersMap = {};

        rows.forEach(row => {
            if (!ordersMap[row.order_id]) {
                ordersMap[row.order_id] = {
                    orderId: row.order_id,
                    status: row.status,
                    total: row.total_amount,
                    date: row.order_time,
                    paymentStatus: row.payment_status, // New field for history
                    items: []
                };
            }
            ordersMap[row.order_id].items.push({
                name: row.name,
                quantity: row.quantity,
                price: row.price_per_item
            });
        });

        const ordersList = Object.values(ordersMap);
        res.json(ordersList);
    });
});

// Update Order Status Endpoint 
// PATCH request to http://localhost:5000/order/1 
// (this is also for postman, but you might need this one more than me)
// this will be important for the admin panel to update the order status
// tbh instead of making the admin type in each new status if you could hardcode some buttons i think that would be user friendly
// Body: { "status": "completed" }
app.patch('/order/:orderId', (req, res) => {
    const orderId = req.params.orderId;
    const { status } = req.body;

    const allowedStatuses = ['pending', 'in_progress', 'completed', 'cancelled'];
    if (!allowedStatuses.includes(status)) {
        return res.status(400).json({ error: "Invalid status value" });
    }

    const sql = "UPDATE orders SET status = ? WHERE order_id = ?";

    db.run(sql, [status, orderId], function(err) {
        if (err) {
            return res.status(400).json({ error: err.message });
        }
        if (this.changes === 0) {
            return res.status(404).json({ error: "Order not found" });
        }
        res.json({ message: `Order ${orderId} updated to ${status}` });
    });
});

// Stuff for the Admin Panel 

// View All Orders
// GET request to http://localhost:5000/admin/orders
app.get('/admin/orders', checkIsAdmin, (req, res) => {
    const sql = `
        SELECT 
            o.order_id, o.status, o.total_amount, o.order_time, o.payment_status, o.delivery_person_id,
            m.name, oi.quantity, oi.price_per_item, u.username
        FROM orders o
        JOIN order_items oi ON o.order_id = oi.order_id
        JOIN menu_items m ON oi.item_id = m.item_id
        JOIN users u ON o.user_id = u.user_id
        ORDER BY o.order_time DESC
    `;

    db.all(sql, [], (err, rows) => {
        if (err) return res.status(400).json({ error: err.message });

        const ordersMap = {};
        rows.forEach(row => {
            if (!ordersMap[row.order_id]) {
                ordersMap[row.order_id] = {
                    orderId: row.order_id,
                    username: row.username, 
                    status: row.status,
                    total: row.total_amount,
                    date: row.order_time,
                    paymentStatus: row.payment_status,
                    items: []
                };
            }
            ordersMap[row.order_id].items.push({
                name: row.name,
                quantity: row.quantity,
                price: row.price_per_item
            });
        });

        res.json(Object.values(ordersMap));
    });
});

// Add new menu item 
// POST request to http://localhost:5000/admin/menu-items
app.post('/admin/menu-items', checkIsAdmin, (req, res) => {
    const { name, description, price, category, image_url } = req.body; // <-- New variable
    
    const sql = "INSERT INTO menu_items (name, description, price, category, image_url) VALUES (?, ?, ?, ?, ?)";
    
    db.run(sql, [name, description, price, category, image_url], function(err) {
        if (err) return res.status(400).json({ error: err.message });
        res.status(201).json({ message: "Item added", itemId: this.lastID });
    });
});

// Delete Menu Item 
// DELETE request to http://localhost:5000/admin/menu-items/10 (10 is the item id this will need to be changed)
app.delete('/admin/menu-items/:id', checkIsAdmin, (req, res) => {
    const itemId = req.params.id;
    
    const sql = "DELETE FROM menu_items WHERE item_id = ?";
    
    db.run(sql, [itemId], function(err) {
        if (err) return res.status(400).json({ error: err.message });
        res.json({ message: `Item ${itemId} deleted` });
    });
});

// Get Single Menu Item (this pairs with the edit function and a function you need on
// the frontend to get the item details to prefill the edit form)
// GET request to http://localhost:5000/admin/menu-items/10
app.get('/admin/menu-items/:id', checkIsAdmin, (req, res) => {
    const itemId = req.params.id;
    const sql = "SELECT item_id, name, description, price, category, image_url FROM menu_items WHERE item_id = ?";
    
    db.get(sql, [itemId], (err, row) => {
        if (err) return res.status(400).json({ error: err.message });
        if (!row) return res.status(404).json({ message: "Item not found" });
        
        res.json(row);
    });
});

// Edit menu items 
// PUT request to http://localhost:5000/admin/menu-items/10 (1 is the item id)
// Body: { "name": "Updated Burger", "description": "Now with extra cheese", "price": 10.99, "category": "entree" }
app.put('/admin/menu-items/:id', checkIsAdmin, (req, res) => {
    const itemId = req.params.id;
    const { name, description, price, category, image_url } = req.body; 

    const sql = "UPDATE menu_items SET name = ?, description = ?, price = ?, category = ?, image_url = ? WHERE item_id = ?";

    db.run(sql, [name, description, price, category, image_url, itemId], function(err) {
        if (err) {
            return res.status(400).json({ error: err.message });
        }
        if (this.changes === 0) return res.status(404).json({ error: "Menu item not found" });
        res.json({ message: `Menu item ${itemId} updated successfully` });
    });
});

//  START THE SERVER
app.listen(PORT, () => {
    console.log(`Server is running and listening on http://localhost:${PORT}`);
});