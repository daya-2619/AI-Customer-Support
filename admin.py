import streamlit as st
import sqlite3

st.title("📊 Admin Dashboard - Orders")

conn = sqlite3.connect("orders.db")
cursor = conn.cursor()

cursor.execute("SELECT * FROM orders")
orders = cursor.fetchall()

st.subheader("📦 All Orders")

for order in orders:
    order_id, user_id, status, location, eta, created_at = order

    st.markdown(f"""
**Order ID:** {order_id}  
User: {user_id}  
Status: {status}  
Location: {location}  
ETA: {eta}  
Created: {created_at}
---
""")

# 🔥 Manual status update
st.subheader("🔧 Update Order Status")

order_id = st.text_input("Order ID")
new_status = st.selectbox("New Status", ["Shipped", "In Transit", "Out for delivery", "Delivered", "Cancelled"])

if st.button("Update"):
    conn = sqlite3.connect("orders.db")
    cursor = conn.cursor()
    cursor.execute("UPDATE orders SET status=? WHERE order_id=?", (new_status, order_id))
    conn.commit()
    conn.close()

    st.success(f"✅ Order {order_id} updated to {new_status}")