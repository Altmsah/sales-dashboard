import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import warnings

# 🌐 Page Configuration
st.set_page_config(page_title="Sales Performance Dashboard", layout="wide", page_icon="📊")
warnings.filterwarnings('ignore')

# 🎨 Global Style
sns.set_style("whitegrid")
plt.rcParams.update({
    "font.family": "sans-serif",
    "font.size": 11,
    "axes.titlesize": 13,
    "axes.labelsize": 11,
    "axes.titlepad": 10
})

# 📦 Sample Data
data = {
    'CustomerID': range(1, 43),
    'Age': [23,33,43,66,11,88,34,98,22,13,44,22,12,44,59,45,88,43,21,88,70,
            23,33,43,66,11,88,34,98,22,13,44,22,12,44,59,45,88,43,21,88,70],
    'City': ['New York','London','Tokyo','Paris','Sydney'] * 8 + ['New York','New York'],
    'Purchases': [2,3,1,2,4,66,3,7,2,9,1,20,3,1,4,5,6,6,2,20,44,2,3,1,2,4,66,30,7,2,9,1,2,3,1,4,5,6,6,2,20,44],
    'Total_Spent': [1000,300,22,990,5000,800,359,44,222,60,50,220,100,30,21,88,88,20,320,99,300,
                   100,3000,202,90,5030,870,359,44,222,60,500,220,100,20,11,58,88,20,320,909,3000]
}
df = pd.DataFrame(data)

# 🧮 Data Processing
def prepare_dashboard_data(df):
    df['Spending_Efficiency'] = df['Total_Spent'] / df['Purchases']
    conditions = [
        df['Spending_Efficiency'] < 20,
        (df['Spending_Efficiency'] >= 20) & (df['Spending_Efficiency'] < 100),
        df['Spending_Efficiency'] >= 100
    ]
    choices = ['Low Value', 'Medium Value', 'High Value']
    df['Customer_Segment'] = np.select(conditions, choices, default='Undefined')
    return df

df = prepare_dashboard_data(df)

# 🧭 Sidebar Filters
with st.sidebar:
    st.header("⚙️ Filter Options")
    cities = st.multiselect("Select Cities:", df['City'].unique(), default=df['City'].unique())
    segments = st.multiselect("Select Segments:", df['Customer_Segment'].unique(), default=df['Customer_Segment'].unique())
    st.markdown("---")
    st.caption("Use the filters above to customize the dashboard view.")

filtered_df = df[(df['City'].isin(cities)) & (df['Customer_Segment'].isin(segments))]

# 📊 KPI Section
st.markdown("## 🚀 Key Performance Indicators")
col1, col2, col3, col4 = st.columns(4)
kpi_colors = ['#4E79A7', '#F28E2B', '#E15759', '#76B7B2']

total_revenue = filtered_df['Total_Spent'].sum()
avg_efficiency = filtered_df['Spending_Efficiency'].mean()
total_customers = len(filtered_df)
avg_purchases = filtered_df['Purchases'].mean()

def create_kpi_chart(color, text, label):
    fig, ax = plt.subplots()
    ax.pie([1], colors=[color], radius=0.7)
    ax.text(0, 0, text, ha='center', va='center', fontsize=13, fontweight='bold', color='white')
    plt.gcf().patch.set_facecolor('#f8f9fa')
    plt.axis("off")
    st.pyplot(fig, use_container_width=True)
    st.markdown(f"<p style='text-align:center; font-weight:bold; color:{color}'>{label}</p>", unsafe_allow_html=True)

with col1:
    create_kpi_chart(kpi_colors[0], f"${total_revenue:,.0f}", "Total Revenue")

with col2:
    create_kpi_chart(kpi_colors[1], f"${avg_efficiency:.1f}", "Avg. Spending Efficiency")

with col3:
    create_kpi_chart(kpi_colors[2], f"{total_customers}", "Total Customers")

with col4:
    create_kpi_chart(kpi_colors[3], f"{avg_purchases:.1f}", "Avg. Purchases")

# 📈 Visual Analysis
st.markdown("---")
st.markdown("## 📊 Visual Insights")

col1, col2, col3 = st.columns(3)
palette = ["#4E79A7", "#F28E2B", "#E15759"]

with col1:
    st.markdown("**Customer Segments Distribution**")
    fig1, ax1 = plt.subplots()
    segment_counts = filtered_df['Customer_Segment'].value_counts()
    ax1.pie(segment_counts, labels=None, autopct='%1.0f%%', colors=palette, startangle=90)
    ax1.legend(segment_counts.index, loc="best", bbox_to_anchor=(1, 0.5))
    st.pyplot(fig1, use_container_width=True)

with col2:
    st.markdown("**Average Efficiency per Segment**")
    fig2, ax2 = plt.subplots()
    sns.barplot(
        x=segment_counts.index,
        y=filtered_df.groupby('Customer_Segment')['Spending_Efficiency'].mean().values,
        palette=palette, ax=ax2
    )
    for container in ax2.containers:
        ax2.bar_label(container, fmt="%.1f$")
    ax2.set_xlabel("")
    ax2.set_ylabel("")
    st.pyplot(fig2, use_container_width=True)

with col3:
    st.markdown("**Revenue by City**")
    fig3, ax3 = plt.subplots()
    city_revenue = filtered_df.groupby('City')['Total_Spent'].sum().sort_values()
    sns.barplot(x=city_revenue.values, y=city_revenue.index, ax=ax3, color='#76B7B2')
    for i, v in enumerate(city_revenue.values):
        ax3.text(v + 10, i, f"${v:,.0f}", va='center')
    ax3.set_xlabel("")
    ax3.set_ylabel("")
    st.pyplot(fig3, use_container_width=True)

# 🌈 Scatter Plot
st.markdown("### 📉 Purchase Behavior Analysis")
fig4, ax4 = plt.subplots(figsize=(10, 5))
scatter = ax4.scatter(
    filtered_df['Purchases'],
    filtered_df['Spending_Efficiency'],
    c=filtered_df['Total_Spent'],
    cmap='viridis', s=80, alpha=0.8
)
ax4.set_xlabel("Number of Purchases")
ax4.set_ylabel("Spending Efficiency ($ per purchase)")
plt.colorbar(scatter, ax=ax4, label='Total Spent ($)')
st.pyplot(fig4, use_container_width=True)

# 📋 Data Table
st.markdown("---")
st.markdown("## 🧾 Customer Data")
st.dataframe(filtered_df, use_container_width=True)

# 🧠 Info
with st.expander("ℹ️ About the Analysis"):
    st.write("""
    - **Spending Efficiency** = Total Spent ÷ Purchases  
    - **High Value** ≥ $100  
    - **Medium Value** = $20 - $99  
    - **Low Value** < $20  
    This dashboard visualizes customer behavior and spending patterns across cities.
    """)
