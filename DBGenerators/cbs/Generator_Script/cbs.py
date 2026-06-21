"""
CBS (Core Banking System) - MSSQL 100% Compatible Data Generator
All 10 tables with strict schema compliance and master table relationships
Production-ready for BULK INSERT into MSSQL Server
"""

import pandas as pd
import numpy as np
import random
from datetime import datetime, timezone, timedelta
import os

RANDOM_SEED = 42
CUSTOMER_COUNT = 100
ACCOUNTS_PER_CUSTOMER = 2.5

# ============================================================================
# MASTER TABLE DATA - STRICT SCHEMA (DO NOT CHANGE)
# ============================================================================

MASTER_DATA = {
    'gender': [
        ('GEN_M', 'Male'),
        ('GEN_F', 'Female'),
        ('GEN_O', 'Other'),
    ],
    'marital_status': [
        ('MS_SINGLE', 'Single'),
        ('MS_MARRIED', 'Married'),
        ('MS_DIV', 'Divorced'),
        ('MS_UNDISC', 'Undisclosed'),
    ],
    'occupation': [
        ('OCC_SAL', 'Salaried'),
        ('OCC_BUS', 'Business'),
        ('OCC_HOME', 'Homemaker'),
    ],
    'segment_code': [
        ('SEG_REG', 'REG'),
        ('SEG_HNI', 'HNI'),
        ('SEG_PEP', 'PEP'),
    ],
    'customer_status': [
        ('CUST_ACTIVE', 'Active'),
        ('CUST_INACTIVE', 'Inactive'),
    ],
    'nationality': [
        ('NAT_IND', 'Indian'),
        ('NAT_US', 'American'),
    ],
    'product_code': [
        ('PROD_SAV', 'Savings Account'),
        ('PROD_CUR', 'Current Account'),
        ('PROD_FD', 'Fixed Deposit'),
    ],
    'account_status': [
        ('ACC_ACTIVE', 'Active'),
        ('ACC_DORMANT', 'Dormant'),
        ('ACC_FROZEN', 'Frozen'),
        ('ACC_INACTIVE', 'Inactive'),
    ],
    'currency_code': [
        ('CUR_INR', 'INR'),
        ('CUR_USD', 'USD'),
        ('CUR_EUR', 'EUR'),
    ],
    'kyc_status': [
        ('KYC_INIT', 'Initiated'),
        ('KYC_PENDING', 'Pending'),
        ('KYC_DONE', 'Completed'),
    ],
    'risk_category': [
        ('RISK_LOW', 'Low'),
        ('RISK_MED', 'Medium'),
        ('RISK_HIGH', 'High'),
    ],
    'address_type': [
        ('ADDR_PERM', 'Permanent'),
        ('ADDR_COMM', 'Communication'),
    ],
    'branch_code': [
        ('BR001', 'Delhi Main Branch'),
        ('BR002', 'Mumbai Branch'),
        ('BR003', 'Bangalore Branch'),
    ],
}

CITIES_BY_BRANCH = {
    'BR001': ['Delhi', 'Gurgaon', 'Noida'],
    'BR002': ['Mumbai', 'Pune', 'Thane'],
    'BR003': ['Bangalore', 'Hyderabad', 'Chennai']
}

TXN_TYPES = ['UPI', 'NEFT', 'RTGS', 'CHEQUE', 'TRANSFER']
CHANNEL_CODES = ['MOBILE', 'BRANCH', 'ATM', 'NETBANKING', 'IVR']

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def to_utc_str(dt):
    """Convert datetime to UTC string YYYY-MM-DD HH:MM:SS"""
    if dt is None:
        return ''
    return dt.astimezone(timezone.utc).strftime('%Y-%m-%d %H:%M:%S')

def to_utc_date(dt):
    """Convert datetime to UTC date string YYYY-MM-DD"""
    if dt is None:
        return ''
    return dt.astimezone(timezone.utc).strftime('%Y-%m-%d')

def gen_cif(idx):
    """Generate CIF ID: CIF00000001 format"""
    return f"CIF{str(idx).zfill(8)}"

def gen_account_id(idx):
    """Generate Account ID: ACC00000001 format"""
    return f"ACC{str(idx).zfill(8)}"

def gen_account_number(idx):
    """Generate 10-digit account number"""
    return f"{str(1000000000 + idx)}"

# ============================================================================
# TABLE GENERATORS
# ============================================================================

def generate_master_table():
    """
    master_table - Reference data for all master codes
    Schema: id INT, type VARCHAR(50), code VARCHAR(50), value VARCHAR(100), 
            description VARCHAR(255), created_at DATETIME2, updated_at DATETIME2
    """
    print("Generating master_table...")
    records = []
    record_id = 1
    now = to_utc_str(datetime.now(timezone.utc))
    
    for master_type, entries in MASTER_DATA.items():
        for code, value in entries:
            records.append({
                'id': record_id,
                'type': master_type,
                'code': code,
                'value': value,
                'description': '',
                'created_at': now,
                'updated_at': now
            })
            record_id += 1
    
    return pd.DataFrame(records)

def generate_customer_master():
    """
    customer_master - Core customer data
    Schema: cif, customer_type, first_name, middle_name, last_name, date_of_birth,
            gender, marital_status, nationality, occupation_code, segment_code,
            customer_status, customer_since_date, branch_code, created_at, updated_at
    """
    print("Generating customer_master...")
    records = []
    now = to_utc_str(datetime.now(timezone.utc))
    
    first_names = ['Manikya', 'Dhruv', 'Aarav', 'Vivaan', 'Arjun', 'Ravi', 'Amit', 'Rahul',
                   'Ananya', 'Priya', 'Neha', 'Sarika', 'Pooja', 'Kavya', 'Nisha']
    last_names = ['Jani', 'Sood', 'Kumar', 'Singh', 'Gupta', 'Sharma', 'Patel', 'Verma',
                  'Iyer', 'Nair', 'Wadhwa', 'Vasa', 'Reddy', 'Desai', 'Kulkarni']
    
    gender_codes = [x[0] for x in MASTER_DATA['gender']]
    marital_codes = [x[0] for x in MASTER_DATA['marital_status']]
    occupation_codes = [x[0] for x in MASTER_DATA['occupation']]
    segment_codes = [x[0] for x in MASTER_DATA['segment_code']]
    nationality_codes = [x[0] for x in MASTER_DATA['nationality']]
    branch_codes = [x[0] for x in MASTER_DATA['branch_code']]
    
    for idx in range(1, CUSTOMER_COUNT + 1):
        cif = gen_cif(idx)
        dob = datetime.now(timezone.utc) - timedelta(days=random.randint(7300, 27000))
        customer_since = datetime.now(timezone.utc) - timedelta(days=random.randint(365, 1095))
        
        records.append({
            'cif': cif,
            'customer_type': 'INDIVIDUAL',
            'first_name': random.choice(first_names),
            'middle_name': '',
            'last_name': random.choice(last_names),
            'date_of_birth': to_utc_date(dob),
            'gender': random.choice(gender_codes),
            'marital_status': random.choice(marital_codes),
            'nationality': random.choice(nationality_codes),
            'occupation_code': random.choice(occupation_codes),
            'segment_code': random.choice(segment_codes),
            'customer_status': 'CUST_ACTIVE',
            'customer_since_date': to_utc_date(customer_since),
            'branch_code': random.choice(branch_codes),
            'created_at': now,
            'updated_at': now
        })
    
    return pd.DataFrame(records)

def generate_customer_address(df_customers):
    """
    customer_address - Customer address records
    Schema: address_id, cif, address_type, address_line1, address_line2,
            city, state, country, postal_code, is_primary, created_at, updated_at
    """
    print("Generating customer_address...")
    records = []
    address_id = 1
    now = to_utc_str(datetime.now(timezone.utc))
    address_type_codes = [x[0] for x in MASTER_DATA['address_type']]
    
    for idx, customer in df_customers.iterrows():
        branch_code = customer['branch_code']
        cities = CITIES_BY_BRANCH.get(branch_code, ['Delhi', 'Mumbai', 'Bangalore'])
        
        for addr_type in address_type_codes:
            records.append({
                'address_id': f"ADDR{str(address_id).zfill(8)}",
                'cif': customer['cif'],
                'address_type': addr_type,
                'address_line1': 'Street Area',
                'address_line2': '',
                'city': random.choice(cities),
                'state': random.choice(cities),
                'country': 'India',
                'postal_code': str(random.randint(100000, 999999)),
                'is_primary': 'Y',
                'created_at': now,
                'updated_at': now
            })
            address_id += 1
    
    return pd.DataFrame(records)

def generate_customer_contact(df_customers):
    """
    customer_contact - Customer contact information
    Schema: contact_id, cif, mobile_number, email_id, alternate_mobile,
            landline_number, is_primary, verified_flag, created_at, updated_at
    """
    print("Generating customer_contact...")
    records = []
    contact_id = 1
    now = to_utc_str(datetime.now(timezone.utc))
    
    for idx, customer in df_customers.iterrows():
        records.append({
            'contact_id': f"CONT{str(contact_id).zfill(8)}",
            'cif': customer['cif'],
            'mobile_number': str(random.randint(6000000000, 9999999999)),
            'email_id': f"user{random.randint(1000, 9999)}@mail.com",
            'alternate_mobile': '',
            'landline_number': '',
            'is_primary': 'Y',
            'verified_flag': 'Y',
            'created_at': now,
            'updated_at': now
        })
        contact_id += 1
    
    return pd.DataFrame(records)

def generate_customer_kyc_reference(df_customers):
    """
    customer_kyc_reference - KYC compliance tracking
    Schema: kyc_ref_id, cif, kyc_status, risk_category,
            kyc_last_updated_date, kyc_expiry_date
    """
    print("Generating customer_kyc_reference...")
    records = []
    kyc_id = 1
    risk_codes = [x[0] for x in MASTER_DATA['risk_category']]
    
    for idx, customer in df_customers.iterrows():
        kyc_update_date = datetime.now(timezone.utc) - timedelta(days=random.randint(1, 30))
        kyc_expiry_date = kyc_update_date + timedelta(days=365)
        
        records.append({
            'kyc_ref_id': f"KYC{str(kyc_id).zfill(8)}",
            'cif': customer['cif'],
            'kyc_status': 'KYC_DONE',
            'risk_category': random.choice(risk_codes),
            'kyc_last_updated_date': to_utc_date(kyc_update_date),
            'kyc_expiry_date': to_utc_date(kyc_expiry_date)
        })
        kyc_id += 1
    
    return pd.DataFrame(records)

def generate_account_master(df_customers):
    """
    account_master - Account information
    Schema: account_id, account_number, product_code, branch_code, account_type,
            account_status, currency_code, open_date, close_date, rm_id,
            created_at, updated_at
    """
    print("Generating account_master...")
    records = []
    account_id = 1
    now = to_utc_str(datetime.now(timezone.utc))
    
    product_codes = [x[0] for x in MASTER_DATA['product_code']]
    account_status_codes = [x[0] for x in MASTER_DATA['account_status']]
    
    for idx, customer in df_customers.iterrows():
        num_accounts = random.choices([1, 2, 3], weights=[40, 45, 15], k=1)[0]
        
        for _ in range(num_accounts):
            open_date = datetime.now(timezone.utc) - timedelta(days=random.randint(30, 730))
            close_date = open_date + timedelta(days=365) if random.random() > 0.9 else None
            
            records.append({
                'account_id': gen_account_id(account_id),
                'account_number': gen_account_number(account_id),
                'product_code': random.choice(product_codes),
                'branch_code': customer['branch_code'],
                'account_type': random.choice(['SAVINGS', 'CURRENT', 'FIXED_DEPOSIT']),
                'account_status': random.choices(account_status_codes, weights=[85, 5, 5, 5], k=1)[0],
                'currency_code': 'CUR_INR',
                'open_date': to_utc_date(open_date),
                'close_date': to_utc_date(close_date) if close_date else '',
                'rm_id': f"RM{str(random.randint(1, 100)).zfill(8)}",
                'created_at': now,
                'updated_at': now
            })
            account_id += 1
    
    return pd.DataFrame(records)

def generate_account_balance(df_accounts):
    """
    account_balance - Account balance snapshot
    Schema: balance_id, account_id, ledger_balance, available_balance,
            lien_amount, hold_amount, last_updated_timestamp
    """
    print("Generating account_balance...")
    records = []
    now = to_utc_str(datetime.now(timezone.utc))
    
    for idx, account in df_accounts.iterrows():
        ledger_balance = round(random.uniform(-50000, 500000), 2)
        available_balance = round(ledger_balance - random.uniform(0, 10000), 2)
        lien_amount = round(random.uniform(0, 5000), 2) if random.random() > 0.8 else 0
        hold_amount = round(random.uniform(0, 5000), 2) if random.random() > 0.8 else 0
        
        records.append({
            'balance_id': f"BAL{str(idx + 1).zfill(8)}",
            'account_id': account['account_id'],
            'ledger_balance': ledger_balance,
            'available_balance': available_balance,
            'lien_amount': lien_amount,
            'hold_amount': hold_amount,
            'last_updated_timestamp': now
        })
    
    return pd.DataFrame(records)

def generate_account_customer_mapping(df_customers, df_accounts):
    """
    account_customer_mapping - Maps customers to accounts
    Schema: cif, account_id
    """
    print("Generating account_customer_mapping...")
    records = []
    
    for idx, account in df_accounts.iterrows():
        customer = df_customers.sample(1, random_state=RANDOM_SEED).iloc[0]
        records.append({
            'cif': customer['cif'],
            'account_id': account['account_id']
        })
    
    return pd.DataFrame(records).drop_duplicates()

def generate_account_nominee(df_accounts):
    """
    account_nominee - Nominee information for accounts
    Schema: relationship_id, account_id, related_cif, relationship_type,
            share_percentage, nominee_name, nominee_dob, guardian_name, guardian_dob
    """
    print("Generating account_nominee...")
    records = []
    relationship_id = 1
    
    first_names = ['Kavya', 'Tushar', 'Asha', 'Rajesh', 'Pooja', 'Aryan', 'Nisha', 'Vikram']
    last_names = ['Wadhwa', 'Vasa', 'Joshi', 'Kumar', 'Singh', 'Sharma', 'Patel', 'Verma']
    relationships = ['NOMINEE', 'SPOUSE', 'CHILD', 'PARENT']
    
    for idx, account in df_accounts.iterrows():
        if random.random() > 0.2:
            nominee_dob = datetime.now(timezone.utc) - timedelta(days=random.randint(3650, 27000))
            guardian_dob = datetime.now(timezone.utc) - timedelta(days=random.randint(10950, 27000)) if random.random() > 0.5 else None
            
            records.append({
                'relationship_id': f"REL{str(relationship_id).zfill(8)}",
                'account_id': account['account_id'],
                'relationship_type': random.choice(relationships),
                'share_percentage': 100.0,
                'nominee_name': f"{random.choice(first_names)} {random.choice(last_names)}",
                'nominee_dob': to_utc_date(nominee_dob),
                'guardian_name': f"{random.choice(first_names)} {random.choice(last_names)}" if random.random() > 0.5 else '',
                'guardian_dob': to_utc_date(guardian_dob) if guardian_dob else ''
            })
            relationship_id += 1
    
    return pd.DataFrame(records)

def generate_transaction_ledger(df_accounts):
    """
    transaction_ledger - Account transactions
    Schema: txn_id, account_id, txn_reference_no, txn_date, txn_type,
            dr_cr_flag, amount, balance_after_txn, channel_code,
            narration, counterparty_reference
    """
    print("Generating transaction_ledger...")
    records = []
    txn_id = 1
    
    for account_idx, account in df_accounts.iterrows():
        num_txns = random.randint(3, 10)
        
        for txn_num in range(num_txns):
            txn_date = datetime.now(timezone.utc) - timedelta(days=random.randint(1, 90))
            dr_cr = random.choice(['DR', 'CR'])
            amount = round(random.uniform(100, 50000), 2)
            
            records.append({
                'txn_id': f"TXN{str(txn_id).zfill(8)}",
                'account_id': account['account_id'],
                'txn_reference_no': f"{str(txn_id).zfill(6)}",
                'txn_date': to_utc_str(txn_date),
                'txn_type': random.choice(TXN_TYPES),
                'dr_cr_flag': dr_cr,
                'amount': amount,
                'balance_after_txn': round(random.uniform(-50000, 500000), 2),
                'channel_code': random.choice(CHANNEL_CODES),
                'narration': 'TXN',
                'counterparty_reference': f"S{str(txn_id).zfill(6)}"
            })
            txn_id += 1
    
    return pd.DataFrame(records)

# ============================================================================
# FILE OPERATIONS
# ============================================================================

def create_output_directory():
    """Create output directory"""
    base_path = os.path.join(os.getcwd(), 'Generated_Data', 'cbs')
    os.makedirs(base_path, exist_ok=True)
    print(f"✓ Created directory: {base_path}\n")
    return base_path

def export_to_csv(df, table_name, output_path):
    """
    Export DataFrame to CSV with MSSQL BULK INSERT compatibility
    - UTF-8 encoding
    - Comma separator
    - NULL as empty string
    - Proper quoting
    """
    filepath = os.path.join(output_path, f'{table_name}.csv')
    
    df = df.fillna('').convert_dtypes()
    df.to_csv(
        filepath,
        index=False,
        encoding='utf-8',
        sep=',',
        quoting=1,
        lineterminator='\n'
    )
    
    row_count = len(df)
    file_size = os.path.getsize(filepath) / 1024
    print(f"✓ Exported: {table_name:35} | Rows: {row_count:6} | Size: {file_size:8.2f} KB")
    
    return filepath

# ============================================================================
# VALIDATION
# ============================================================================

def validate_foreign_keys(df_customers, df_accounts, df_addresses, df_contacts, 
                          df_kyc, df_balances, df_mapping, df_nominees, df_transactions):
    """Validate all foreign key relationships"""
    print("\n--- Foreign Key Validation ---")
    
    valid = True
    
    all_cifs = set(df_customers['cif'].unique())
    all_accounts = set(df_accounts['account_id'].unique())
    
    if not df_addresses['cif'].isin(all_cifs).all():
        print("✗ ERROR: customer_address.cif → customer_master.cif")
        valid = False
    else:
        print("✓ customer_address.cif → customer_master.cif")
    
    if not df_contacts['cif'].isin(all_cifs).all():
        print("✗ ERROR: customer_contact.cif → customer_master.cif")
        valid = False
    else:
        print("✓ customer_contact.cif → customer_master.cif")
    
    if not df_kyc['cif'].isin(all_cifs).all():
        print("✗ ERROR: customer_kyc_reference.cif → customer_master.cif")
        valid = False
    else:
        print("✓ customer_kyc_reference.cif → customer_master.cif")
    
    if not df_balances['account_id'].isin(all_accounts).all():
        print("✗ ERROR: account_balance.account_id → account_master.account_id")
        valid = False
    else:
        print("✓ account_balance.account_id → account_master.account_id")
    
    if not df_mapping['account_id'].isin(all_accounts).all():
        print("✗ ERROR: account_customer_mapping.account_id → account_master.account_id")
        valid = False
    else:
        print("✓ account_customer_mapping.account_id → account_master.account_id")
    
    if not df_nominees['account_id'].isin(all_accounts).all():
        print("✗ ERROR: account_nominee.account_id → account_master.account_id")
        valid = False
    else:
        print("✓ account_nominee.account_id → account_master.account_id")
    
    if not df_transactions['account_id'].isin(all_accounts).all():
        print("✗ ERROR: transaction_ledger.account_id → account_master.account_id")
        valid = False
    else:
        print("✓ transaction_ledger.account_id → account_master.account_id")
    
    return valid

# ============================================================================
# MAIN EXECUTION
# ============================================================================

def main():
    print("=" * 90)
    print("CBS (CORE BANKING SYSTEM) - MSSQL 100% COMPATIBLE DATA GENERATOR")
    print("=" * 90)
    
    random.seed(RANDOM_SEED)
    np.random.seed(RANDOM_SEED)
    
    output_path = create_output_directory()
    
    print("--- Generating Tables ---\n")
    
    df_master = generate_master_table()
    df_customers = generate_customer_master()
    df_addresses = generate_customer_address(df_customers)
    df_contacts = generate_customer_contact(df_customers)
    df_kyc = generate_customer_kyc_reference(df_customers)
    df_accounts = generate_account_master(df_customers)
    df_balances = generate_account_balance(df_accounts)
    df_mapping = generate_account_customer_mapping(df_customers, df_accounts)
    df_nominees = generate_account_nominee(df_accounts)
    df_transactions = generate_transaction_ledger(df_accounts)
    
    print("\n--- Exporting to CSV (MSSQL Compatible) ---\n")
    
    export_to_csv(df_master, 'master_table', output_path)
    export_to_csv(df_customers, 'customer_master', output_path)
    export_to_csv(df_addresses, 'customer_address', output_path)
    export_to_csv(df_contacts, 'customer_contact', output_path)
    export_to_csv(df_kyc, 'customer_kyc_reference', output_path)
    export_to_csv(df_accounts, 'account_master', output_path)
    export_to_csv(df_balances, 'account_balance', output_path)
    export_to_csv(df_mapping, 'account_customer_mapping', output_path)
    export_to_csv(df_nominees, 'account_nominee', output_path)
    export_to_csv(df_transactions, 'transaction_ledger', output_path)
    
    print("\n--- Data Quality Summary ---\n")
    print(f"Master Table Records:              {len(df_master):6}")
    print(f"Customers:                         {len(df_customers):6}")
    print(f"Customer Addresses:                {len(df_addresses):6}")
    print(f"Customer Contacts:                 {len(df_contacts):6}")
    print(f"Customer KYC:                      {len(df_kyc):6}")
    print(f"Accounts:                          {len(df_accounts):6}")
    print(f"Account Balances:                  {len(df_balances):6}")
    print(f"Customer-Account Mapping:          {len(df_mapping):6}")
    print(f"Account Nominees:                  {len(df_nominees):6}")
    print(f"Transactions:                      {len(df_transactions):6}")
    print(f"\nTotal Records:                     {len(df_master) + len(df_customers) + len(df_addresses) + len(df_contacts) + len(df_kyc) + len(df_accounts) + len(df_balances) + len(df_mapping) + len(df_nominees) + len(df_transactions):6}")
    
    print(f"\nAccounts per Customer:             {len(df_accounts) / len(df_customers):.2f}")
    print(f"Transactions per Account:          {len(df_transactions) / len(df_accounts):.2f}")
    
    valid = validate_foreign_keys(df_customers, df_accounts, df_addresses, df_contacts, 
                                   df_kyc, df_balances, df_mapping, df_nominees, df_transactions)
    
    print("\n" + "=" * 90)
    if valid:
        print("✓ ALL DATA GENERATED SUCCESSFULLY - READY FOR MSSQL BULK INSERT")
    else:
        print("✗ VALIDATION ERRORS - PLEASE CHECK OUTPUT ABOVE")
    print("=" * 90)
    
    print(f"\nOutput Location: {output_path}")
    print("\nMSSQL BULK INSERT Example:")
    print("BULK INSERT cbs.master_table")
    print("FROM 'C:\\path\\to\\master_table.csv'")
    print("WITH (FIELDTERMINATOR=',', ROWTERMINATOR='\\n', FIRSTROW=2, CODEPAGE='65001');")
    print("\n" + "=" * 90)

if __name__ == "__main__":
    main()
