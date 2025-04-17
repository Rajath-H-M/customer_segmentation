import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(page_title="Customer Segmentation Dashboard", layout="wide")

@st.cache_data
def load_data():
    df = pd.read_csv("outputs/customer_segments.csv")
    return df

df = load_data()

st.title("📊 Customer Segmentation & Discount Strategies")

segments = df['Segment'].unique()
selected_segment = st.sidebar.selectbox("🔍 Select Customer Segment", segments)

print(f"Selected Segment: '{selected_segment}'")

filtered_df = df[df['Segment'] == selected_segment].copy()

def calculate_churn(row, frequency_threshold=6, spending_threshold=298):
    if row['Customer_Frequency'] < frequency_threshold and row['Total_Spending'] < spending_threshold:
        return 1  
    else:
        return 0  

filtered_df['Churned'] = filtered_df.apply(calculate_churn, axis=1)
total_customers = len(filtered_df)
churned_customers = filtered_df['Churned'].sum()
churn_rate = churned_customers / total_customers if total_customers > 0 else 0

discount_strategies = {
    "😴 Low Value": "⚠️ Re-engage with small discounts and targeted emails.",
    "🛍 Deal Seeker": "🔥 Use flash sales (30-50%) and coupons.",
    "🎯 High Spender": "🏆 Offer loyalty programs and early access.",
    "🔁 Frequent Buyer": "💎 Introduce subscription discounts or bundles."
}

normalized_selected_segment = selected_segment.strip()

print("Available discount strategies:", discount_strategies.keys())
print(f"Normalized selected_segment: '{normalized_selected_segment}'")
discount_info = discount_strategies.get(normalized_selected_segment, "🔥 Use flash sales (30-50%) and coupons.")
filtered_df['CLV'] = filtered_df['AOV'] * filtered_df['Customer_Frequency'] * 0.3

col1, col2 = st.columns(2)

with col1:
    st.subheader("📈 PCA Cluster View")
    fig, ax = plt.subplots()
    sns.scatterplot(data=filtered_df, x='PCA1', y='PCA2', hue='Segment', palette="Set2", s=100, ax=ax)
    ax.set_title("Customer Segments by PCA")
    st.pyplot(fig)

with col2:
    st.subheader("💡 Strategy Recommendation")
    st.info(discount_info) 
    st.metric("Average CLV (₹)", round(filtered_df['CLV'].mean(), 2))
    churn_rate_percentage = round(churn_rate * 100, 2) 
    st.metric("Churn Rate (%)", churn_rate_percentage)

with st.expander("📋 View Customer Details"):
    st.dataframe(filtered_df[['User_ID', 'AOV', 'Customer_Frequency', 'Total_Spending', 'CLV', 'Churned']])

st.markdown("---")
st.caption("Built by Rajath")
