import sqlite3
import pandas as pd
from sklearn.linear_model import LinearRegression
import joblib
import os

conn = sqlite3.connect("database/retailiq.db")

df = pd.read_sql("SELECT quantity, unit_price, profit FROM sales", conn)

conn.close()

if len(df) < 2:
    print("Need at least 2 sales records to train the model.")
    exit()

X = df[["quantity", "unit_price"]]
y = df["profit"]

model = LinearRegression()
model.fit(X, y)

os.makedirs("models", exist_ok=True)

joblib.dump(model, "models/sales_model.pkl")

print("AI Model Trained Successfully!")