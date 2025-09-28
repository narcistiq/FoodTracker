from fastapi import FastAPI, UploadFile, File
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pymongo import MongoClient
import os, shutil

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
    return {"filename": file.filename, "saved_to": file_path}

@app.post("/recipes/generate/")
async def generate_recipes():
    '''
        Call AI model, generate recipes based on current ingredients in inventory, 
        and return recipes as json
    '''
    gemini = GeminiClient()
    gemini.setup() #THIS TAKES IN A LIST, ADJUST IF NEEDED
    reply = gemini.ask()
    # print(reply)
    pass

@app.get("/recipes/")
async def get_recipes():
    # Fetch recipes from mongodb
    # Useful for history view or analytics
    pass
