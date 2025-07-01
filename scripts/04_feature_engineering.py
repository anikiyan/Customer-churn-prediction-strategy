
import pandas as pd
from pathlib import Path
from sklearn.preprocessing import OneHotEncoder

# Paths
base_dir = Path(__file__).resolve().parents[2]
input_path = Path(__file__).resolve().parents[1] / 'data' / 'processed' / 'merged_features.csv'
output_path = Path(__file__).resolve().parents[1] / 'data' / 'processed' / 'features_cleaned.csv'

# Load data
df = pd.read_csv(input_path)

# Handle missing values: fill with median or 0
df.fillna({
    'avg_logins': 0,
    'avg_active_minutes': 0,
    'total_tickets': 0,
    'tickets_resolved': 0,
    'total_payments': 0,
    'failed_payments': 0,
    'avg_payment': df['avg_payment'].median()
}, inplace=True)

# Create new features
df['support_resolution_ratio'] = df['tickets_resolved'] / (df['total_tickets'] + 1e-6)
df['failed_payment_ratio'] = df['failed_payments'] / (df['total_payments'] + 1e-6)
df['tenure_bucket'] = pd.cut(df['tenure_months'], bins=[0, 6, 12, 24, 60], labels=['0-6', '7-12', '13-24', '25+'])

# One-hot encode: gender, segment, tenure_bucket
df_encoded = pd.get_dummies(df, columns=['gender', 'segment', 'tenure_bucket'], drop_first=True)

# Save cleaned dataset
df_encoded.to_csv(output_path, index=False)
print(f"✅ Cleaned features exported to: {output_path}")
