import pandas as pd
import os

# ✅ ✅ UPDATED BASE PATH
BASE_PATH = r"C:\Projects\BFSI C360\cbs"


def load_csv(file):
    path = os.path.join(BASE_PATH, file)
    return pd.read_csv(path)


def check_exists(child_df, parent_df, child_col, parent_col, check_name):
    print(f"\n🔍 {check_name}")

    missing = child_df[~child_df[child_col].isin(parent_df[parent_col])]

    if len(missing) == 0:
        print(f"✅ PASS: All values in '{child_col}' are valid")
    else:
        print(f"❌ FAIL: {len(missing)} invalid records found")
        print(missing[[child_col]].head(5))


def check_uniqueness(df, col, name):
    duplicates = df[col].duplicated()

    if duplicates.any():
        print(f"❌ FAIL: Duplicate values in {name}")
    else:
        print(f"✅ PASS: Unique values in {name}")


def check_nulls(df, name):
    nulls = df.isnull().sum().sum()

    if nulls > 0:
        print(f"⚠️ WARNING: {nulls} null values found in {name}")
    else:
        print(f"✅ PASS: No nulls in {name}")


def main():
    print("\n🚀 STARTING RELATIONAL DATA VALIDATION\n")

    # ✅ Load tables from NEW PATH
    customer = load_csv("customer_master.csv")
    account = load_csv("account_master.csv")
    mapping = load_csv("account_customer_mapping.csv")
    nominee = load_csv("account_nominee.csv")
    transaction = load_csv("transaction_ledger.csv")
    balance = load_csv("account_balance.csv")
    kyc = load_csv("customer_kyc_reference.csv")  # ✅ NEW FILE INCLUDED

    print("✅ All files loaded\n")

    # =========================================================
    # ✅ 1. PRIMARY KEY VALIDATION
    # =========================================================
    print("\n======== PRIMARY KEY VALIDATION ========")

    check_uniqueness(customer, "cif", "customer_master.cif")
    check_uniqueness(account, "account_id", "account_master.account_id")

    # =========================================================
    # ✅ 2. ACCOUNT ↔ CUSTOMER RELATION
    # =========================================================
    print("\n======== ACCOUNT-CUSTOMER MAPPING ========")

    check_exists(mapping, account, "account_id", "account_id",
                 "Mapping → Account Master")

    check_exists(mapping, customer, "cif", "cif",
                 "Mapping → Customer Master")

    print("\n🔍 Distribution Check (Accounts per CIF):")
    dist = mapping['cif'].value_counts()
    print(dist.describe())

    # =========================================================
    # ✅ 3. ACCOUNT-DEPENDENT TABLES
    # =========================================================
    print("\n======== ACCOUNT-BASED TABLES ========")

    check_exists(balance, account, "account_id", "account_id",
                 "Balance → Account Master")

    check_exists(transaction, account, "account_id", "account_id",
                 "Transaction → Account Master")

    check_exists(nominee, account, "account_id", "account_id",
                 "Nominee → Account Master")

    # =========================================================
    # ✅ 4. CUSTOMER-DEPENDENT TABLES
    # =========================================================
    print("\n======== CUSTOMER-BASED TABLES ========")

    check_exists(kyc, customer, "cif", "cif",
                 "KYC → Customer Master")

    # =========================================================
    # ✅ 5. ORPHAN CHECK
    # =========================================================
    print("\n======== ORPHAN RECORD CHECK ========")

    orphan_accounts = account[~account['account_id'].isin(mapping['account_id'])]

    if len(orphan_accounts) == 0:
        print("✅ PASS: All accounts mapped to customers")
    else:
        print(f"❌ FAIL: {len(orphan_accounts)} unmapped accounts")
        print(orphan_accounts.head(5))

    orphan_customers = customer[~customer['cif'].isin(mapping['cif'])]
    print(f"ℹ️ Customers without accounts: {len(orphan_customers)}")

    # =========================================================
    # ✅ 6. DUPLICATES
    # =========================================================
    print("\n======== DUPLICATE CHECK ========")

    print(f"Mapping duplicates: {mapping.duplicated().sum()}")
    print(f"Transactions duplicates: {transaction.duplicated().sum()}")

    # =========================================================
    # ✅ 7. NULL CHECKS
    # =========================================================
    print("\n======== NULL CHECK ========")

    check_nulls(mapping, "Mapping Table")
    check_nulls(nominee, "Nominee Table")
    check_nulls(transaction, "Transaction Table")
    check_nulls(kyc, "KYC Table")

    # =========================================================
    # ✅ 8. SANITY CHECK
    # =========================================================
    print("\n======== SANITY CHECK ========")

    print(f"Total Customers: {len(customer)}")
    print(f"Total Accounts: {len(account)}")
    print(f"Total Mappings: {len(mapping)}")

    if len(mapping) == len(account):
        print("✅ PASS: Each account has mapping")
    else:
        print("⚠️ WARNING: Mapping count mismatch")

    print("\n✅ ✅ VALIDATION COMPLETE ✅ ✅")


if __name__ == "__main__":
    main()
