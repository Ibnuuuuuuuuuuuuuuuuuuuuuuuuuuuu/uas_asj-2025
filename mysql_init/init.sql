ALTER USER 'flask_user'@'%' IDENTIFIED WITH mysql_native_password BY 'anis_banjarbaru_projek_uas_asj';
FLUSH PRIVILEGES;

-- Tambahkan ini untuk membuat database jika belum ada (walaupun Docker sudah membuat)
-- Pastikan nama database sesuai dengan MYSQL_DB di .env Anda
CREATE DATABASE IF NOT EXISTS coffeeshop_db;
USE coffeeshop_db;

CREATE TABLE IF NOT EXISTS menu_items (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    description TEXT,
    price DECIMAL(10, 2) NOT NULL,
    category VARCHAR(50)
);