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
csv_path = Path(r"food-tracker/recipes.csv") 
open_kwargs = {         
    "mode": "r",
    "encoding": "utf-8",
    "newline": "",
}
docs = None
with csv_path.open(**open_kwargs) as file:
    reader = csv.DictReader(file)
    docs = list(reader)
collection.delete_many({})
collection.insert_many(docs)
# for i, doc in enumerate(client["Recipes"]["Recipes"].find(), start=1):
#     print(doc)
#     if i == 10:
#         break    
     
recipes = list(collection.find({}, {"_id": 0}))
print(recipes[:10])

class GeminiClient:
    def __init__(self):
        genai.configure(api_key=os.getenv("APIKEY"))
        self.model = genai.GenerativeModel("gemini-2.0-flash")
        base_prompt = "You have these recipes:\n\n"
        recipe_texts = []
        for num, doc in enumerate(collection.find().limit(10)):
            title = doc.get(title_key, "Untitled")
            # Some CSVs write the ingredients as a string separated by semicolons or commas.
            # If it’s already a string, no need to join; if it’s a list, join it.
            ingredients_raw = doc.get(ingredients_key, "")
            if isinstance(ingredients_raw, list):
                ingredients = ", ".join(ingredients_raw)
            else:
                ingredients = ingredients_raw
            steps = doc.get(instructions_key, "")
            recipe_texts.append(
                f"• {title}\n  Ingredients: {ingredients}\n  Steps: {steps}\n"
            )
        self.context = base_prompt + "\n".join(recipe_texts)

    def ask(self, question: str) -> str:
        prompt = self.context + f"\n\nQuestion: {question}\nAnswer:"
        response: GenerateContentResponse = self.model.generate_content(prompt)
        return response.text


if __name__ == "__main__":
    gemini = GeminiClient()
    reply = gemini.ask("Which recipe uses beef brisket and onions?")
    print(reply)