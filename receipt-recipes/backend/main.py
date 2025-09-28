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
    CLEANED_FILE_PATH = os.path.join(OCR_DIR, "cleaned_file.txt")
    with open(CLEANED_FILE_PATH, "r") as f:
        contents = f.read().strip()
        
        # Remove markdown code block syntax if present
        if contents.startswith("```python"):
            contents = contents.replace("```python", "").replace("```", "").strip()
        elif contents.startswith("````plaintext\n```python"):
            contents = contents.replace("````plaintext\n```python", "").replace("```\n````", "").strip()
        
        parsed = ast.literal_eval(contents)   # Parse the list from file
        
        # Handle both flat list and nested list formats
        if parsed and isinstance(parsed[0], list):
            # Nested list format: [['tomato', 'onion', 'garlic']]
            ingredients = [item for sublist in parsed for item in sublist]  # flatten
        else:
            # Flat list format: ['diced tomatoes', 'tomato paste', ...]
            ingredients = parsed
        
        print(f"Extracted ingredients: {ingredients}")  # Debug logging

    # 4. Call /recipes/generate internally
    try:
        recipes = generate_recipes(ingredients)
        print(f"Generated recipes: {recipes}")  # Debug logging
        return recipes
    except Exception as e:
        print(f"Error generating recipes: {e}")  # Debug logging
        raise HTTPException(status_code=500, detail=f"Recipe generation failed: {e}")


@app.post("/recipes/generate/")
def generate_recipes(ingredients_text: list[str]):
    '''
        Call AI model, generate recipes based on current ingredients in inventory, 
        and return recipes as json
    '''
    try:
        print(f"Generating recipes for ingredients: {ingredients_text}")  # Debug logging
        
        # TODO: Remove this mock response when API quota is available
        # Mock response for testing
        mock_response = {
            "recipes": [
                {
                    "name": "Tomato Chicken Pasta",
                    "servings": "4",
                    "ingredients": ["diced tomatoes", "boneless chicken breast", "pasta", "garlic"],
                    "substitutions": "Can substitute chicken with impossible burger for vegetarian option"
                },
                {
                    "name": "Bell Pepper Stir Fry",
                    "servings": "2", 
                    "ingredients": ["green bell peppers", "red bell peppers", "organic carrots", "chicken broth"],
                    "substitutions": "Use vegetable broth instead of chicken broth for vegetarian"
                },
                {
                    "name": "Green Bean Casserole",
                    "servings": "6",
                    "ingredients": ["green beans", "organic carrots", "french dressing", "onions"],
                    "substitutions": "None needed - all ingredients available"
                }
            ]
        }
        return mock_response
        
        # Uncomment below when API quota is available:
        # gemini = GeminiClient()
        # gemini.setup(ingredients_text)
        # reply = gemini.ask()
        # print(f"Gemini response: {reply.text}")
        # import json
        # recipes_data = json.loads(reply.text)
        # return recipes_data
    except Exception as e:
        print(f"Gemini API error: {e}")  # Debug logging
        raise HTTPException(status_code=500, detail=f"Gemini API error: {e}")

@app.get("/recipes/")
async def get_recipes():
    # Fetch recipes from mongodb
    # Useful for history view or analytics
    pass
