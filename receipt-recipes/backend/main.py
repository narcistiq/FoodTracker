from fastapi import FastAPI, UploadFile, File
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pymongo import MongoClient
import os, shutil, subprocess
import ast

from recipes import GeminiClient

app = FastAPI()
origins = [
    "http://localhost:5173"
]

client = MongoClient("mongodb://localhost:27017/")
db = client["recipes_db"]       # database
collection = db["recipes"]      # collection
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins, # React app URL
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
    OCR_PATH = os.path.join(BASE_DIR, "..", "FoodTracker", "ocr-reader.py")

    subprocess.run(["python", "ocr-reader/ocr-reader.py"], check=True)
    subprocess.run(["python", "ocr-reader/data_cleaner.py"], check=True)


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
