# Retail Sales Data Analysis & Business Intelligence Dashboard

A beginner-friendly, end-to-end Data Analyst portfolio project using a **synthetic Sri Lankan retail sales dataset**. The project demonstrates data cleaning, exploratory data analysis (EDA), business KPIs, SQL analysis, and an interactive Streamlit dashboard.

> Dataset note: `data/retail_sales.csv` is synthetic and created for learning. It is not real company/customer data.

## Project questions
1. How do revenue and profit change month by month?
2. Which product categories and products generate the most revenue?
3. Which regions and sales channels perform best?
4. What are the most frequently used payment methods?
5. What business actions could improve sales and profitability?

## Tools
- Python, Pandas, NumPy
- Matplotlib
- SQL (portable query examples)
- Streamlit

## Folder structure
```text
retail-sales-data-analysis/
├── data/
│   └── retail_sales.csv
├── src/
│   └── analysis.py
├── sql/
│   └── analysis_queries.sql
├── app.py
├── requirements.txt
├── README.md
└── .gitignore
```

## Run the project

### 1. Clone the repository
```bash
git clone https://github.com/VithusiyaT/retail-sales-data-analysis.git
cd retail-sales-data-analysis
```

### 2. Create and activate a virtual environment (recommended)
Windows:
```bash
python -m venv .venv
.venv\Scripts\activate
```
macOS/Linux:
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install packages
```bash
pip install -r requirements.txt
```

### 4. Run the analysis script
```bash
python src/analysis.py
```
Cleaned data and charts will be saved in the `outputs/` folder.

### 5. Launch the interactive dashboard
```bash
streamlit run app.py
```
The dashboard opens in your browser. Use the filters to explore dates, regions, and product categories.

## Key metrics
- **Revenue:** Sum of `revenue_lkr`
- **Cost:** Sum of `cost_lkr`
- **Profit:** Sum of `profit_lkr`
- **Profit margin:** Profit / Revenue × 100
- **Orders:** Number of unique `order_id` values
- **Average order value:** Revenue / Number of orders

## Data dictionary
| Column | Description |
|---|---|
| order_id | Unique order reference |
| order_date | Date of order |
| customer_id | Synthetic customer reference |
| region | Sales region in Sri Lanka |
| sales_channel | In-store or Online |
| category | Product category |
| product | Product name |
| quantity | Units purchased |
| unit_price_lkr | Price per unit in LKR |
| discount_rate | Discount fraction (e.g. 0.10 = 10%) |
| revenue_lkr | Revenue after discount |
| cost_lkr | Estimated product cost |
| profit_lkr | Revenue minus cost |
| payment_method | Payment type |

## Suggested portfolio workflow
1. Read the dataset and inspect its shape, data types, and missing values.
2. Clean missing values and remove duplicate orders.
3. Create month, year, and profit-margin fields.
4. Calculate KPIs and group sales by month, region, category, and channel.
5. Use the dashboard filters to answer the project questions.
6. Write 3–5 evidence-based business recommendations after reviewing your actual results.

## Important
Do not claim the synthetic data represents a real business. In an interview, explain that you generated a practice dataset and demonstrate your analysis process. You can later replace it with an openly licensed real dataset and update the README accordingly.
