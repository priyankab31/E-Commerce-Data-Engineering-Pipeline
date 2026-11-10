
CREATE TABLE IF NOT EXISTS customers (
    customer_id VARCHAR(20) PRIMARY KEY,
    customer_name VARCHAR(150),
    email VARCHAR(255),
    city VARCHAR(100),
    country VARCHAR(100),
    registration_date DATE
);

CREATE TABLE IF NOT EXISTS products (
    product_id VARCHAR(20) PRIMARY KEY,
    product_name VARCHAR(150),
    category VARCHAR(100),
    unit_price NUMERIC(12, 2)
);

CREATE TABLE IF NOT EXISTS orders (
    order_id VARCHAR(20) PRIMARY KEY,
    customer_id VARCHAR(20),
    product_id VARCHAR(20),
    order_date DATE,
    quantity INTEGER,
    order_status VARCHAR(30)
);

CREATE TABLE IF NOT EXISTS payments (
    payment_id VARCHAR(20) PRIMARY KEY,
    order_id VARCHAR(20),
    payment_date DATE,
    payment_method VARCHAR(50),
    payment_status VARCHAR(30),
    amount NUMERIC(12, 2)
);

CREATE TABLE IF NOT EXISTS sales (
    order_id VARCHAR(20),
    customer_id VARCHAR(20),
    product_id VARCHAR(20),
    order_date DATE,
    quantity INTEGER,
    order_status VARCHAR(30),
    customer_name VARCHAR(150),
    email VARCHAR(255),
    city VARCHAR(100),
    country VARCHAR(100),
    registration_date DATE,
    product_name VARCHAR(150),
    category VARCHAR(100),
    unit_price NUMERIC(12, 2),
    total_order_value NUMERIC(12, 2),
    paid_amount NUMERIC(12, 2),
    payment_count INTEGER,
    revenue_month VARCHAR(7),
    revenue_difference NUMERIC(12, 2)
);

CREATE TABLE IF NOT EXISTS customer_metrics (
    customer_id VARCHAR(20),
    customer_name VARCHAR(150),
    city VARCHAR(100),
    total_orders INTEGER,
    total_spent NUMERIC(14, 2),
    average_order_value NUMERIC(14, 2)
);

CREATE TABLE IF NOT EXISTS product_metrics (
    product_id VARCHAR(20),
    product_name VARCHAR(150),
    category VARCHAR(100),
    units_sold INTEGER,
    total_revenue NUMERIC(14, 2)
);

CREATE INDEX IF NOT EXISTS idx_orders_customer
    ON orders(customer_id);

CREATE INDEX IF NOT EXISTS idx_orders_product
    ON orders(product_id);

CREATE INDEX IF NOT EXISTS idx_sales_order_date
    ON sales(order_date);

CREATE INDEX IF NOT EXISTS idx_sales_revenue_month
    ON sales(revenue_month);

