import sqlite3
import pandas as pd

def get_dashboard_data():

    conn = sqlite3.connect("database/retailiq.db")

    sales = pd.read_sql("SELECT * FROM sales", conn)
    products = pd.read_sql("SELECT * FROM products", conn)
    customers = pd.read_sql("SELECT * FROM customers", conn)

    conn.close()

    dashboard = {

        "total_sales": len(sales),

        "total_products": len(products),

        "total_customers": len(customers),

        "total_revenue": sales["unit_price"].sum(),

        "total_profit": sales["profit"].sum(),

        "average_sale": sales["unit_price"].mean()

    }

    return dashboard