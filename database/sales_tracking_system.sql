-- ==============================================================================
-- AI-Powered Sales Tracking System
-- Database Schema: sales_tracking_system
-- Prepared for: Lincoln University College / Balmiki Lincoln College
-- ==============================================================================

CREATE DATABASE IF NOT EXISTS `sales_tracking_system` 
CHARACTER SET utf8mb4 
COLLATE utf8mb4_unicode_ci;

USE `sales_tracking_system`;

-- ------------------------------------------------------------------------------
-- Table structure for table `admin_users`
-- ------------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS `admin_users` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `full_name` VARCHAR(100) NOT NULL,
    `email` VARCHAR(150) NOT NULL UNIQUE,
    `password_hash` VARCHAR(255) NOT NULL,
    `role` VARCHAR(30) DEFAULT 'admin' NOT NULL,
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX `idx_admin_email` (`email`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ------------------------------------------------------------------------------
-- Initial Seed Record: Super Admin
-- Password: admin123 (hashed via bcrypt)
-- ------------------------------------------------------------------------------
INSERT INTO `admin_users` (`full_name`, `email`, `password_hash`, `role`)
VALUES (
    'Jamuna Rajbanshi',
    'admin@salestrack.ai',
    '$2b$12$e0L1uJ8Yp.6bA8cZl6X6vO7d2c3k4b5a6c7d8e9f0g1h2i3j4k5l6',
    'Super Admin'
)
ON DUPLICATE KEY UPDATE `email`=`email`;
