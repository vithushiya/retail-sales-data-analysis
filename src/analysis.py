from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT / "data" / "retail_sales.csv"
OUT = ROOT / "outputs"
OUT.mkdir(exist_ok=True)

def load_and_clean_data(path=DATA_PATH):
    df = pd.read_csv(path)
    df["order_date"] = pd.to_datetime(df["order_date"], errors="coerce")
    df = df.drop_duplicates(subset=["order_id"])
    df["region"] = df["region"].fillna("Unknown")
    df["discount_rate"] = df["discount_rate"].fillna(0)
    numeric_cols = ["quantity", "unit_price_lkr", "revenue_lkr", "cost_lkr", "profit_lkr"]
    for col in numeric_cols:
        df[col] = pd.to_numeric(df[col], errors="coerce")
    df = df.dropna(subset=["order_date", "revenue_lkr", "profit_lkr"])
    df["month"] = df["order_date"].dt.to_period("M").astype(str)
    df["profit_margin_pct"] = (df["profit_lkr"] / df["revenue_lkr"].replace(0, pd.NA)) * 100
    return df

def main():
    df = load_and_clean_data()
    print("\\n--- DATA OVERVIEW ---")
    print(f"Rows: {len(df):,} | Columns: {len(df.columns)}")
    print("\\n--- KEY PERFORMANCE INDICATORS ---")
    revenue = df["revenue_lkr"].sum()
    profit = df["profit_lkr"].sum()
    orders = df["order_id"].nunique()
    print(f"Total revenue: LKR {revenue:,.2f}")
    print(f"Total profit:  LKR {profit:,.2f}")
    print(f"Total orders:  {orders:,}")
    print(f"Profit margin: {(profit/revenue*100):.2f}%")
    print(f"Average order value: LKR {revenue/orders:,.2f}")

    monthly = df.groupby("month", as_index=False).agg(
        revenue_lkr=("revenue_lkr", "sum"),
        profit_lkr=("profit_lkr", "sum")
    )
    category = df.groupby("category", as_index=False).agg(
        revenue_lkr=("revenue_lkr", "sum"),
        profit_lkr=("profit_lkr", "sum")
    ).sort_values("revenue_lkr", ascending=False)
    region = df.groupby("region", as_index=False)["revenue_lkr"].sum().sort_values(
        "revenue_lkr", ascending=False
    )
    channel = df.groupby("sales_channel", as_index=False)["revenue_lkr"].sum()

    monthly.to_csv(OUT/"monthly_performance.csv", index=False)
    category.to_csv(OUT/"category_performance.csv", index=False)
    region.to_csv(OUT/"region_performance.csv", index=False)

    plt.figure(figsize=(11, 5))
    plt.plot(monthly["month"], monthly["revenue_lkr"], marker="o")
    plt.title("Monthly Revenue")
    plt.xlabel("Month")
    plt.ylabel("Revenue (LKR)")
    plt.xticks(rotation=60, ha="right")
    plt.tight_layout()
    plt.savefig(OUT/"monthly_revenue.png", dpi=160)
    plt.close()

    plt.figure(figsize=(9, 5))
    plt.bar(category["category"], category["revenue_lkr"])
    plt.title("Revenue by Product Category")
    plt.xlabel("Category")
    plt.ylabel("Revenue (LKR)")
    plt.xticks(rotation=20, ha="right")
    plt.tight_layout()
    plt.savefig(OUT/"category_revenue.png", dpi=160)
    plt.close()

    print("\\n--- TOP CATEGORIES BY REVENUE ---")
    print(category.to_string(index=False))
    print("\\n--- REVENUE BY REGION ---")
    print(region.to_string(index=False))
    print("\\nAnalysis complete. Check the outputs/ folder.")

if __name__ == "__main__":
    main()
