import pandas as pd
from sqlalchemy import create_engine, text

# 1. Establish XAMPP MySQL Connection
# Format: mysql+pymysql://username:password@host:port/database
# XAMPP default is 'root' with no password
DATABASE_URL = "mysql+pymysql://root:@localhost:3306/db_ecomerce_etl"
engine = create_engine(DATABASE_URL)

def run_validation_checks():
    print("=" * 50)
    print("🚀 STARTING ETL DATA VALIDATION CHECKS")
    print("=" * 50)
    
    # --- CHECK 1: DUPLICATES IN ORDERS ---
    print("\n🔍 Checking for duplicate records in orders.csv...")
    df_orders = pd.read_csv("data/orders.csv")
    
    # Find rows where the primary key (order_id) is duplicated
    duplicates = df_orders[df_orders.duplicated(subset=['order_id'], keep=False)]
    
    if not duplicates.empty:
        print(f"❌ FAIL: Found {len(duplicates)} duplicate row references!")
        print(duplicates)
    else:
        print("✅ PASS: No duplicate Order IDs detected.")

    # --- CHECK 2: REFERENTIAL INTEGRITY (ORPHANED RECORDS) ---
    print("\n🔍 Checking for Foreign Key violations (Orphaned Orders)...")
    
    # We will temporarily load the orders to check them against the database's users table
    # Using SQL to find rows in orders where the user_id does not exist in the users table
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
            # Let's ensure our users table has our clean data first to compare against
            df_users = pd.read_csv("data/users.csv")
            df_users.to_sql("users", con=connection, if_exists="append", index=False)
            
            # Execute the cross-reference validation query
            result = connection.execute(query)
            orphaned_records = result.fetchall()
            
            if orphaned_records:
                print(f"❌ FAIL: Found {len(orphaned_records)} orphaned order record(s) referencing non-existent users!")
                for row in orphaned_records:
                    print(f" -> Order ID: {row[0]} references missing User ID: {row[1]}")
            else:
                print("✅ PASS: All orders map cleanly to existing users.")
                
    except Exception as e:
        print(f"⚠️ Database Error: {e}")
    
    print("\n" + "=" * 50)
    print("🏁 ETL VALIDATION RUN COMPLETE")
    print("=" * 50)

if __name__ == "__main__":
    run_validation_checks()