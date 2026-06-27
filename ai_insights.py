print("***** LOADED ai_insights.py *****")
import sqlite3


def get_ai_insights():

    conn = sqlite3.connect("database/retailiq.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    # Total Revenue
    cursor.execute("""
        SELECT SUM(quantity * unit_price)
        FROM sales
    """)
    total_revenue = cursor.fetchone()[0] or 0

    # Total Profit
    cursor.execute("""
        SELECT SUM(profit)
        FROM sales
    """)
    total_profit = cursor.fetchone()[0] or 0

    # Total Customers
    cursor.execute("""
        SELECT COUNT(*)
        FROM customers
    """)
    total_customers = cursor.fetchone()[0] or 0

    # Total Products
    cursor.execute("""
        SELECT COUNT(*)
        FROM products
    """)
    total_products = cursor.fetchone()[0] or 0

    # Top Selling Product
    cursor.execute("""
        SELECT product_name,
               SUM(quantity) AS total_qty
        FROM sales
        GROUP BY product_name
        ORDER BY total_qty DESC
        LIMIT 1
    """)
    top_product = cursor.fetchone()

    # Highest Profit Product
    cursor.execute("""
        SELECT product_name,
               SUM(profit) AS total_profit
        FROM sales
        GROUP BY product_name
        ORDER BY total_profit DESC
        LIMIT 1
    """)
    profit_product = cursor.fetchone()

    # Best Region
    cursor.execute("""
        SELECT region,
               COUNT(*) AS total
        FROM customers
        GROUP BY region
        ORDER BY total DESC
        LIMIT 1
    """)
    region = cursor.fetchone()

    # Best Category
    cursor.execute("""
        SELECT category,
               COUNT(*) AS total
        FROM products
        GROUP BY category
        ORDER BY total DESC
        LIMIT 1
    """)
    category = cursor.fetchone()

    # Low Stock
    cursor.execute("""
        SELECT COUNT(*)
        FROM products
        WHERE stock < 10
    """)
    low_stock = cursor.fetchone()[0] or 0

    # Average Profit
    cursor.execute("""
        SELECT AVG(profit)
        FROM sales
    """)
    avg_profit = cursor.fetchone()[0] or 0

    conn.close()

    # -------------------------
    # AI Recommendations
    # -------------------------

    recommendations = []

    if low_stock > 0:
        recommendations.append(
            f"⚠️ {low_stock} product(s) have low stock. Restock immediately."
        )

    if total_revenue > 100000:
        recommendations.append(
            "📈 Excellent revenue performance."
        )
    else:
        recommendations.append(
            "📉 Increase sales through promotions."
        )

    if avg_profit > 3000:
        recommendations.append(
            "💰 Profit margin is healthy."
        )
    else:
        recommendations.append(
            "💡 Improve your profit margin."
        )

    if top_product:
        recommendations.append(
            f"🏆 Top Selling Product: {top_product['product_name']}"
        )

    if category:
        recommendations.append(
            f"📂 Best Category: {category['category']}"
        )

    if region:
        recommendations.append(
            f"🌍 Best Region: {region['region']}"
        )
        

    # -------------------------
    # Business Score
    # -------------------------

    business_score = 50

    if total_revenue > 100000:
        business_score += 15

    if total_profit > 30000:
        business_score += 15

    if total_customers > 10:
        business_score += 10

    if total_products > 10:
        business_score += 5

    if low_stock == 0:
        business_score += 5

    if business_score > 100:
        business_score = 100

    # -------------------------
    # Executive Summary
    # -------------------------

    summary = f"""
RetailIQ AI Business Analysis

Business Performance Overview

• Total Revenue: ₹{round(total_revenue,2)}
• Total Profit: ₹{round(total_profit,2)}
• Total Customers: {total_customers}
• Total Products: {total_products}

Top Business Highlights

• Best Selling Product: {top_product['product_name'] if top_product else 'N/A'}
• Highest Profit Product: {profit_product['product_name'] if profit_product else 'N/A'}
• Best Sales Region: {region['region'] if region else 'N/A'}
• Best Category: {category['category'] if category else 'N/A'}

Business Score

AI Business Score: {business_score}/100

Recommendations

- Continue promoting the best-selling product.
- Restock low inventory items immediately.
- Improve profit margin through pricing and cost optimization.
- Increase marketing campaigns in the best-performing region.

Conclusion

The business is generating strong revenue and maintaining stable profitability. Continued focus on inventory management, regional marketing, and high-performing products will help increase future sales and overall business growth.
"""
    print("Recommendation Type:", type(recommendations))
    print("Recommendations:", recommendations)

    print("Summary Type:", type(summary))
    print("Summary:", summary)

    return {

    "total_revenue": round(total_revenue, 2),

    "total_profit": round(total_profit, 2),

    "total_customers": total_customers,

    "total_products": total_products,

    "top_product": top_product["product_name"] if top_product else "N/A",

    "profit_product": profit_product["product_name"] if profit_product else "N/A",

    "best_region": region["region"] if region else "N/A",

    "best_category": category["category"] if category else "N/A",

    "low_stock": low_stock,

    "avg_profit": round(avg_profit, 2),

    "recommendation": recommendations,

    "business_score": business_score,

    "summary": summary

}