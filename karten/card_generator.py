"""
Card generator using Google GenAI
"""

from google import genai
from google.genai import types

from .card import Card, CardError
from .prompt import CardPrompt


class CardGenerator:
    """Generates flashcards using Google GenAI"""

    def __init__(self, api_key: str, model_name: str):
        self.client = genai.Client(api_key=api_key)
        self.model_name = model_name
        self.config = types.GenerateContentConfig(
            response_mime_type="application/json",
            response_schema=Card,
        )

    def _prepare_prompt(self, word: str, lang: str) -> str:
        """Prepares the prompt for a given word and language"""
        return CardPrompt[lang.upper()].value + f"\n\nWord: {word}"

    def generate_content(self, prompt: str) -> str:
        """Generate content using the configured model"""
        response = self.client.models.generate_content(
            model=self.model_name,
            contents=prompt,
            config=self.config,
        )
        if response.text is None:
            raise CardError("No response text from model")
        return response.text

    def collect(self, word: str, lang: str) -> Card:
        """Creates a card for the given word using the LLM"""
        prompt = self._prepare_prompt(word, lang)
        response_text = self.generate_content(prompt)
        return Card.from_json(response_text)
