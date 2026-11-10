from src.logger import get_logger

logger = get_logger(__name__)


def check_required_columns(df, required_columns, dataset_name):
    missing = set(required_columns) - set(df.columns)

    if missing:
        raise ValueError(
            f"{dataset_name} is missing columns: {sorted(missing)}"
        )

    logger.info("%s: required column check passed", dataset_name)


def check_duplicates(df, column, dataset_name):
    duplicates = df[column].duplicated().sum()

    if duplicates > 0:
        logger.warning(
            "%s contains %d duplicate values in %s",
            dataset_name,
            duplicates,
            column
        )

    return duplicates


def check_missing_values(df, dataset_name):
    missing = df.isnull().sum()
    missing = missing[missing > 0]

    if not missing.empty:
        logger.warning(
            "%s contains missing values: %s",
            dataset_name,
            missing.to_dict()
        )
    else:
        logger.info("%s: no missing values found", dataset_name)

    return missing.to_dict()
