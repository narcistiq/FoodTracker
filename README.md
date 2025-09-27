# FoodTracker


# Backend Setup
- pip3 install -r requirements.txt
- cd receipt-recipes
- uvicorn main:app --reload --port 8000
- open http://127.0.0.1:8000/uploads/grocery.jpg for example file

Here’s a tight summary of your project idea and stack:

---

## 📌 Project Idea

* Users upload **receipts** (images) via drag-and-drop.
* Backend extracts an **ingredient list** (OCR / parsing).
* Ingredients are passed to an **AI model** → generates **custom recipes**.
* Recipes are **returned as JSON** to the user and can be **stored in MongoDB** for history, analytics, or reuse.
* A simple **frontend** (HTML/JS) lets users upload files and view results.

---

## ⚙️ Tech Stack

* **Frontend**:

  * Static HTML/CSS/JS (drag-and-drop upload).

* **Backend**:

  * **FastAPI** (Python) → handles uploads, routes, AI integration.
  * **Uvicorn** → ASGI server.

* **Database**:

  * **MongoDB** → stores ingredients + generated recipes.

* **AI Integration**:

  * LLM (e.g., OpenAI, local model, or similar) to generate recipe text from ingredient lists.

* **File Handling**:

  * Local `uploads/` directory for storing receipt images.
  * OCR library (e.g., **Tesseract / pytesseract**) to extract text from receipts.

