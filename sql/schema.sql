-- Target Database
USE db_ecomerce_etl;

-- 1. Create Users Table
CREATE TABLE IF NOT EXISTS users (
    user_id INT PRIMARY KEY,
    email VARCHAR(100) NOT NULL,
    signup_date DATE NOT NULL
);

-- 2. Create Orders Table
CREATE TABLE IF NOT EXISTS orders (
    order_id INT PRIMARY KEY,
    user_id INT,
    order_date DATE NOT NULL,
    total_amount DECIMAL(10, 2) NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);
-- Create Data Quality Audit Log Table
CREATE TABLE IF NOT EXISTS data_quality_logs (
    log_id INT AUTO_INCREMENT PRIMARY KEY,
    run_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    target_table VARCHAR(50) NOT NULL,
    check_type VARCHAR(50) NOT NULL,
    records_evaluated INT NOT NULL,
    failures_detected INT NOT NULL,
    status VARCHAR(10) NOT NULL
);
