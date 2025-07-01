
import pandas as pd
import sqlite3
from pathlib import Path

# Define paths
base_dir = Path(__file__).resolve().parents[1]
raw_data = base_dir / 'data' / 'raw'
sql_script_path = base_dir / 'scripts' / 'data_ingestion.sql'
output_path = base_dir / 'data' / 'processed' / 'merged_features.csv'

# Create in-memory SQLite DB
conn = sqlite3.connect(':memory:')

# Load CSVs into SQLite tables
tables = {
    'customers': pd.read_csv(raw_data / 'customers.csv'),
    'usage_logs': pd.read_csv(raw_data / 'usage_logs.csv'),
    'tickets': pd.read_csv(raw_data / 'tickets.csv'),
    'payments': pd.read_csv(raw_data / 'payments.csv'),
}

for table_name, df in tables.items():
    df.to_sql(table_name, conn, index=False, if_exists='replace')

# Read full SELECT query from SQL file
with open(sql_script_path, 'r') as f:
    sql_query = f.read()

# Run the SELECT query
df_final = pd.read_sql_query(sql_query, conn)

# Export the result
df_final.to_csv(output_path, index=False)
print(f"✅ Data successfully exported to: {output_path}")
