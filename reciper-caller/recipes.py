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
csv_path = Path(r"Receipes from around the world.csv") 
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
        self.model = genai.GenerativeModel("gemini-2.0-flash")
        base_prompt = "You have these recipes:\n\n"
        recipe_texts = []
        for num, doc in enumerate(recipes):
            title = doc.get("title", "")
            ingredients = doc.get("ingredients", "")
            steps = doc.get("servings", "")
            recipe_texts.append(f"• {title}\n  Ingredients: {ingredients}\Servings: {steps}\n")
            print(ingredients)
            if num == 50:   # ten items total
                break
            self.context = base_prompt + "\n".join(recipe_texts)

    def ask(self, question: str) -> str:
        prompt = self.context + f"\n\nQuestion: {question}\nAnswer:"
        response: GenerateContentResponse = self.model.generate_content(prompt)
        return response.text


if __name__ == "__main__":
    gemini = GeminiClient()
    reply = gemini.ask("Which recipe uses onions or some kind of beef? As long as it has those it should be fine.")
    print(reply)