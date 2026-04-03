import sqlite3
from datetime import datetime

def init_db():
    conn = sqlite3.connect("orders.db")
    cursor = conn.cursor()

    # 🔥 FINAL TABLE (6 columns)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS orders (
        order_id TEXT PRIMARY KEY,
        user_id TEXT,
        status TEXT,
        location TEXT,
        eta TEXT,
        created_at TEXT
    )
    """)

    # 🔥 CORRECT INSERT
    cursor.execute("""
    INSERT OR IGNORE INTO orders VALUES (?, ?, ?, ?, ?, ?)
    """, (
        '12345',
        '101',
        'Shipped',
        'Jamshedpur',
        '2026-04-06',
        datetime.now().isoformat()
    ))

    conn.commit()
    conn.close()


def get_order(order_id):
    conn = sqlite3.connect("orders.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM orders WHERE order_id=?", (order_id,))
    result = cursor.fetchone()

    conn.close()
    return result


def update_order_status(order_id, status):
    conn = sqlite3.connect("orders.db")
    cursor = conn.cursor()

    cursor.execute("UPDATE orders SET status=? WHERE order_id=?", (status, order_id))

    conn.commit()
    conn.close()


def auto_update_status(order):
    from datetime import datetime

    order_id, user_id, status, location, eta, created_at = order

    created_time = datetime.fromisoformat(created_at)
    now = datetime.now()
    diff = (now - created_time).seconds

    if diff > 60 and status == "Shipped":
        return "In Transit"
    elif diff > 120 and status == "In Transit":
        return "Out for delivery"
    elif diff > 180 and status == "Out for delivery":
        return "Delivered"

    return status