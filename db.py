users = {
    "101": {"name": "Daya", "order_status": "Shipped"},
    "102": {"name": "Rahul", "order_status": "Processing"}
}

def get_user(user_id):
    return users.get(user_id, {"name": "Unknown", "order_status": "Not Found"})