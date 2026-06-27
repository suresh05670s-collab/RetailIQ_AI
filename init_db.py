import sqlite3

conn = sqlite3.connect("database/retailiq.db")
cursor = conn.cursor()

cursor.execute("""
UPDATE users
SET fullname = ?, email = ?, password = ?
WHERE id = 1
""", (
    "Harini",
    "retailadmin@gmail.com",
    "Retail@2007"
))

conn.commit()
conn.close()

print("User updated successfully!")