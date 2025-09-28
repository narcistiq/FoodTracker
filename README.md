# FoodTracker

A receipt-to-recipe generator that uses OCR to extract ingredients from grocery receipts and generates personalized recipes using AI.

## 📋 Prerequisites

Make sure you have the following installed on your system:

- **Python 3.8+**
- **Node.js 16+** 
- **npm** as the package manager
- **MongoDB** (for recipe storage)

## 🚀 Setup Instructions

### 1. Clone the Repository
```bash
git clone https://github.com/narcistiq/FoodTracker.git
cd FoodTracker
```

### 2. Backend Setup

#### Navigate to Backend Directory
```bash
cd receipt-recipes/backend
```

#### Install Python Dependencies
```bash
pip3 install -r requirements.txt
```

#### Environment Configuration
Create `.env` files with your Gemini API key:

**Backend configuration:**
```bash
# In receipt-recipes/.env
GEMINI_API_KEY=your_gemini_api_key_here
```

**OCR configuration:**
```bash
# In ocr-reader/.env
GEMINI_API_KEY=your_gemini_api_key_here
```

#### Start the Backend Server
```bash
uvicorn main:app --reload --port 8000
```

The backend will be available at: `http://127.0.0.1:8000`

### 3. Frontend Setup

#### Navigate to Frontend Directory (in a new terminal)
```bash
cd receipt-recipes/frontend
```

#### Install Node Dependencies
```bash
npm install
```

#### Start the Frontend Development Server
```bash
npm run dev
```

The frontend will be available at: `http://localhost:5173`

## 🧪 Testing

1. **Backend API**: Visit `http://127.0.0.1:8000/docs` for FastAPI interactive documentation
2. **Upload Test**: Use the frontend to upload a receipt image
3. **Example Files**: Test with images in `receipt-recipes/backend/uploads/`

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

