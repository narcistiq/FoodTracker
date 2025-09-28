import google.generativeai as genai
from google.generativeai.types import GenerateContentResponse
import os
from dotenv import load_dotenv
import csv
from pymongo import MongoClient
from pathlib import Path

load_dotenv()

client = MongoClient("mongodb://localhost:27017")

db = client["Recipes"]
collection = db["Recipes"]
csv_path = Path(r"../../Receipes from around the world.csv") 
open_kwargs = {         
    "mode": "r",
    "encoding": "utf-8",
    "newline": "",
}
rows = None
with csv_path.open(encoding="cp1252") as f:      # Windows‑1252 (aka Latin‑1)
    reader = csv.DictReader(f)
    rows = list(reader)
    
collection.delete_many({})
collection.insert_many(rows)
# for i, doc in enumerate(client["Recipes"]["Recipes"].find(), start=1):
#     print(doc)
#     if i == 10:
#         break    
     
recipes = list(collection.find({}, {"_id": 0}))
#print(recipes[:10])

class GeminiClient:
    def __init__(self):
        genai.configure(api_key=os.getenv("APIKEY"))
        self.model = genai.GenerativeModel(
            "gemini-2.0-flash",
            config={
                "response_mime_type": "application/json",  # <-- comma added
                "response_schema": [
                    "Name",
                    "Servings",
                    "Ingredients",
                    "Necessary Substitutions",
                ],
            },
        )

    def setup(self, actualingredients: list):
        base_prompt = "You have these recipes:\n\n"
        base_prompt += "You have these ingredients" + actualingredients
        recipe_texts = []
        for doc in recipes[0]:
            title = doc.get("title", "")
            ingredients = doc.get("ingredients", "")
            steps = doc.get("servings", "")
            recipe_texts.append(f"• {title} Ingredients: {ingredients}\Servings: {steps}")
            # print(ingredients) # debugging only
            self.context = base_prompt + "\n".join(recipe_texts)

    def ask(self):
        question = "Please choose at least 3 recipes that contain these items. Make the necessary substitions as needed. Ignore any words that are not abbreviated ingredients."
        prompt = self.context + f"\n\nQuestion: {question}\nAnswer:"
        response: GenerateContentResponse = self.model.generate_content(prompt)
        return response


