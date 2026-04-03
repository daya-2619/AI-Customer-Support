def detect_intent(query: str):
    q = query.lower()

    if any(x in q for x in ["track", "where is my order", "order status"]):
        return "track_order"

    elif any(x in q for x in ["cancel", "cancel order"]):
        return "cancel_order"

    elif any(x in q for x in ["refund"]):
        return "refund_policy"

    elif any(x in q for x in ["return"]):
        return "return_order"

    elif any(x in q for x in ["agent", "human"]):
        return "human_handoff"

    return "general"