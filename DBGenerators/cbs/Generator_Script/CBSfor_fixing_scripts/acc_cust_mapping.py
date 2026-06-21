import pandas as pd
import random
import os

# ✅ Paths
BASE_PATH = r"C:\Projects\BFSI C360\cbs"

CUSTOMER_FILE = os.path.join(BASE_PATH, "customer_master.csv")
ACCOUNT_FILE = os.path.join(BASE_PATH, "account_master.csv")
OUTPUT_FILE = os.path.join(BASE_PATH, "account_customer_mapping.csv")


def generate_mapping():
    print("🔄 Reading input files...")

    customer_df = pd.read_csv(CUSTOMER_FILE)
    account_df = pd.read_csv(ACCOUNT_FILE)

    customers = customer_df['cif'].tolist()
    accounts = account_df['account_id'].tolist()

    print(f"✅ Customers: {len(customers)}")
    print(f"✅ Accounts : {len(accounts)}")

    print("🔄 Creating realistic distribution...")

    # Shuffle
    random.shuffle(customers)
    random.shuffle(accounts)

    # Distribution (realistic)
    distribution = [1]*70 + [2]*20 + [3]*10

    mapping_data = []
    acc_index = 0

    for cif in customers:
        if acc_index >= len(accounts):
            break

        num_accounts = random.choice(distribution)

        for _ in range(num_accounts):
            if acc_index >= len(accounts):
                break

            # ✅ ONLY 2 columns now
            mapping_data.append({
                'account_id': accounts[acc_index],
                'cif': cif
            })

            acc_index += 1

    # Cover remaining accounts
    while acc_index < len(accounts):
        cif = random.choice(customers)

        mapping_data.append({
            'account_id': accounts[acc_index],
            'cif': cif
        })

        acc_index += 1

    mapping_df = pd.DataFrame(mapping_data)

    print("🔄 Saving CSV...")

    mapping_df.to_csv(
        OUTPUT_FILE,
        index=False,
        lineterminator='\n',
        quoting=1,
        encoding='utf-8'
    )

    print(f"✅ SUCCESS: Created {OUTPUT_FILE}")
    print(f"✅ Total mappings: {len(mapping_df)}")


if __name__ == "__main__":
    generate_mapping()