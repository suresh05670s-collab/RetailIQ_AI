import sqlite3
import pandas as pd
import plotly.express as px


def profit_trend_chart():

    conn = sqlite3.connect("database/retailiq.db")

    df = pd.read_sql("SELECT * FROM sales", conn)

    conn.close()

    if df.empty:
        return "<h3>No Sales Data Available</h3>"

    df["sale_date"] = pd.to_datetime(df["sale_date"])

    df["Month"] = df["sale_date"].dt.strftime("%b")

    monthly_profit = df.groupby("Month")["profit"].sum().reset_index()

    fig = px.line(
        monthly_profit,
        x="Month",
        y="profit",
        title="Monthly Profit Trend",
        markers=True
    )

    return fig.to_html(full_html=False)