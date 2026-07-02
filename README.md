# Relational Data Validation & ETL Integrity Framework

A production-ready data quality engine built with **Python**, **Pandas**, and **MySQL (XAMPP)** designed to audit relational datasets, automate constraint checking, and verify pipeline accuracy prior to downstream analytical ingestion.

## 🚀 Key Features Evaluated
* **Primary Key Audit:** Scans transaction schemas to isolate and flag duplicate record entities.
* **Referential Integrity Enforcement:** Executes automated `LEFT JOIN` operations to identify orphaned relational rows (Foreign Key validation failures).
* **Automated Data Quality Reporting:** Emits real-time terminal diagnostics detailing exact failure tables and specific row index metrics.

## 🛠️ Project Structure
```text
db_validation_framework/
├── data/                  # Source CSV payloads (Clean & Intentionally Faulty)
├── sql/
│   └── schema.sql         # Database structures & integrity layers
├── scripts/
│   └── validation_engine.py  # Automation validation framework
├── requirements.txt       # Core dependencies
└── README.md              # Documentation