import sqlite3
import pandas as pd
import plotly.express as px


def category_chart():

    conn = sqlite3.connect("database/retailiq.db")

    sales = pd.read_sql("SELECT * FROM sales", conn)
    products = pd.read_sql("SELECT * FROM products", conn)

    conn.close()

    if sales.empty or products.empty:
        return "<h3>No Data Available</h3>"

    sales["product_name"] = sales["product_name"].str.lower().str.strip()
    products["product_name"] = products["product_name"].str.lower().str.strip()

    df = sales.merge(products, on="product_name")

    if df.empty:
        return "<h3>No Matching Products Found</h3>"

    category_sales = (
        df.groupby("category")["quantity"]
        .sum()
        .reset_index()
    )

    fig = px.pie(
        category_sales,
        names="category",
        values="quantity",
        title="Product Category Distribution"
    )

    return fig.to_html(full_html=False)