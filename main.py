
import argparse
import yaml
from pathlib import Path

from src.logger import get_logger
from src.extract import extract_all
from src.transform import transform_all
from src.load import save_processed_data, load_to_postgres

logger = get_logger("main")

BASE_DIR = Path(__file__).resolve().parent
CONFIG_FILE = BASE_DIR / "config" / "config.yaml"


def load_config():
    with open(CONFIG_FILE, "r", encoding="utf-8") as file:
        return yaml.safe_load(file)


def print_pipeline_summary(datasets):
    logger.info("================ PIPELINE SUMMARY ================")

    for name, df in datasets.items():
        logger.info("%-20s : %d records", name, len(df))

    logger.info("==================================================")


def run_pipeline(load_postgres=False):
    logger.info("E-COMMERCE ETL PIPELINE STARTED")

    config = load_config()

    # Stage 1: Extract
    logger.info("STAGE 1: DATA EXTRACTION")
    raw_datasets = extract_all()

    # Stage 2: Transform and validate
    logger.info("STAGE 2: DATA TRANSFORMATION")
    transformed_datasets = transform_all(raw_datasets)

    # Stage 3: Save processed files
    if config["pipeline"]["save_csv"]:
        logger.info("STAGE 3: SAVING PROCESSED DATA")
        save_processed_data(transformed_datasets)

    # Stage 4: Optional PostgreSQL load
    if load_postgres:
        logger.info("STAGE 4: POSTGRESQL LOAD")
        load_to_postgres(transformed_datasets)
    else:
        logger.info("PostgreSQL load skipped.")

    print_pipeline_summary(transformed_datasets)

    logger.info("ETL PIPELINE COMPLETED SUCCESSFULLY")


def main():
    parser = argparse.ArgumentParser(
        description="E-Commerce Data Engineering ETL Pipeline"
    )

    parser.add_argument(
        "--load-postgres",
        action="store_true",
        help="Load processed datasets into PostgreSQL"
    )

    args = parser.parse_args()

    try:
        run_pipeline(load_postgres=args.load_postgres)

    except Exception:
        logger.exception("ETL PIPELINE FAILED")
        raise


if __name__ == "__main__":
    main()
