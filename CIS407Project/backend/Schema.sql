
-- Schema.sql shows what the database structure looks like, please dont actually try to run this one
-- you may be looking for Food_app.db
CREATE TABLE users (
    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
    username VARCHAR(50) NOT NULL UNIQUE,
    email VARCHAR(100) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE menu_items (
    item_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(100) NOT NULL,
    description TEXT,
    price DECIMAL(10, 2) NOT NULL,
    category VARCHAR(20) NOT NULL -- 'entree', 'side', 'drink', etc.
    image_url VARCHAR(255)
);

CREATE TABLE orders (
    order_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INT NOT NULL,
    order_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    status VARCHAR(20) DEFAULT 'pending', -- e.g., 'pending', 'in the works', 'completed'
    total_amount DECIMAL(10, 2),

    -- for payment 
    payment_method VARCHAR(50),
    payment_status VARCHAR(20) DEFAULT 'pending', 
    restaurant_id INT NOT NULL,
    delivery_person_id INT,


    FOREIGN KEY (user_id) REFERENCES users(user_id)
    FOREIGN KEY (restaurant_id) REFERENCES restaurants(restaurant_id),
    FOREIGN KEY (delivery_person_id) REFERENCES delivery_personnel(delivery_person_id)
);

CREATE TABLE order_items (
    order_item_id INTEGER PRIMARY KEY AUTOINCREMENT,
    order_id INT NOT NULL,
    item_id INT NOT NULL,
    quantity INT NOT NULL,
    price_per_item DECIMAL(10, 2) NOT NULL,
    FOREIGN KEY (order_id) REFERENCES orders(order_id),
    FOREIGN KEY (item_id) REFERENCES menu_items(item_id)
);

CREATE TABLE restaurants (
    restaurant_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(100) NOT NULL,
    location VARCHAR(100) NOT NULL,
    -- links to a specific driver for simplicity sake 
    delivery_person_id INT UNIQUE,
    FOREIGN KEY (delivery_person_id) REFERENCES delivery_personnel(delivery_person_id)
);

CREATE TABLE delivery_personnel (
    delivery_person_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(100) NOT NULL,
    status VARCHAR(20) DEFAULT 'available' -- 'available', 'on_delivery', 'off_duty' // we might just stick with forver
                                             -- available for simplicity
);

CREATE TABLE payment_cards (
    card_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INT NOT NULL,
    card_holder VARCHAR(100) NOT NULL,
    card_number VARCHAR(16) NOT NULL,
    -- this is for a simulated balance only, we wouldn't actually store this 
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);