import google.generativeai as genai
from google.generativeai.types import GenerateContentResponse


genai.configure(api_key="AIzaSyBCn45I0DUKZFUkHYaARAMzTe8EET_IWD0")


class GeminiClient:
    def __init__(self):
        # Create an instance of the model you want to use.
        # The correct class is GenerativeModel.
        self.model = genai.GenerativeModel("gemini-2.5-flash") # Using 1.5-flash as it's a common, solid choice
        self.response: GenerateContentResponse | None = None

    def give_context(self, prompt: str) -> GenerateContentResponse:
        """Ask the model a question and store the reply."""
        # Call generate_content directly on the model instance.
        self.response = self.model.generate_content(prompt)
        return self.response


# --- Example Usage ---
if __name__ == "__main__":
    my_client = GeminiClient()
    response = my_client.give_context("Do you work?")
    print(response.text)
    