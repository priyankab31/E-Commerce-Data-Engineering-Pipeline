# E-Commerce Data Engineering Pipeline

## Project Overview

An end-to-end E-Commerce Data Engineering project demonstrating
data extraction, transformation, data quality validation,
analytical processing and database loading.

The pipeline processes customer, product, order and payment
datasets to generate business-ready analytical datasets.

## Architecture

CSV Source Data
      |
      v
Python Data Extraction
      |
      v
Data Cleaning and Validation
      |
      v
Data Transformation and Joins
      |
      v
Business Metrics Generation
      |
      v
Processed CSV / PostgreSQL
      |
      v
SQL Business Analytics

## Technology Stack

- Python
- Pandas
- NumPy
- PostgreSQL
- SQLAlchemy
- SQL
- PyYAML
- Pytest
- Git and GitHub

## Project Structure

```text
ecommerce-data-engineering-pipeline/
├── config/
├── data/
│   ├── raw/
│   └── processed/
├── logs/
├── sql/
├── src/
├── tests/
├── main.py
├── requirements.txt
└── README.md
```

## Key Features

- Multi-source CSV data extraction
- Data cleaning and standardization
- Duplicate and missing-value checks
- Referential integrity validation
- Customer and product data enrichment
- Sales and revenue calculations
- Customer and product performance metrics
- PostgreSQL integration
- SQL analytical queries
- Automated unit testing
- Pipeline logging and error handling

## How to Run

### 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/ecommerce-data-engineering-pipeline.git

cd ecommerce-data-engineering-pipeline
```

### 2. Create a virtual environment

```bash
python -m venv .venv
```

### 3. Activate it

Windows:

```bash
.venv\Scripts\activate
```

### 4. Install dependencies

```bash
python -m pip install -r requirements.txt
```

### 5. Run the pipeline

```bash
python main.py
```

### 6. Run automated tests

```bash
python -m pytest -v
```

## PostgreSQL Integration

Set the DATABASE_URL environment variable before running:

```text
postgresql+psycopg2://username:password@localhost:5432/ecommerce_db
```

Windows PowerShell example:

```powershell
$env:DATABASE_URL="postgresql+psycopg2://username:password@localhost:5432/ecommerce_db"

python main.py --load-postgres
```

Never commit real credentials or passwords to GitHub.

## Generated Datasets

The pipeline produces:

- customers.csv
- products.csv
- orders.csv
- payments.csv
- sales.csv
- customer_metrics.csv
- product_metrics.csv

## Business Questions Answered

- What is the total revenue?
- Which products generate the most revenue?
- Who are the highest-value customers?
- How does revenue change month by month?
- Which cities generate the most sales?
- Are payments fully reconciled with order values?

## Future Enhancements

- PySpark distributed data processing
- Azure Data Factory orchestration
- Azure Databricks integration
- Azure Data Lake Storage
- Incremental loading and upsert logic
- Docker deployment
- CI/CD with GitHub Actions
- Power BI dashboard

## Data Privacy

All included records are fictional sample data.
No real customer or payment information is used.
