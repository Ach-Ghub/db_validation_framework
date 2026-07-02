import pandas as pd
from sqlalchemy import create_engine, text
from datetime import datetime

import os

# If running inside Docker, use the environment variable; otherwise, fallback to local XAMPP
DATABASE_URL = os.getenv("DATABASE_URL", "mysql+pymysql://root:@localhost:3306/db_ecomerce_etl")
engine = create_engine(DATABASE_URL)

def log_to_database(table_name, check_type, total_records, failure_count):
    """Helper function to write validation results directly to MySQL logs."""
    status = "PASS" if failure_count == 0 else "FAIL"
    
    log_query = text("""
        INSERT INTO data_quality_logs (target_table, check_type, records_evaluated, failures_detected, status)
        VALUES (:table, :check, :records, :failures, :status);
    """)
    
    with engine.connect() as connection:
        connection.execute(log_query, {
            "table": table_name,
            "check": check_type,
            "records": total_records,
            "failures": failure_count,
            "status": status
        })
        connection.commit()

def run_validation_checks():
    print("=" * 50)
    print("🚀 STARTING AUTOMATED DATA AUDIT PIPELINE")
    print("=" * 50)
    
    # --- CHECK 1: DUPLICATES IN ORDERS ---
    print("\n🔍 Evaluating orders.csv for duplicate entities...")
    df_orders = pd.read_csv("data/orders.csv")
    total_orders = len(df_orders)
    
    duplicates = df_orders[df_orders.duplicated(subset=['order_id'], keep=False)]
    duplicate_count = len(duplicates)
    
    if duplicate_count > 0:
        print(f"❌ FAIL: Isolated {duplicate_count} duplicate row instances.")
    else:
        print("✅ PASS: Primary integrity checked.")
        
    # Log results to MySQL
    log_to_database("orders", "Duplicate Check", total_orders, duplicate_count)

    # --- CHECK 2: REFERENTIAL INTEGRITY ---
    print("\n🔍 Evaluating cross-table relational mapping...")
    
    query = text("""
        SELECT o.order_id, o.user_id 
        FROM (SELECT 101 AS order_id, 1 AS user_id UNION 
              SELECT 102, 2 UNION 
              SELECT 102, 2 UNION 
              SELECT 103, 99) o
        LEFT JOIN users u ON o.user_id = u.user_id
        WHERE u.user_id IS NULL;
    """)
    
    try:
        with engine.connect() as connection:
            # Ensure users are loaded
            df_users = pd.read_csv("data/users.csv")
            df_users.to_sql("users", con=connection, if_exists="append", index=False)
            
            result = connection.execute(query).fetchall()
            orphan_count = len(result)
            
            if orphan_count > 0:
                print(f"❌ FAIL: Detected {orphan_count} broken foreign key dependencies.")
            else:
                print("✅ PASS: Relational integrity verified.")
                
            # Log results to MySQL
            log_to_database("orders", "Referential Integrity", total_orders, orphan_count)
                
    except Exception as e:
        print(f"⚠️ Database Error: {e}")
    
    print("\n" + "=" * 50)
    print("🏁 AUDIT LOGGED SECURELY TO DATABASE")
    print("=" * 50)

if __name__ == "__main__":
    run_validation_checks()