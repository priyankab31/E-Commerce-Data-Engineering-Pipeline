
import pandas as pd
import numpy as np

from src.logger import get_logger
from src.data_quality import (
    check_required_columns,
    check_duplicates
)

logger = get_logger(__name__)


def transform_customers(df):
    logger.info("Transforming customer data")

    required = [
        "customer_id", "customer_name", "email",
        "city", "country", "registration_date"
    ]
    check_required_columns(df, required, "customers")

    df = df.copy()
    df = df.drop_duplicates(subset=["customer_id"])
    df = df.dropna(subset=["customer_id", "email"])

    df["email"] = df["email"].astype("string").str.strip().str.lower()
    df["customer_name"] = df["customer_name"].astype("string").str.strip()
    df["city"] = df["city"].astype("string").str.strip()
    df["country"] = df["country"].astype("string").str.strip()
    df["registration_date"] = pd.to_datetime(
        df["registration_date"], errors="coerce"
    )

    df = df.dropna(subset=["registration_date"])

    logger.info("Customer records after cleaning: %d", len(df))
    return df


def transform_products(df):
    logger.info("Transforming product data")

    required = ["product_id", "product_name", "category", "unit_price"]
    check_required_columns(df, required, "products")

    df = df.copy()
    df = df.drop_duplicates(subset=["product_id"])

    df["unit_price"] = pd.to_numeric(
        df["unit_price"], errors="coerce"
    )
    df = df.dropna(subset=["product_id", "unit_price"])
    df = df[df["unit_price"] >= 0]

    df["product_name"] = df["product_name"].astype("string").str.strip()
    df["category"] = df["category"].astype("string").str.strip()

    logger.info("Product records after cleaning: %d", len(df))
    return df


def transform_orders(df):
    logger.info("Transforming order data")

    required = [
        "order_id", "customer_id", "product_id",
        "order_date", "quantity", "order_status"
    ]
    check_required_columns(df, required, "orders")

    df = df.copy()
    df = df.drop_duplicates(subset=["order_id"])

    df["order_date"] = pd.to_datetime(
        df["order_date"], errors="coerce"
    )
    df["quantity"] = pd.to_numeric(
        df["quantity"], errors="coerce"
    )

    df = df.dropna(
        subset=["order_id", "customer_id", "product_id",
                "order_date", "quantity"]
    )
    df = df[df["quantity"] > 0]

    df["order_status"] = (
        df["order_status"].astype("string").str.strip().str.title()
    )

    logger.info("Order records after cleaning: %d", len(df))
    return df


def transform_payments(df):
    logger.info("Transforming payment data")

    required = [
        "payment_id", "order_id", "payment_date",
        "payment_method", "payment_status", "amount"
    ]
    check_required_columns(df, required, "payments")

    df = df.copy()
    df = df.drop_duplicates(subset=["payment_id"])

    df["payment_date"] = pd.to_datetime(
        df["payment_date"], errors="coerce"
    )
    df["amount"] = pd.to_numeric(
        df["amount"], errors="coerce"
    )

    df = df.dropna(
        subset=["payment_id", "order_id", "payment_date", "amount"]
    )
    df = df[df["amount"] >= 0]

    df["payment_method"] = (
        df["payment_method"].astype("string").str.strip().str.title()
    )
    df["payment_status"] = (
        df["payment_status"].astype("string").str.strip().str.title()
    )

    logger.info("Payment records after cleaning: %d", len(df))
    return df


def transform_all(datasets):
    customers = transform_customers(datasets["customers"])
    products = transform_products(datasets["products"])
    orders = transform_orders(datasets["orders"])
    payments = transform_payments(datasets["payments"])

    # Check foreign-key relationships
    orders = orders[
        orders["customer_id"].isin(customers["customer_id"])
        & orders["product_id"].isin(products["product_id"])
    ].copy()

    payments = payments[
        payments["order_id"].isin(orders["order_id"])
    ].copy()

    # Keep completed orders for sales analytics
    completed_orders = orders[
        orders["order_status"].eq("Completed")
    ].copy()

    # Join orders with customers and products
    sales = completed_orders.merge(
        customers,
        on="customer_id",
        how="inner"
    )

    sales = sales.merge(
        products,
        on="product_id",
        how="inner"
    )

    sales["total_order_value"] = (
        sales["quantity"] * sales["unit_price"]
    )

    # Aggregate successful payments by order
    paid_payments = payments[
        payments["payment_status"].eq("Paid")
    ]

    payment_summary = (
        paid_payments.groupby("order_id", as_index=False)
        .agg(
            paid_amount=("amount", "sum"),
            payment_count=("payment_id", "count")
        )
    )

    sales = sales.merge(
        payment_summary,
        on="order_id",
        how="left"
    )

    sales["paid_amount"] = sales["paid_amount"].fillna(0)
    sales["payment_count"] = (
        sales["payment_count"].fillna(0).astype(int)
    )

    sales["revenue_month"] = (
        sales["order_date"].dt.to_period("M").astype(str)
    )

    sales["revenue_difference"] = (
        sales["total_order_value"] - sales["paid_amount"]
    )

    # Customer-level metrics
    customer_metrics = (
        sales.groupby(
            ["customer_id", "customer_name", "city"],
            as_index=False
        )
        .agg(
            total_orders=("order_id", "nunique"),
            total_spent=("total_order_value", "sum"),
            average_order_value=("total_order_value", "mean")
        )
    )

    # Product-level metrics
    product_metrics = (
        sales.groupby(
            ["product_id", "product_name", "category"],
            as_index=False
        )
        .agg(
            units_sold=("quantity", "sum"),
            total_revenue=("total_order_value", "sum")
        )
    )

    logger.info("Sales records created: %d", len(sales))

    return {
        "customers": customers,
        "products": products,
        "orders": orders,
        "payments": payments,
        "sales": sales,
        "customer_metrics": customer_metrics,
        "product_metrics": product_metrics
    }

