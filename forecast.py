import sqlite3
import joblib
import numpy as np

model = joblib.load("models/sales_model.pkl")

def predict_next_month_sales():

    conn = sqlite3.connect("database/retailiq.db")
    cursor = conn.cursor()

    cursor.execute("""
        SELECT AVG(quantity), AVG(unit_price)
        FROM sales
    """)

    row = cursor.fetchone()
    conn.close()

    avg_quantity = row[0] or 0
    avg_price = row[1] or 0

    prediction = model.predict(
        np.array([[avg_quantity, avg_price]])
    )[0]

    return round(float(prediction), 2)