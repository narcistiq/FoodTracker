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
with csv_path.open(**open_kwargs) as file:
    reader = csv.DictReader(file)
    docs = list(reader)

collection.insert_many(docs)
# for i, doc in enumerate(client["Recipes"]["Recipes"].find(), start=1):
#     print(doc)
#     if i == 10:
#         break    
recipes = list(collection.find({}, {"_id": 0}))
 
    
class GeminiClient:
    def __init__(self):
        # Create an instance of the model you want to use.
        # The correct class is GenerativeModel.
        genai.configure(api_key=(os.getenv("APIKEY")))
        self.model = genai.GenerativeModel("gemini-2.0-flash")
        self.response: GenerateContentResponse | None = None
        base_prompt = "You have these recipes:\n\n"
        recipe_texts = []
        for num, doc in enumerate(recipes):
            # Example formatting – customise to your schema
            title = doc.get("title", "Untitled")
            ingredients = ", ".join(doc.get("ingredients", []))
            steps = doc.get("instructions", "")
            recipe_texts.append(f"• {title}\n  Ingredients: {ingredients}\n" + "Steps: {steps}\n")
            if num == 10:
                break
        self.context = base_prompt + "\n".join(recipe_texts)

    def ask(self, question: str):
        """Ask Gemini a new question, but keep the database context."""
        prompt = self.context + f"\n\nQuestion: {question}\nAnswer:"
        response = self.model.generate_content(prompt)
        return response.text


if __name__ == "__main__":
    gemini = GeminiClient()
    reply = gemini.ask("Which recipe uses beef brisket and onions?")
    print(reply)