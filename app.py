from fastapi import FastAPI
import re
from deep_translator import GoogleTranslator
from rag import create_vector_store, get_context
from db import get_user
from database import get_order, update_order_status, init_db, auto_update_status
import requests
import os
from dotenv import load_dotenv
from openai import OpenAI


loaded = load_dotenv()
print("dotenv loaded:", loaded)

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

print("OPENAI KEY:", "OK" if os.getenv("OPENAI_API_KEY") else "MISSING")
# Initialize DB
init_db()

app = FastAPI()

# Load vector DB
vector_db = create_vector_store()

# Memory
chat_histories = {}
user_sessions = {}


# 🌍 Detect Language
def detect_language(text):
    if any("\u0980" <= c <= "\u09FF" for c in text):
        return "bn"
    elif any("\u0900" <= c <= "\u097F" for c in text):
        return "hi"
    return "en"


# 🌐 Translate
def translate_text(text, target_lang):
    if target_lang == "en":
        return text
    try:
        return GoogleTranslator(source='auto', target=target_lang).translate(text)
    except:
        return text


# 🔍 Intent detection
def detect_intent(query: str):
    q = query.lower()

    if "track" in q or "where is my order" in q:
        return "track_order"
    elif "cancel" in q:
        return "cancel_order"
    elif "refund" in q:
        return "refund_policy"
    elif "return" in q:
        return "return_order"
    elif "agent" in q or "human" in q:
        return "human_handoff"
    else:
        return "general"

def openai_generate(prompt):
    try:
        resp = client.chat.completions.create(
            model="gpt-4o-mini",  # cheap + fast
            messages=[
                {"role": "system", "content": "You are a helpful customer support assistant."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.5,
            max_tokens=300
        )
        return resp.choices[0].message.content.strip()

    except Exception as e:
        return f"⚠️ OpenAI error: {str(e)}"
    
# 🔍 Extract order ID
def extract_order_id(query):
    match = re.search(r"\b\d{4,}\b", query)
    return match.group() if match else None


@app.get("/")
def home():
    return {"message": "Customer Support Bot Running"}


@app.get("/chat")
def chat(query: str, user_id: str = "101"):
    try:
        user = get_user(user_id)

        # 🌍 Detect language
        lang = detect_language(query)

        # Translate to English
        query_en = translate_text(query, "en") if lang != "en" else query

        # Init memory
        if user_id not in chat_histories:
            chat_histories[user_id] = []

        if user_id not in user_sessions:
            user_sessions[user_id] = {"order_id": None}

        # Detect intent
        intent = detect_intent(query_en)

        # Extract order ID
        extracted_id = extract_order_id(query_en)
        if extracted_id:
            user_sessions[user_id]["order_id"] = extracted_id

        order_id = user_sessions[user_id]["order_id"]

        # =========================
        # 📦 ORDER TRACKING
        # =========================
        if intent == "track_order":
            if not order_id:
                return {"response": translate_text("Sure! Please provide your order ID 😊", lang)}

            order = get_order(order_id)

            if not order:
                return {"response": translate_text(f"No order found with ID {order_id}", lang)}

            # Auto update
            new_status = auto_update_status(order)

            if new_status != order[2]:
                update_order_status(order_id, new_status)

            order = get_order(order_id)

            _, _, status, location, eta = order

            response_text = f"""📦 Order #{order_id}
🚚 Status: {status}
📍 Location: {location}
📅 Expected Delivery: {eta}

Want me to notify you when it arrives?"""

            return {"response": translate_text(response_text, lang)}

        # =========================
        # ❌ CANCEL ORDER
        # =========================
        elif intent == "cancel_order":
            if not order_id:
                return {"response": translate_text("Please provide your order ID", lang)}

            order = get_order(order_id)

            if not order:
                return {"response": translate_text(f"Order {order_id} not found", lang)}

            status = order[2]

            if status.lower() == "out for delivery":
                text = f"""Cannot cancel order #{order_id}
Already out for delivery

Would you like to request a return instead?"""
                return {"response": translate_text(text, lang)}

            update_order_status(order_id, "Cancelled")

            return {"response": translate_text(f"Order #{order_id} has been cancelled successfully", lang)}

        # =========================
        # 🔁 RETURN ORDER
        # =========================
        elif intent == "return_order":
            if not order_id:
                return {"response": translate_text("Please provide your order ID", lang)}

            order = get_order(order_id)

            if not order:
                return {"response": translate_text(f"Order {order_id} not found", lang)}

            update_order_status(order_id, "Return Requested")

            text = f"""Return initiated for order #{order_id}
Pickup will be scheduled soon

You’ll receive SMS confirmation shortly."""

            return {"response": translate_text(text, lang)}

        # =========================
        # 💰 REFUND POLICY (RAG)
        # =========================
        elif intent == "refund_policy":
            context = get_context(query_en, vector_db)

            text = f"""Refund Policy:

{context}

Need help initiating a refund?"""

            return {"response": translate_text(text, lang)}

        # =========================
        # 👨‍💼 HUMAN HANDOFF
        # =========================
        elif intent == "human_handoff":
            text = """I understand your concern
Connecting you to a support agent...

Your chat history will be shared automatically."""
            return {"response": translate_text(text, lang)}

        # =========================
        # 🤖 GENERAL
        # =========================
        else:
            context = get_context(query_en, vector_db)

            prompt = f"""
You are a smart and friendly customer support assistant.

Respond in {lang} language.

User Info: {user}

Context:
{context}

Conversation History:
{chat_histories[user_id][-5:]}

User Question: {query_en}

Give a helpful, short and human-like answer.
"""

            
            reply = openai_generate(prompt)

            if not reply:
                reply = "Sorry, I will create a support ticket for you."

            # Translate back
            reply = translate_text(reply, lang)

            # Save history
            chat_histories[user_id].append({"role": "user", "content": query})
            chat_histories[user_id].append({"role": "assistant", "content": reply})

            return {"response": reply}

    except Exception as e:
        return {"error": str(e)}