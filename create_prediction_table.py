import sqlite3

conn = sqlite3.connect("database/retailiq.db")

cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS prediction_history(

id INTEGER PRIMARY KEY AUTOINCREMENT,

quantity REAL,

unit_price REAL,

predicted_profit REAL,

prediction_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP

)
""")

conn.commit()

conn.close()

print("Prediction History Table Created Successfully!")