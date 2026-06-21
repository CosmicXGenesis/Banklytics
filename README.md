# Banklytics

## Overview

Banklytics is a synthetic banking analytics platform that simulates a Core Banking System by generating realistic relational banking datasets, loading them into SQL Server, and creating business intelligence dashboards in Power BI.
The objective is to build an end-to-end Customer 360 analytics solution that enables stakeholders and end users to derive actionable insights from banking data.

---

## Objectives

- Generate realistic synthetic banking datasets
- Simulate Core Banking System entities and relationships
- Ingest data into SQL Server
- Build analytical dashboards using Power BI
- Support data-driven decision making for business stakeholders

---

## Tech Stack

### Data Generation & Processing

- Python
- Pandas

### Database

- Microsoft SQL Server
- PyODBC

### Visualization

- Power BI

### Streaming (Future Enhancement)

- Kafka

---

## Project Architecture

```text
C360/

├── DataPipeline/
│
│   ├── Batch_Loaders/
│   │   └── Data ingestion scripts
│
│   ├── Config/
│   │   └── System configurations
│
│   ├── DB_Scripts/
│   │   └── SQL schema creation scripts
│
│   ├── Kafka/
│   │   └── Streaming integrations (future)
│
│   ├── Logs/
│   │   └── Execution logs
│
│   └── Utils/
│       ├── csv_utils.py
│       ├── db_connection.py
│       └── extract_schema.py
│
├── DBGenerators/
│   └── cbs/
│       ├── Generated_Data/
│       └── Generator_Script/
│
├── Power BI
        ├── Dashboard/
            └── Dashboard.pbix
        └── Theme/
│           └── lilac_theme.json
│
├── .gitignore
└── README.md
```

---

## System Entities

The project currently simulates:

- Customer Master
- Account Master
- Account Balance
- Customer Contact
- Customer Address
- Customer KYC Reference
- Account Nominee
- Account-Customer Mapping
- Transaction Ledger
- Master Reference Tables

---

## Project Workflow

### Step 1: Generate Synthetic Banking Data

Generate realistic CSV datasets while maintaining relational integrity.

### Step 2: Create SQL Schemas

Create normalized SQL Server tables.

### Step 3: Batch Load Data

Load generated CSV files into SQL Server.

### Step 4: Validate Data

Validate row counts and relationships.

### Step 5: Build Power BI Dashboards

Create dashboards for business users and stakeholders.

---

## Dashboard Use Cases

- Customer segmentation
- Account analysis
- Transaction analysis
- Branch performance tracking
- KYC compliance monitoring
- Banking operations insights

---

## Future Enhancements

- Kafka-based streaming ingestion

---

