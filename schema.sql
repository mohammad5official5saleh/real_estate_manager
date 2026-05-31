DROP TABLE IF EXISTS properties;
DROP TABLE IF EXISTS users;

CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL
);

CREATE TABLE properties (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    title TEXT NOT NULL,
    location TEXT NOT NULL,
    property_type TEXT NOT NULL,
    area TEXT NOT NULL,
    bedrooms TEXT NOT NULL,
    bathrooms TEXT NOT NULL,
    status TEXT NOT NULL,
    price REAL NOT NULL,
    contact_phone TEXT NOT NULL,
    contact_email TEXT NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users (id)
);