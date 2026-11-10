from pathlib import Path
import pandas as pd

from src.logger import get_logger

logger = get_logger(__name__)

BASE_DIR = Path(__file__).resolve().parents[1]
RAW_DIR = BASE_DIR / "data" / "raw"


def extract_csv(filename):
    file_path = RAW_DIR / filename

    logger.info("Starting extraction: %s", filename)

    if not file_path.exists():
        raise FileNotFoundError(f"Source file not found: {file_path}")

    try:
        df = pd.read_csv(file_path)

        if df.empty:
            raise ValueError(f"Source file is empty: {filename}")

        logger.info(
            "Successfully extracted %s records from %s",
            len(df),
            filename
        )

        return df

    except Exception:
        logger.exception("Extraction failed for %s", filename)
        raise


def extract_all():
    datasets = {
        "customers": extract_csv("customers.csv"),
        "products": extract_csv("products.csv"),
        "orders": extract_csv("orders.csv"),
        "payments": extract_csv("payments.csv")
    }

    return datasets
