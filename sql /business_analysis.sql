
-- 1. Total revenue from completed orders
SELECT
    SUM(total_order_value) AS total_revenue
FROM sales;


-- 2. Monthly revenue trend
SELECT
    revenue_month,
    SUM(total_order_value) AS monthly_revenue
FROM sales
GROUP BY revenue_month
ORDER BY revenue_month;


-- 3. Top 10 customers by spending
SELECT
    customer_id,
    customer_name,
    city,
    total_orders,
    total_spent
FROM customer_metrics
ORDER BY total_spent DESC
LIMIT 10;


-- 4. Best-selling products
SELECT
    product_name,
    category,
    units_sold,
    total_revenue
FROM product_metrics
ORDER BY units_sold DESC;


-- 5. Revenue by product category
SELECT
    category,
    SUM(total_order_value) AS category_revenue
FROM sales
GROUP BY category
ORDER BY category_revenue DESC;


-- 6. Average order value
SELECT
    ROUND(AVG(total_order_value), 2) AS average_order_value
FROM sales;


-- 7. Revenue by city
SELECT
    city,
    COUNT(DISTINCT order_id) AS total_orders,
    SUM(total_order_value) AS revenue
FROM sales
GROUP BY city
ORDER BY revenue DESC;


-- 8. Payment reconciliation
SELECT
    order_id,
    total_order_value,
    paid_amount,
    revenue_difference,
    CASE
        WHEN ABS(revenue_difference) < 0.01 THEN 'Matched'
        WHEN paid_amount = 0 THEN 'Unpaid'
        WHEN paid_amount < total_order_value THEN 'Underpaid'
        ELSE 'Overpaid'
    END AS payment_reconciliation_status
FROM sales
ORDER BY order_id;


-- 9. Running monthly revenue
SELECT
    revenue_month,
    SUM(total_order_value) AS monthly_revenue,
    SUM(SUM(total_order_value)) OVER (
        ORDER BY revenue_month
    ) AS cumulative_revenue
FROM sales
GROUP BY revenue_month
ORDER BY revenue_month;


-- 10. Customer ranking
SELECT
    customer_id,
    customer_name,
    total_spent,
    DENSE_RANK() OVER (
        ORDER BY total_spent DESC
    ) AS customer_rank
FROM customer_metrics
ORDER BY customer_rank;

