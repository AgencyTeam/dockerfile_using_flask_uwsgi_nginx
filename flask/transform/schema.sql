DROP TABLE IF EXISTS user;

CREATE TABLE user (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL
);

-- CREATE TABLE master (
--     product_id TEXT PRIMARY KEY,
--     season TEXT,
--     status TEXT,
--     product_name TEXT,
--     sell_price INTEGER,
--     deliver_price INTEGER,
--     package_price INTEGER,
--     tax INTEGER,
--     MSRP INTEGER,
--     supply_price INTEGER
-- );