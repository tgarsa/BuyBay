
-- CREATE TABLES sold_products
DROP TABLE IF EXISTS sold_products_bronze;
CREATE TABLE sold_products_bronze (
    id SERIAL PRIMARY KEY,
    license_plate VARCHAR NOT NULL,
    status VARCHAR NOT NULL,
    platform VARCHAR NOT NULL,
    created_at timestamp NOT NULL,
    shipped_at timestamp,
    updated_at timestamp NOT NULL,
    sold_price real NOT NULL,
    country VARCHAR,
    channel_ref VARCHAR NOT NULL,
    platform_fee real
);

DROP TABLE IF EXISTS products_silver;
CREATE TABLE products_silver (
    id SERIAL PRIMARY KEY,
    license_plate VARCHAR NOT NULL,
    status VARCHAR NOT NULL,
    platform VARCHAR NOT NULL,
    created_at timestamp NOT NULL,
    shipped_at timestamp,
    updated_at timestamp NOT NULL,
    sold_price real NOT NULL,
    country VARCHAR,
    channel_ref VARCHAR NOT NULL,
    platform_fee real NOT NULL,
    grading_cat VARCHAR NOT NULL,
    grading_time integer NOT NULL
);


DROP TABLE IF EXISTS products_gold;
CREATE TABLE products_gold (
    id SERIAL PRIMARY KEY,
    license_plate VARCHAR NOT NULL,
    status VARCHAR NOT NULL,
    platform VARCHAR NOT NULL,
    created_at timestamp NOT NULL,
    shipped_at timestamp,
    updated_at timestamp NOT NULL,
    sold_price real NOT NULL,
    country VARCHAR ,
    transport_cost real NOT NULL,
    channel_ref VARCHAR NOT NULL,
    platform_fee real NOT NULL,
    grading_cat VARCHAR NOT NULL,
    grading_fee real NOT NULL,
    grading_time integer NOT NULL
);

-- CREATE TABLES graded_products
DROP TABLE IF EXISTS graded_products_bronze;
CREATE TABLE graded_products_bronze (
    id SERIAL PRIMARY KEY,
    license_plate VARCHAR NOT NULL,
    grading_cat VARCHAR NOT NULL,
    grading_time integer NOT NULL,
    created_at timestamp NOT NULL,
    updated_at timestamp NOT NULL
);


-- CREATE TABLES grading_fees
DROP TABLE IF EXISTS grading_fees_bronze;
CREATE TABLE grading_fees_bronze (
    id SERIAL PRIMARY KEY,
    grading_cat VARCHAR NOT NULL,
    cost real NOT NULL,
    created_at timestamp NOT NULL,
    updated_at timestamp NOT NULL
);

DROP TABLE IF EXISTS grading_fees_silver;
CREATE TABLE grading_fees_silver (
    id SERIAL PRIMARY KEY,
    grading_cat VARCHAR NOT NULL,
    cost real NOT NULL,
    created_at timestamp NOT NULL,
    updated_at timestamp NOT NULL
);


-- CREATE TABLES transport_cost
DROP TABLE IF EXISTS transport_cost_bronze;
CREATE TABLE transport_cost_bronze (
    id SERIAL PRIMARY KEY,
    country VARCHAR NOT NULL,
    transport_cost real NOT NULL,
    created_at timestamp NOT NULL,
    updated_at timestamp NOT NULL
);

DROP TABLE IF EXISTS transport_cost_silver;
CREATE TABLE transport_cost_silver (
    id SERIAL PRIMARY KEY,
    country VARCHAR NOT NULL,
    transport_cost real NOT NULL,
    created_at timestamp NOT NULL,
    updated_at timestamp NOT NULL
);

-- CREATE TABLES platform_cost_cost
DROP TABLE IF EXISTS platform_cost_bronze;
CREATE TABLE platform_cost_bronze (
    id SERIAL PRIMARY KEY,
    platform VARCHAR NOT NULL,
    cost real NOT NULL,
    created_at timestamp NOT NULL,
    updated_at timestamp NOT NULL
);


DROP TABLE IF EXISTS platform_cost_silver;
CREATE TABLE platform_cost_silver (
    id SERIAL PRIMARY KEY,
    platform VARCHAR NOT NULL,
    cost real NOT NULL,
    created_at timestamp NOT NULL,
    updated_at timestamp NOT NULL
);

-- Add the data to the Platform_cost_bronze table.

INSERT into platform_cost_bronze (platform, cost, created_at, updated_at)
VALUES ('Bol', 10, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP) ,
('Amazon', 10.5, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
('Ebay', 9, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
('Everything else', 11, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)



