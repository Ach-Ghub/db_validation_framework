import pandas as pd
from sqlalchemy import create_engine, text

import os

# If running inside Docker, use the environment variable; otherwise, fallback to local XAMPP
DATABASE_URL = os.getenv("DATABASE_URL", "mysql+pymysql://root:@localhost:3306/db_ecomerce_etl")
engine = create_engine(DATABASE_URL)

def generate_dashboard():
    print("=" * 60)
    print("📊 DATA GOVERNANCE & QUALITY HISTORICAL REPORT")
    print("=" * 60)
    
    # Query to aggregate our database log history
    query = text("""
        SELECT 
            target_table AS 'Table',
            check_type AS 'Audit Type',
            COUNT(*) AS 'Total Runs',
            SUM(failures_detected) AS 'Cumulative Failures',
            ROUND(AVG(failures_detected), 2) AS 'Avg Failures/Run',
            MAX(run_timestamp) AS 'Last Audit Timestamp'
        FROM data_quality_logs
        GROUP BY target_table, check_type;
    """)
    
    with engine.connect() as connection:
        df_report = pd.read_sql(query, con=connection)
        
    if not df_report.empty:
        print(df_report.to_string(index=False))
    else:
        print("⚠️ No data logs found. Run validation_engine.py first!")
        
    print("\n" + "=" * 60)

if __name__ == "__main__":
    generate_dashboard()