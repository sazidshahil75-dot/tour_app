-- Run this once to set up the database
-- mysql -u root -p < schema.sql

CREATE DATABASE IF NOT EXISTS tour_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE tour_db;

CREATE TABLE IF NOT EXISTS trips (
    id               INT AUTO_INCREMENT PRIMARY KEY,
    destination      VARCHAR(255)   NOT NULL,
    duration_days    INT            NOT NULL DEFAULT 1,
    transport_type   VARCHAR(100),
    transport_detail VARCHAR(255),
    cost_transport   DECIMAL(12,2)  DEFAULT 0,
    cost_hotel       DECIMAL(12,2)  DEFAULT 0,
    cost_food        DECIMAL(12,2)  DEFAULT 0,
    cost_tickets     DECIMAL(12,2)  DEFAULT 0,
    cost_guide       DECIMAL(12,2)  DEFAULT 0,
    cost_misc        DECIMAL(12,2)  DEFAULT 0,
    split_method     VARCHAR(50)    DEFAULT 'equal',
    total_cost       DECIMAL(12,2)  DEFAULT 0,
    created_at       DATETIME       DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS tourists (
    id            INT AUTO_INCREMENT PRIMARY KEY,
    trip_id       INT            NOT NULL,
    name          VARCHAR(255)   NOT NULL,
    share_pct     DECIMAL(6,2)   DEFAULT 0,
    share_amount  DECIMAL(12,2)  DEFAULT 0,
    FOREIGN KEY (trip_id) REFERENCES trips(id) ON DELETE CASCADE
);
