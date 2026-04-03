# 🤖 AI Customer Support Chatbot (RAG + OpenAI)

An **intelligent, production-ready customer support chatbot** powered by **Retrieval-Augmented Generation (RAG)**, **FastAPI**, and **OpenAI GPT models**.

🚀 Designed to simulate real-world enterprise customer support systems with **order tracking, automation, and contextual intelligence**.

---

## 🌟 Features

### 🧠 AI-Powered Responses

* Uses OpenAI (`gpt-4o-mini`) for fast and accurate answers
* Context-aware conversation handling
* Natural, human-like replies

### 📦 Order Management System

* Track order status
* Cancel orders
* Return request handling
* Real-time status updates (simulation)

### 🔍 RAG (Retrieval-Augmented Generation)

* Retrieves answers from FAQ / documents
* Uses embeddings + vector search (FAISS)
* Reduces hallucination

### 💬 Smart Conversation

* Remembers previous user inputs
* Handles "same as before" queries
* Intent detection system

### 🌐 Multilingual Support

* English 🇬🇧
* Hindi 🇮🇳
* Bengali 🇧🇩

### ⚙️ Automation

* Auto-update delivery status
* Ticket generation fallback
* Human handoff simulation

---

## 🏗️ Tech Stack

| Layer      | Technology         |
| ---------- | ------------------ |
| Backend    | FastAPI            |
| AI Model   | OpenAI GPT-4o-mini |
| RAG        | LangChain + FAISS  |
| Database   | SQLite             |
| Frontend   | Streamlit          |
| Deployment | Render             |

---

## 📂 Project Structure

```bash
customer-support-bot/
│
├── app.py              # Main FastAPI backend
├── rag.py              # RAG logic (embeddings + search)
├── database.py         # Order database (SQLite)
├── db.py               # User data simulation
├── ui.py               # Streamlit frontend
├── data/
│   └── faq.txt         # Knowledge base
├── requirements.txt
├── .env                # API keys (ignored)
└── README.md
```

---

## 🔐 Environment Setup

Create a `.env` file:

```env
OPENAI_API_KEY=your_api_key_here
```

---

## ⚙️ Installation & Run

```bash
# Install dependencies
pip install -r requirements.txt

# Run backend
uvicorn app:app --reload

# Run frontend (optional)
streamlit run ui.py
```

---

## 🌍 Deployment (Render)

1. Push project to GitHub
2. Go to Render → New Web Service
3. Use:

```bash
Build: pip install -r requirements.txt
Start: uvicorn app:app --host 0.0.0.0 --port 10000
```

4. Add environment variable:

```
OPENAI_API_KEY=your_key
```

---

## 🧪 Example Queries

* `Where is my order?`
* `Cancel my order`
* `Return my order`
* `What is your refund policy?`
* `Mera order kahan hai?`
* `Amar order kothai?`

---

## 📊 API Example

```json
{
  "query": "Where is my order?",
  "user_id": "101"
}
```

Response:

```json
{
  "response": "📦 Order #12345 is out for delivery..."
}
```

---

## 🔒 Security

* API keys stored in `.env`
* `.env` excluded via `.gitignore`
* Rate limiting & validation applied

---

## 🚀 Future Improvements

* 🔐 Authentication system (JWT)
* 💳 SaaS billing integration
* 📊 Admin dashboard analytics
* 📲 WhatsApp / Telegram bot integration
* 🧠 Fine-tuned domain models

---

## 🧠 Learning Outcomes

* RAG architecture implementation
* LLM API integration
* FastAPI backend design
* Real-world AI system architecture
* Deployment & DevOps basics

---

## 👨‍💻 Author

**Dayamay Das**
Aspiring AI/ML Engineer 🚀

---

## ⭐ Support

If you like this project:

👉 Star the repo
👉 Share with others
👉 Use it in your portfolio

---

## 💣 Final Note

This is not just a chatbot —
👉 It’s a **mini AI SaaS product prototype**.

🔥 Built with real-world architecture principles.
