
/* MSSQL schema derived from actual CSV profiling */

CREATE TABLE cbs_account_balance (
 balance_id VARCHAR(20) NOT NULL PRIMARY KEY,
 account_id VARCHAR(20) NOT NULL,
 ledger_balance DECIMAL(18,2) NOT NULL,
 available_balance DECIMAL(18,2) NOT NULL,
 lien_amount DECIMAL(18,2) NOT NULL,
 hold_amount DECIMAL(18,2) NOT NULL,
 last_updated_timestamp DATETIME2 NOT NULL
);

CREATE TABLE cbs_account_customer_mapping (
 account_id VARCHAR(20) NOT NULL,
 cif VARCHAR(20) NOT NULL,
 CONSTRAINT PK_account_customer_mapping PRIMARY KEY (account_id)
);

CREATE TABLE cbs_account_master (
 account_id VARCHAR(20) NOT NULL PRIMARY KEY,
 account_number BIGINT NOT NULL,
 product_code VARCHAR(30) NOT NULL,
 branch_code VARCHAR(20) NOT NULL,
 account_type VARCHAR(30) NOT NULL,
 account_status VARCHAR(30) NOT NULL,
 currency_code VARCHAR(20) NOT NULL,
 open_date DATE NOT NULL,
 close_date DATE NULL,
 rm_id VARCHAR(20) NOT NULL,
 created_at DATETIME2 NOT NULL,
 updated_at DATETIME2 NOT NULL
);

CREATE TABLE cbs_account_nominee (
 relationship_id VARCHAR(20) NOT NULL PRIMARY KEY,
 account_id VARCHAR(20) NOT NULL,
 relationship_type VARCHAR(30) NOT NULL,
 share_percentage INT NOT NULL,
 nominee_name VARCHAR(200) NOT NULL,
 nominee_dob DATE NOT NULL,
 guardian_name VARCHAR(200) NULL,
 guardian_dob DATE NULL
);

CREATE TABLE cbs_customer_address (
 address_id VARCHAR(20) NOT NULL PRIMARY KEY,
 cif VARCHAR(20) NOT NULL,
 address_type VARCHAR(20) NOT NULL,
 address_line1 VARCHAR(255) NOT NULL,
 address_line2 VARCHAR(255) NULL,
 city VARCHAR(100) NOT NULL,
 state VARCHAR(100) NOT NULL,
 country VARCHAR(100) NOT NULL,
 postal_code VARCHAR(20) NOT NULL,
 is_primary CHAR(1) NOT NULL,
 created_at DATETIME2 NOT NULL,
 updated_at DATETIME2 NOT NULL
);

CREATE TABLE cbs_customer_contact (
 contact_id VARCHAR(20) NOT NULL PRIMARY KEY,
 cif VARCHAR(20) NOT NULL,
 mobile_number BIGINT NOT NULL,
 email_id VARCHAR(255) NOT NULL,
 alternate_mobile BIGINT NULL,
 landline_number BIGINT NULL,
 is_primary CHAR(1) NOT NULL,
 verified_flag CHAR(1) NOT NULL,
 created_at DATETIME2 NOT NULL,
 updated_at DATETIME2 NOT NULL
);

CREATE TABLE cbs_customer_kyc_reference (
 kyc_ref_id VARCHAR(20) NOT NULL PRIMARY KEY,
 cif VARCHAR(20) NOT NULL,
 kyc_status VARCHAR(30) NOT NULL,
 risk_category VARCHAR(30) NOT NULL,
 kyc_last_updated_date DATE NOT NULL,
 kyc_expiry_date DATE NOT NULL
);

CREATE TABLE cbs_customer_master (
 cif VARCHAR(20) NOT NULL PRIMARY KEY,
 customer_type VARCHAR(30) NOT NULL,
 first_name VARCHAR(100) NOT NULL,
 middle_name VARCHAR(100) NULL,
 last_name VARCHAR(100) NOT NULL,
 date_of_birth DATE NOT NULL,
 gender VARCHAR(20) NOT NULL,
 marital_status VARCHAR(30) NOT NULL,
 nationality VARCHAR(30) NOT NULL,
 occupation_code VARCHAR(30) NOT NULL,
 segment_code VARCHAR(30) NOT NULL,
 customer_status VARCHAR(30) NOT NULL,
 customer_since_date DATE NOT NULL,
 branch_code VARCHAR(20) NOT NULL,
 created_at DATETIME2 NOT NULL,
 updated_at DATETIME2 NOT NULL
);

CREATE TABLE cbs_master_table (
 id INT NOT NULL PRIMARY KEY,
 type VARCHAR(50) NOT NULL,
 code VARCHAR(50) NOT NULL,
 value VARCHAR(100) NOT NULL,
 description VARCHAR(500) NULL,
 created_at DATETIME2 NOT NULL,
 updated_at DATETIME2 NOT NULL
);

CREATE TABLE cbs_transaction_ledger (
 txn_id VARCHAR(20) NOT NULL PRIMARY KEY,
 account_id VARCHAR(20) NOT NULL,
 txn_reference_no BIGINT NOT NULL,
 txn_date DATETIME2 NOT NULL,
 txn_type VARCHAR(30) NOT NULL,
 dr_cr_flag VARCHAR(5) NOT NULL,
 amount DECIMAL(18,2) NOT NULL,
 balance_after_txn DECIMAL(18,2) NOT NULL,
 channel_code VARCHAR(30) NOT NULL,
 narration VARCHAR(500) NOT NULL,
 counterparty_reference VARCHAR(50) NOT NULL
);
