import sqlite3

conn = sqlite3.connect("database/retailiq.db")
cursor = conn.cursor()

sales = [

("INV001","Laptop","Rahul",2,55000,8000,"2026-06-20"),
("INV002","Phone","Harini",3,25000,5000,"2026-06-21"),
("INV003","Mouse","Kumar",5,700,1200,"2026-06-22"),
("INV004","Keyboard","Priya",2,1500,400,"2026-06-23"),
("INV005","Monitor","Arun",1,12000,2500,"2026-06-24")

]

cursor.executemany("""
INSERT INTO sales(
invoice,
product_name,
customer_name,
quantity,
unit_price,
profit,
sale_date
)
VALUES(?,?,?,?,?,?,?)
""", sales)

conn.commit()
conn.close()

print("Sales inserted successfully!")