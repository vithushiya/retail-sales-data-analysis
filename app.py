from pathlib import Path
import pandas as pd
import streamlit as st

ROOT = Path(__file__).resolve().parent
DATA = ROOT / "data" / "retail_sales.csv"

st.set_page_config(page_title="Retail Sales Insights", page_icon="📊", layout="wide")
st.title("📊 Retail Sales Analysis Dashboard")
st.caption("Portfolio project | Synthetic Sri Lankan retail dataset | Currency: LKR")

@st.cache_data
def load_data():
    df = pd.read_csv(DATA)
    df["order_date"] = pd.to_datetime(df["order_date"], errors="coerce")
    df = df.drop_duplicates(subset=["order_id"])
    df["region"] = df["region"].fillna("Unknown")
    df["discount_rate"] = df["discount_rate"].fillna(0)
    return df.dropna(subset=["order_date", "revenue_lkr", "profit_lkr"])

df = load_data()
st.sidebar.header("Dashboard filters")
min_date, max_date = df["order_date"].min().date(), df["order_date"].max().date()
date_range = st.sidebar.date_input("Order date range", value=(min_date, max_date),
                                   min_value=min_date, max_value=max_date)
regions = st.sidebar.multiselect("Region", sorted(df["region"].unique()),
                                 default=sorted(df["region"].unique()))
categories = st.sidebar.multiselect("Category", sorted(df["category"].unique()),
                                    default=sorted(df["category"].unique()))

if isinstance(date_range, tuple) and len(date_range) == 2:
    start, end = pd.Timestamp(date_range[0]), pd.Timestamp(date_range[1])
    filtered = df[(df["order_date"] >= start) &
                  (df["order_date"] <= end + pd.Timedelta(days=1))]
else:
    filtered = df.copy()
filtered = filtered[filtered["region"].isin(regions) & filtered["category"].isin(categories)]

if filtered.empty:
    st.warning("No records match these filters. Please change the selections.")
    st.stop()

revenue = filtered["revenue_lkr"].sum()
profit = filtered["profit_lkr"].sum()
orders = filtered["order_id"].nunique()
margin = (profit / revenue * 100) if revenue else 0
a, b, c, d = st.columns(4)
a.metric("Total revenue", f"LKR {revenue:,.0f}")
b.metric("Total profit", f"LKR {profit:,.0f}")
c.metric("Orders", f"{orders:,}")
d.metric("Profit margin", f"{margin:.1f}%")

st.subheader("Monthly performance")
monthly = filtered.assign(month=filtered["order_date"].dt.to_period("M").astype(str))
monthly = monthly.groupby("month")[["revenue_lkr", "profit_lkr"]].sum()
st.line_chart(monthly)

left, right = st.columns(2)
with left:
    st.subheader("Revenue by category")
    by_category = filtered.groupby("category")["revenue_lkr"].sum().sort_values(ascending=False)
    st.bar_chart(by_category)
with right:
    st.subheader("Revenue by region")
    by_region = filtered.groupby("region")["revenue_lkr"].sum().sort_values(ascending=False)
    st.bar_chart(by_region)

st.subheader("Sales channel and payment method")
x, y = st.columns(2)
with x:
    st.write("Revenue by sales channel")
    st.bar_chart(filtered.groupby("sales_channel")["revenue_lkr"].sum())
with y:
    st.write("Number of orders by payment method")
    st.bar_chart(filtered.groupby("payment_method")["order_id"].nunique())

st.subheader("Top 10 products by revenue")
top_products = (filtered.groupby("product", as_index=False)
                .agg(revenue_lkr=("revenue_lkr", "sum"),
                     units_sold=("quantity", "sum"))
                .sort_values("revenue_lkr", ascending=False).head(10))
st.dataframe(top_products, use_container_width=True, hide_index=True)

st.download_button("Download filtered data as CSV",
                   filtered.to_csv(index=False).encode("utf-8"),
                   file_name="filtered_retail_sales.csv", mime="text/csv")
st.info("Learning dataset only: all records are synthetic and do not represent a real retailer.")
