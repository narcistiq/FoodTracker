from fastapi import FastAPI, UploadFile, File
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pymongo import MongoClient
import os, shutil, subprocess
import ast
from fastapi import HTTPException

from recipes import GeminiClient

app = FastAPI()
origins = [
    "http://localhost:5173",   # Vite
    "http://127.0.0.1:5173",
    "http://localhost:3000",   # CRA
    "http://127.0.0.1:3000",
]

client = MongoClient("mongodb://localhost:27017/")
db = client["recipes_db"]       # database
collection = db["recipes"]      # collection
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.get("/")
async def main():
    return {"message": "Hello World"}

@app.post("/uploads/")
async def upload_receipt(file: UploadFile = File(...)):
    file_path = os.path.join(UPLOAD_DIR, file.filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # backend/
    ROOT_DIR = os.path.abspath(os.path.join(BASE_DIR, "..", ".."))
    OCR_DIR = os.path.join(ROOT_DIR,"ocr-reader")

    OCR_PATH = os.path.join(OCR_DIR, "ocr-reader.py")
    DATA_CLEANER_PATH = os.path.join(OCR_DIR, "data_cleaner.py")

    try:
        subprocess.run(["python", OCR_PATH], check=True)
        subprocess.run(["python", DATA_CLEANER_PATH], check=True)
    except subprocess.CalledProcessError as e:
            # This happens if the script exits with a non-zero status
            raise HTTPException(status_code=500, detail=f"OCR script failed: {e}")
    except FileNotFoundError as e:
            # This happens if the path to the script is wrong
            raise HTTPException(status_code=500, detail=f"Script not found: {e}")
    except Exception as e:
            # Catch anything else
            raise HTTPException(status_code=500, detail=f"Unexpected error: {e}")


    # 3. Read processed output
    with open("ocr-reader/cleaned_file.txt", "r") as f:
        contents = f.read().strip()
        parsed = ast.literal_eval(contents)   # [['tomato', 'onion', 'garlic']]
        ingredients = [item for sublist in parsed for item in sublist]  # flatten

    # 4. Call /recipes/generate internally
    recipes = generate_recipes(ingredients)

    return recipes


@app.post("/recipes/generate/")
async def generate_recipes(ingredients_text: list[str]):
    '''
        Call AI model, generate recipes based on current ingredients in inventory, 
        and return recipes as json
    '''
    gemini = GeminiClient()
    gemini.setup(ingredients_text) # THIS TAKES IN A LIST, ADJUST IF NEEDED
    reply = gemini.ask()
    return {"recipes": reply.text}

@app.get("/recipes/")
async def get_recipes():
    # Fetch recipes from mongodb
    # Useful for history view or analytics
    pass
