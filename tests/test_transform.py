
import pandas as pd

from src.transform import (
    transform_customers,
    transform_products,
    transform_orders,
    transform_payments,
    transform_all
)


def test_customer_duplicate_removal():
    df = pd.DataFrame({
        "customer_id": ["C001", "C001"],
        "customer_name": ["Alice", "Alice"],
        "email": ["alice@example.com", "alice@example.com"],
        "city": ["Berlin", "Berlin"],
        "country": ["Germany", "Germany"],
        "registration_date": ["2026-01-01", "2026-01-01"]
    })

    result = transform_customers(df)

    assert len(result) == 1


def test_product_negative_price_removed():
    df = pd.DataFrame({
        "product_id": ["P001", "P002"],
        "product_name": ["Laptop", "Mouse"],
        "category": ["Electronics", "Accessories"],
        "unit_price": [1200, -10]
    })

    result = transform_products(df)

    assert len(result) == 1
    assert result.iloc[0]["unit_price"] == 1200


def test_order_invalid_quantity_removed():
    df = pd.DataFrame({
        "order_id": ["O001", "O002"],
        "customer_id": ["C001", "C002"],
        "product_id": ["P001", "P002"],
        "order_date": ["2026-01-01", "2026-01-02"],
        "quantity": [2, -1],
        "order_status": ["Completed", "Completed"]
    })

    result = transform_orders(df)

    assert len(result) == 1
    assert result.iloc[0]["quantity"] == 2


def test_invalid_payment_amount_removed():
    df = pd.DataFrame({
        "payment_id": ["PAY001", "PAY002"],
        "order_id": ["O001", "O002"],
        "payment_date": ["2026-01-01", "2026-01-02"],
        "payment_method": ["Card", "PayPal"],
        "payment_status": ["Paid", "Paid"],
        "amount": [100, -50]
    })

    result = transform_payments(df)

    assert len(result) == 1
    assert result.iloc[0]["amount"] == 100


def test_complete_pipeline_creates_sales():
    datasets = {
        "customers": pd.DataFrame({
            "customer_id": ["C001"],
            "customer_name": ["Alice"],
            "email": ["alice@example.com"],
            "city": ["Berlin"],
            "country": ["Germany"],
            "registration_date": ["2026-01-01"]
        }),
        "products": pd.DataFrame({
            "product_id": ["P001"],
            "product_name": ["Laptop"],
            "category": ["Electronics"],
            "unit_price": [1000]
        }),
        "orders": pd.DataFrame({
            "order_id": ["O001"],
            "customer_id": ["C001"],
            "product_id": ["P001"],
            "order_date": ["2026-01-02"],
            "quantity": [2],
            "order_status": ["Completed"]
        }),
        "payments": pd.DataFrame({
            "payment_id": ["PAY001"],
            "order_id": ["O001"],
            "payment_date": ["2026-01-02"],
            "payment_method": ["Card"],
            "payment_status": ["Paid"],
            "amount": [2000]
        })
    }

    result = transform_all(datasets)

    assert len(result["sales"]) == 1
    assert result["sales"].iloc[0]["total_order_value"] == 2000
    assert result["sales"].iloc[0]["paid_amount"] == 2000

