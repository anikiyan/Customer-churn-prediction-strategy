# dashboard_app.py

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Page config
st.set_page_config(page_title="Churn Dashboard", layout="wide")

# Title
st.title("📊 Customer Churn Dashboard")

# Load data
@st.cache_data
def load_data():
    return pd.read_csv("../data/processed/merged_features.csv")

df = load_data()

# Sidebar filters
st.sidebar.header("🔎 Filters")

segment_options = df["segment"].unique().tolist()
selected_segment = st.sidebar.multiselect("Segment", segment_options, default=segment_options)

gender_options = df["gender"].unique().tolist()
selected_gender = st.sidebar.multiselect("Gender", gender_options, default=gender_options)

# Apply filters
filtered_df = df[
    (df["segment"].isin(selected_segment)) &
    (df["gender"].isin(selected_gender))
]

# Show KPIs
st.subheader("📌 Key Stats")
col1, col2, col3 = st.columns(3)

col1.metric("Total Customers", len(filtered_df))
col2.metric("Churn Rate", f"{filtered_df['churn'].mean():.2%}")
col3.metric("Avg Tenure (months)", f"{filtered_df['tenure_months'].mean():.1f}")

# Plot churn by segment
st.subheader("📈 Churn Rate by Segment")
fig1, ax1 = plt.subplots()
sns.barplot(data=filtered_df, x="segment", y="churn", ax=ax1)
ax1.set_ylabel("Churn Rate")
st.pyplot(fig1)

# Ensure tenure_bucket exists
if 'tenure_bucket' not in filtered_df.columns and 'tenure_months' in filtered_df.columns:
    def bucket_tenure(months):
        if months <= 6:
            return '0-6'
        elif months <= 12:
            return '7-12'
        elif months <= 24:
            return '13-24'
        else:
            return '25+'

    filtered_df['tenure_bucket'] = filtered_df['tenure_months'].apply(bucket_tenure)


# Plot churn by tenure bucket
st.subheader("📊 Churn by Tenure Bucket")
fig2, ax2 = plt.subplots()
sns.countplot(data=filtered_df, x="tenure_bucket", hue="churn", ax=ax2)
st.pyplot(fig2)

# Display raw data
with st.expander("🧾 Show Raw Data"):
    st.dataframe(filtered_df)
