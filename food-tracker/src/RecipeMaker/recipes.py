import google.generativeai as genai
from google.generativeai.types import GenerateContentResponse
import os
from dotenv import load_dotenv
import csv
from pymongo import MongoClient
load_dotenv()
genai.configure(api_key=(os.getenv("APIKEY")))

client = MongoClient("mongodb://localhost:27017/")
csv_file = (r"recipes.csv")

db = client["Recipes"]
collection = db["Recipes"]


with open(csv_file, "r") as file:
    reader = csv.DictReader(file)
    for row in reader:
        collection.insert_one(row)
        
for i, j in collection.find():
    print(j)
    if i == 10:
        break
    
    
class GeminiClient:
    def __init__(self):
        # Create an instance of the model you want to use.
        # The correct class is GenerativeModel.
        self.model = genai.GenerativeModel("gemini-2.5-flash")
        self.response: GenerateContentResponse | None = None

    def give_context(self, prompt: str) -> GenerateContentResponse:
        """Ask the model a question and store the reply."""
        # Call generate_content directly on the model instance.
        self.response = self.model.generate_content(prompt)
        return self.response


# # --- Example Usage ---
# if __name__ == "__main__":
#     my_client = GeminiClient()
#     response = my_client.give_context("Do you work?")
#     print(response.text)
    