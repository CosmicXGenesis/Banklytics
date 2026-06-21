import pandas as pd
from DataPipeline.Utils.db_connection import get_connection
import pyodbc
from pathlib import Path

# ==========================================================
# CONFIGURATION
# ==========================================================

CSV_DIR = Path(r"C:\Projects\BFSI C360\cbs")

TABLES = [
    "cbs_account_balance",
    "cbs_account_customer_mapping",
    "cbs_account_master",
    "cbs_account_nominee",
    "cbs_customer_address",
    "cbs_customer_contact",
    "cbs_customer_kyc_reference",
    "cbs_customer_master",
    "cbs_master_table",
    "cbs_transaction_ledger"
]

# ==========================================================
# DATABASE CONNECTION
# ==========================================================

print("Connecting to SQL Server...")


conn = get_connection()

cursor = conn.cursor()

print("Connected Successfully")

# ==========================================================
# INGESTION
# ==========================================================

for table_name in TABLES:

    csv_file = CSV_DIR / f"{table_name}.csv"

    print("\n" + "=" * 70)
    print(f"Processing : {table_name}")
    print("=" * 70)

    if not csv_file.exists():
        print(f"CSV NOT FOUND : {csv_file}")
        continue

    try:

        df = pd.read_csv(csv_file)

        print(f"Rows Found : {len(df)}")

        # Convert NaN -> None
        df = df.astype(object)
        df = df.where(pd.notnull(df), None)

        columns = ",".join(df.columns)
        placeholders = ",".join(["?"] * len(df.columns))

        insert_sql = f"""
        INSERT INTO {table_name}
        ({columns})
        VALUES ({placeholders})
        """

        inserted = 0

        for row in df.itertuples(index=False):

            try:
                cursor.execute(insert_sql, tuple(row))
                inserted += 1

            except Exception as row_error:
                print(f"\nFAILED ROW IN {table_name}")
                print(row)
                print(row_error)
                raise

        conn.commit()

        print(f"SUCCESS : {inserted} rows inserted")

    except Exception as e:

        conn.rollback()

        print(f"FAILED : {table_name}")
        print(str(e))

# ==========================================================
# VALIDATION
# ==========================================================

print("\n")
print("=" * 70)
print("ROW COUNT VALIDATION")
print("=" * 70)

for table_name in TABLES:

    cursor.execute(
        f"SELECT COUNT(*) FROM {table_name}"
    )

    count = cursor.fetchone()[0]

    print(f"{table_name:<35} {count}")

# ==========================================================
# CLEANUP
# ==========================================================

cursor.close()
conn.close()

print("\nCBS Batch Load Completed")