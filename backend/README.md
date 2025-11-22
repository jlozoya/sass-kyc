# 🔧 Backend Setup (FastAPI + MongoDB)

This backend uses **FastAPI**, **Motor** (async MongoDB driver), and **Pydantic v2**.
Follow the steps below to install dependencies, configure MongoDB, and start the API server.

---

## 📦 1. Install Python dependencies

Create and activate a virtual environment:

```bash
python -m venv .venv
.\.venv\Scripts\activate   # Windows
# source .venv/bin/activate  # Linux/Mac
```

Install required packages:

```bash
pip install -r requirements.txt
```

---

## 🗄️ 2. Configure MongoDB

Open the Mongo shell and create the database and application user:

```bash
mongosh

use sasskyc

db.createUser({
  user: "sasskyc",
  pwd: "CHANGE_THIS_PASSWORD!!!",
  roles: [
    { role: "readWrite", db: "sasskyc" }
  ]
})
```

Update your `.env` file (inside `backend/`) with your connection details:

```env
MONGODB_URI=mongodb://sasskyc:CHANGE_THIS_PASSWORD!!!@127.0.0.1:27017/sasskyc?authSource=sasskyc
MONGODB_DB_NAME=sasskyc
```

---

## 🔍 3. Test MongoDB connection

Run the diagnostic script to confirm the backend can connect to MongoDB:

```bash
python tests/test_mongo.py
```

If the output shows a list (even an empty one), the connection is working.

---

## 🚀 4. Start the FastAPI server

Run Uvicorn with auto-reload for local development:

```bash
python -m uvicorn app.main:app --reload --port 8000
```

The API will be available at:

* **Base URL:** [http://127.0.0.1:8000](http://127.0.0.1:8000)
* **Swagger Docs:** [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
* **ReDoc:** [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

