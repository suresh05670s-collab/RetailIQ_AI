import sqlite3
import pandas as pd
import plotly.express as px


def regional_sales_chart():

    conn = sqlite3.connect("database/retailiq.db")

    sales = pd.read_sql("SELECT * FROM sales", conn)
    customers = pd.read_sql("SELECT * FROM customers", conn)

    conn.close()

    if sales.empty or customers.empty:
        return "<h3>No Data Available</h3>"

    df = sales.merge(customers, on="customer_name")

    region = (
        df.groupby("region")["profit"]
        .sum()
        .reset_index()
    )

    fig = px.bar(
        region,
        x="region",
        y="profit",
        title="Regional Profit"
    )

    return fig.to_html(full_html=False)