import sqlite3
import pandas as pd
import plotly.express as px


def top_products_chart():

    conn = sqlite3.connect("database/retailiq.db")

    df = pd.read_sql("SELECT * FROM sales", conn)

    conn.close()

    if df.empty:
        return "<h3>No Sales Data Available</h3>"

    top_products = (
        df.groupby("product_name")["quantity"]
        .sum()
        .reset_index()
        .sort_values(by="quantity", ascending=False)
    )

    fig = px.bar(
        top_products,
        x="product_name",
        y="quantity",
        title="Top Selling Products",
        color="quantity"
    )

    return fig.to_html(full_html=False)