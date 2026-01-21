-- Схема базы данных для интернет-магазина

CREATE TABLE orders (
    id SERIAL PRIMARY KEY,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    product_name VARCHAR(100) NOT NULL,
    category VARCHAR(50) NOT NULL,
    price DECIMAL(10, 2) NOT NULL,
    quantity INTEGER NOT NULL,
    city VARCHAR(50) NOT NULL,
    customer_age INTEGER,
    payment_method VARCHAR(20)
);

-- Индексы для оптимизации запросов
CREATE INDEX idx_orders_created_at ON orders(created_at);
CREATE INDEX idx_orders_category ON orders(category);
CREATE INDEX idx_orders_city ON orders(city);
