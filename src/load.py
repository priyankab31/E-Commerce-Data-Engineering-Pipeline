
import os
from pathlib import Path

from sqlalchemy import create_engine, text

from src.logger import get_logger

logger = get_logger(__name__)

BASE_DIR = Path(__file__).resolve().parents[1]
PROCESSED_DIR = BASE_DIR / "data" / "processed"

TABLES = [
    "customers",
    "products",
    "orders",
    "payments",
    "sales",
    "customer_metrics",
    "product_metrics"
]


def save_processed_data(datasets):
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

    for name, df in datasets.items():
        output_file = PROCESSED_DIR / f"{name}.csv"
        df.to_csv(output_file, index=False)
        logger.info(
            "Saved %s records to %s",
            len(df),
            output_file
        )

    return PROCESSED_DIR


def load_to_postgres(datasets):
    database_url = os.getenv("DATABASE_URL")

    if not database_url:
        raise ValueError(
            "DATABASE_URL environment variable is not configured."
        )

    engine = create_engine(
        database_url,
        pool_pre_ping=True
    )

    try:
        with engine.begin() as connection:
            for table_name in TABLES:
                df = datasets[table_name]

                df.to_sql(
                    name=table_name,
                    con=connection,
                    if_exists="replace",
                    index=False,
                    chunksize=1000,
                    method="multi"
                )

                logger.info(
                    "Loaded %d records into %s",
                    len(df),
                    table_name
                )

            connection.execute(
                text("SELECT 1")
            )

        logger.info("PostgreSQL loading completed successfully.")

    except Exception:
        logger.exception("PostgreSQL loading failed.")
        raise

    finally:
        engine.dispose()

