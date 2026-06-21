import pandas as pd
import os

# ✅ Path
FILE_PATH = r"C:\Projects\BFSI C360\cbs\account_nominee.csv"


def fix_nominee_file():
    print("🔄 Reading account_nominee.csv...")

    df = pd.read_csv(FILE_PATH)

    print(f"✅ Columns before: {list(df.columns)}")

    # ✅ Remove column if exists
    if 'related_cif' in df.columns:
        df = df.drop(columns=['related_cif'])
        print("✅ 'related_cif' column removed")
    else:
        print("⚠️ 'related_cif' column not found")

    print(f"✅ Columns after: {list(df.columns)}")

    # ✅ Save file (overwrite)
    df.to_csv(
        FILE_PATH,
        index=False,
        lineterminator='\n',
        quoting=1,
        encoding='utf-8'
    )

    print("✅ File updated successfully!")


if __name__ == "__main__":
    fix_nominee_file()