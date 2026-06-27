print("RetailIQ app.py loaded successfully")
from flask import Flask, render_template, request, redirect, session
from analytics import get_dashboard_data
from prediction import monthly_sales_chart
from profit_chart import profit_trend_chart
from top_products import top_products_chart
from category_chart import category_chart
from regional_chart import regional_sales_chart
from ai_insights import get_ai_insights
from forecast import predict_next_month_sales
import sqlite3
import webbrowser
from threading import Timer
import os
import joblib

app = Flask(__name__)
app.secret_key = "retailiq_secret_key"
model = joblib.load("models/sales_model.pkl")


def get_db_connection():
    conn = sqlite3.connect("database/retailiq.db")
    conn.row_factory = sqlite3.Row
    return conn


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        fullname = request.form["fullname"]
        email = request.form["email"]
        password = request.form["password"]
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("""
        INSERT INTO users(fullname,email,password)
        VALUES(?,?,?)
        """, (fullname, email, password))

        conn.commit()
        conn.close()

        return redirect("/login")

    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        email = request.form["email"]
        password = request.form["password"]

        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("""
        SELECT * FROM users
        WHERE email=? AND password=?
        """, (email, password))

        user = cursor.fetchone()

        conn.close()

        if user:
            session["user"] = user["fullname"]
            return redirect("/dashboard")

        return "Invalid Email or Password"

    return render_template("login.html")
@app.route("/dashboard")
def dashboard():

    if "user" not in session:
        return redirect("/login")

    data = get_dashboard_data()

    return render_template(
        "dashboard.html",
        user=session["user"],
        dashboard=data
    )
@app.route("/add_product", methods=["GET", "POST"])
def add_product():

    if "user" not in session:
        return redirect("/login")

    if request.method == "POST":

        product_name = request.form["product_name"]
        category = request.form["category"]
        price = request.form["price"]
        stock = request.form["stock"]

        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("""
        INSERT INTO products(product_name, category, price, stock)
        VALUES (?, ?, ?, ?)
        """, (product_name, category, price, stock))

        conn.commit()
        conn.close()

        return redirect("/products")

    return render_template("add_product.html")
@app.route("/products")
def products():

    if "user" not in session:
        return redirect("/login")

    search = request.args.get("search")

    conn = get_db_connection()
    cursor = conn.cursor()

    if search:

        cursor.execute("""
        SELECT *
        FROM products
        WHERE product_name LIKE ?
        """, ('%' + search + '%',))

    else:

        cursor.execute("SELECT * FROM products")

    products = cursor.fetchall()

    conn.close()

    return render_template("products.html", products=products)
@app.route("/edit_product/<int:id>", methods=["GET", "POST"])
def edit_product(id):

    if "user" not in session:
        return redirect("/login")

    conn = get_db_connection()
    cursor = conn.cursor()

    if request.method == "POST":

        product_name = request.form["product_name"]
        category = request.form["category"]
        price = request.form["price"]
        stock = request.form["stock"]

        cursor.execute("""
        UPDATE products
        SET product_name=?, category=?, price=?, stock=?
        WHERE id=?
        """, (product_name, category, price, stock, id))

        conn.commit()
        conn.close()

        return redirect("/products")

    cursor.execute("SELECT * FROM products WHERE id=?", (id,))
    product = cursor.fetchone()

    conn.close()

    return render_template("edit_product.html", product=product)
@app.route("/search_product", methods=["GET"])
def search_product():

    if "user" not in session:
        return redirect("/login")

    keyword = request.args.get("keyword")

    conn = get_db_connection()

    products = conn.execute("""
    SELECT * FROM products
    WHERE product_name LIKE ?
    """, ('%' + keyword + '%',)).fetchall()

    conn.close()

    return render_template("products.html", products=products)
@app.route("/delete_product/<int:id>")
def delete_product(id):

    if "user" not in session:
        return redirect("/login")

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM products WHERE id=?", (id,))

    conn.commit()
    conn.close()

    return redirect("/products")

@app.route("/customers")
def customers():

    if "user" not in session:
        return redirect("/login")

    search = request.args.get("search")

    conn = get_db_connection()
    cursor = conn.cursor()

    if search:

        cursor.execute("""
        SELECT *
        FROM customers
        WHERE customer_name LIKE ?
        """, ('%' + search + '%',))

    else:

        cursor.execute("SELECT * FROM customers")

    customers = cursor.fetchall()

    conn.close()

    return render_template("customers.html",
                           customers=customers)

@app.route("/add_customer", methods=["GET", "POST"])
def add_customer():

    if request.method == "POST":

        customer_name = request.form["customer_name"]
        email = request.form["email"]
        phone = request.form["phone"]
        region = request.form["region"]

        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("""
        INSERT INTO customers(customer_name,email,phone,region)
        VALUES(?,?,?,?)
        """, (customer_name, email, phone, region))

        conn.commit()
        conn.close()

        return redirect("/customers")

    return render_template("add_customer.html")
@app.route("/edit_customer/<int:id>", methods=["GET", "POST"])
def edit_customer(id):

    conn = get_db_connection()
    cursor = conn.cursor()

    if request.method == "POST":

        customer_name = request.form["customer_name"]
        email = request.form["email"]
        phone = request.form["phone"]
        region = request.form["region"]

        cursor.execute("""
        UPDATE customers
        SET customer_name=?, email=?, phone=?, region=?
        WHERE id=?
        """, (customer_name, email, phone, region, id))

        conn.commit()
        conn.close()

        return redirect("/customers")

    cursor.execute("SELECT * FROM customers WHERE id=?", (id,))
    customer = cursor.fetchone()

    conn.close()

    return render_template("edit_customer.html", customer=customer)
@app.route("/delete_customer/<int:id>")
def delete_customer(id):

    if "user" not in session:
        return redirect("/login")

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM customers WHERE id=?", (id,))

    conn.commit()
    conn.close()

    return redirect("/customers")
@app.route("/customer_stats")
def customer_stats():

    if "user" not in session:
        return redirect("/login")

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM customers")
    total_customers = cursor.fetchone()[0]

    cursor.execute("""
    SELECT region,
    COUNT(*)
    FROM customers
    GROUP BY region
    """)

    region_data = cursor.fetchall()

    conn.close()

    return render_template(
        "customer_stats.html",
        total_customers=total_customers,
        region_data=region_data
    )
@app.route("/sales")
def sales():

    if "user" not in session:
        return redirect("/login")

    keyword = request.args.get("search")

    conn = get_db_connection()

    if keyword:

        sales = conn.execute("""
        SELECT *
        FROM sales
        WHERE invoice LIKE ?
        OR product_name LIKE ?
        OR customer_name LIKE ?
        """,
        (
            '%' + keyword + '%',
            '%' + keyword + '%',
            '%' + keyword + '%'
        )).fetchall()

    else:

        sales = conn.execute("SELECT * FROM sales").fetchall()

    conn.close()

    return render_template("sales.html", sales=sales)
@app.route("/add_sale", methods=["GET", "POST"])
def add_sale():

    if "user" not in session:
        return redirect("/login")

    if request.method == "POST":

        invoice = request.form["invoice"]
        product_name = request.form["product_name"]
        customer_name = request.form["customer_name"]
        quantity = request.form["quantity"]
        unit_price = request.form["unit_price"]
        profit = request.form["profit"]
        sale_date = request.form["sale_date"]

        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("""
        INSERT INTO sales(
            invoice,
            product_name,
            customer_name,
            quantity,
            unit_price,
            profit,
            sale_date
        )
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            invoice,
            product_name,
            customer_name,
            quantity,
            unit_price,
            profit,
            sale_date
        ))

        conn.commit()
        conn.close()

        return redirect("/sales")

    return render_template("add_sale.html")
@app.route("/edit_sale/<int:id>", methods=["GET", "POST"])
def edit_sale(id):

    if "user" not in session:
        return redirect("/login")

    conn = get_db_connection()
    cursor = conn.cursor()

    if request.method == "POST":

        invoice = request.form["invoice"]
        product_name = request.form["product_name"]
        customer_name = request.form["customer_name"]
        quantity = request.form["quantity"]
        unit_price = request.form["unit_price"]
        profit = request.form["profit"]
        sale_date = request.form["sale_date"]

        cursor.execute("""
        UPDATE sales
        SET invoice=?,
            product_name=?,
            customer_name=?,
            quantity=?,
            unit_price=?,
            profit=?,
            sale_date=?
        WHERE id=?
        """, (
            invoice,
            product_name,
            customer_name,
            quantity,
            unit_price,
            profit,
            sale_date,
            id
        ))

        conn.commit()
        conn.close()

        return redirect("/sales")

    cursor.execute("SELECT * FROM sales WHERE id=?", (id,))
    sale = cursor.fetchone()

    conn.close()

    return render_template("edit_sale.html", sale=sale)
@app.route("/delete_sale/<int:id>")
def delete_sale(id):

    if "user" not in session:
        return redirect("/login")

    conn = get_db_connection()

    conn.execute("DELETE FROM sales WHERE id=?", (id,))

    conn.commit()
    conn.close()

    return redirect("/sales")
from prediction import monthly_sales_chart

@app.route("/analytics")
def analytics():

    if "user" not in session:
        return redirect("/login")

    chart = monthly_sales_chart()

    return render_template(
        "analytics.html",
        chart=chart
    )
@app.route("/prediction", methods=["GET", "POST"])
def prediction():

    if "user" not in session:
        return redirect("/login")

    if request.method == "POST":

        quantity = float(request.form["quantity"])
        unit_price = float(request.form["unit_price"])

        result = model.predict([[quantity, unit_price]])[0]

        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("""
        INSERT INTO prediction_history(
            quantity,
            unit_price,
            predicted_profit
        )
        VALUES(?,?,?)
        """, (quantity, unit_price, result))

        conn.commit()
        conn.close()

        return render_template(
            "prediction.html",
            prediction=round(result, 2)
        )

    return render_template("prediction.html")
@app.route("/profit_chart")
def profit_chart():

    if "user" not in session:
        return redirect("/login")

    chart = profit_trend_chart()

    return render_template(
        "profit_chart.html",
        chart=chart
    )
@app.route("/top_products")
def top_products():

    if "user" not in session:
        return redirect("/login")

    chart = top_products_chart()

    return render_template(
        "top_products.html",
        chart=chart
    )
@app.route("/category_chart")
def category():

    if "user" not in session:
        return redirect("/login")

    chart = category_chart()

    return render_template(
        "category_chart.html",
        chart=chart
    )
@app.route("/regional_chart")
def regional_chart():

    if "user" not in session:
        return redirect("/login")

    chart = regional_sales_chart()

    return render_template(
        "regional_chart.html",
        chart=chart
    )
@app.route("/analytics_dashboard")
def analytics_dashboard():

    if "user" not in session:
        return redirect("/login")

    return render_template(
        "full_dashboard.html",
        sales_chart=monthly_sales_chart(),
        profit_chart=profit_trend_chart(),
        top_chart=top_products_chart(),
        category_chart=category_chart(),
        regional_chart=regional_sales_chart()
    )
@app.route("/prediction_history")
def prediction_history():

    if "user" not in session:
        return redirect("/login")

    keyword = request.args.get("search")

    conn = get_db_connection()

    if keyword:

        history = conn.execute("""
        SELECT *
        FROM prediction_history
        WHERE quantity LIKE ?
        OR unit_price LIKE ?
        OR predicted_profit LIKE ?
        ORDER BY id DESC
        """,
        (
            '%' + keyword + '%',
            '%' + keyword + '%',
            '%' + keyword + '%'
        )).fetchall()

    else:

        history = conn.execute("""
        SELECT *
        FROM prediction_history
        ORDER BY id DESC
        """).fetchall()

    conn.close()

    return render_template(
        "prediction_history.html",
        history=history
    )
@app.route("/delete_prediction/<int:id>")
def delete_prediction(id):

    if "user" not in session:
        return redirect("/login")

    conn = get_db_connection()

    conn.execute(
        "DELETE FROM prediction_history WHERE id=?",
        (id,)
    )

    conn.commit()
    conn.close()

    return redirect("/prediction_history")
@app.route("/edit_prediction/<int:id>", methods=["GET", "POST"])
def edit_prediction(id):

    if "user" not in session:
        return redirect("/login")

    conn = get_db_connection()

    if request.method == "POST":

        quantity = request.form["quantity"]
        unit_price = request.form["unit_price"]
        predicted_profit = request.form["predicted_profit"]

        conn.execute("""
        UPDATE prediction_history
        SET quantity=?,
            unit_price=?,
            predicted_profit=?
        WHERE id=?
        """,
        (
            quantity,
            unit_price,
            predicted_profit,
            id
        ))

        conn.commit()
        conn.close()

        return redirect("/prediction_history")

    prediction = conn.execute(
        "SELECT * FROM prediction_history WHERE id=?",
        (id,)
    ).fetchone()

    conn.close()

    return render_template(
        "edit_prediction.html",
        prediction=prediction
    )


@app.route("/ai_insights")
def ai_insights():

    if "user" not in session:
        return redirect("/login")

    insights = get_ai_insights()

    print("===================================")
    print(insights)
    print(type(insights["recommendation"]))
    print(insights["recommendation"])
    print(type(insights["summary"]))
    print("===================================")

    return render_template(
        "ai_insights.html",
        insights=insights
    )
@app.route("/forecast")
def forecast():

    if "user" not in session:
        return redirect("/login")

    prediction = predict_next_month_sales()

    return render_template(
        "forecast.html",
        prediction=prediction
    )
@app.route("/test")
def test():
    return "Test Route Working!"

@app.route("/logout")
def logout():

    session.clear()

    return redirect("/")



def open_browser():
    webbrowser.open("http://127.0.0.1:5000")


if __name__ == "__main__":

    print("\n========== REGISTERED ROUTES ==========\n")
    for rule in app.url_map.iter_rules():
        print(rule)

    print("\n=======================================\n")

    # Open browser only on the first start
    if os.environ.get("WERKZEUG_RUN_MAIN") != "true":
        Timer(1, open_browser).start()

    app.run(debug=False)