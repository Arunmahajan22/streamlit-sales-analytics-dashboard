import streamlit as st
import pandas as pd
import plotly.express as px

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Sales Performance Dashboard",
    page_icon="📊",
    layout="wide"
)

# ---------------- HEADER ----------------
col1, col2 = st.columns([1, 4])

with col1:
    st.image("assets/logo.png", width=120)

with col2:
    st.title("📊 Sales Performance Dashboard")

st.divider()

# ---------------- LOAD DATA ----------------
df = pd.read_csv("data.csv")

# Clean column names (removes hidden spaces)
df.columns = df.columns.str.strip()

# Convert Date column to datetime
df["Date"] = pd.to_datetime(df["Date"], dayfirst=True, errors="coerce")


# ---------------- SIDEBAR FILTERS ----------------
st.sidebar.header("Filters")

category = st.sidebar.multiselect(
    "Select Category",
    df["Category"].unique(),
    default=df["Category"].unique()
)

region = st.sidebar.multiselect(
    "Select Region",
    df["Region"].unique(),
    default=df["Region"].unique()
)

start_date = st.sidebar.date_input(
    "Start Date",
    df["Date"].min()
)

end_date = st.sidebar.date_input(
    "End Date",
    df["Date"].max()
)

# Apply filters
filtered_df = df[
    (df["Category"].isin(category)) &
    (df["Region"].isin(region)) &
    (df["Date"] >= pd.to_datetime(start_date)) &
    (df["Date"] <= pd.to_datetime(end_date))
]

# ---------------- KPI SECTION ----------------
st.subheader("📌 Key Performance Indicators")

col1, col2, col3 = st.columns(3)

col1.metric("Total Sales", f"₹ {filtered_df['Sales'].sum():,.0f}")
col2.metric("Average Sales", f"₹ {filtered_df['Sales'].mean():,.0f}")
col3.metric("Total Orders", filtered_df.shape[0])

st.divider()

# ---------------- BAR CHART ----------------
st.subheader("📊 Sales by Product")

fig_bar = px.bar(
    filtered_df,
    x="Product",
    y="Sales",
    color="Product",
    title="Product-wise Sales",
    template="plotly_white"
)

st.plotly_chart(fig_bar, use_container_width=True)

# ---------------- LINE CHART ----------------
st.subheader("📈 Sales Trend Over Time")

trend = filtered_df.groupby("Date")["Sales"].sum().reset_index()

fig_line = px.line(
    trend,
    x="Date",
    y="Sales",
    markers=True,
    title="Sales Trend",
    template="plotly_white"
)

st.plotly_chart(fig_line, use_container_width=True)

# ---------------- PIE CHART ----------------
st.subheader("🥧 Sales Distribution by Category")

category_data = filtered_df.groupby("Category")["Sales"].sum().reset_index()

fig_pie = px.pie(
    category_data,
    names="Category",
    values="Sales",
    title="Category Contribution",
    template="plotly_white"
)

st.plotly_chart(fig_pie, use_container_width=True)

st.divider()

# ---------------- DATA TABLE ----------------
st.subheader("📋 Filtered Data Table")

st.dataframe(filtered_df, use_container_width=True)

# ---------------- DOWNLOAD BUTTON ----------------
st.download_button(
    label="⬇ Download Filtered Data as CSV",
    data=filtered_df.to_csv(index=False),
    file_name="filtered_sales_data.csv",
    mime="text/csv"
)

st.markdown("---")
st.caption("Built with ❤️ using Streamlit")
