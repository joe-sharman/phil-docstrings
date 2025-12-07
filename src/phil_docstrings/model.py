from typing import Protocol

from google import genai
import time


class Model(Protocol):
    """Protocol for defining interaction with model providers
    allows easy testing with new providers in future."""

    def generate(self, prompt: str) -> str:
        pass


class GeminiModel:

    def __init__(self, token: str):
        self.client = genai.Client(api_key=token)
        self.model = "gemini-2.5-flash-lite"

    def generate(self, prompt: str) -> str:
        try:
            response = self.client.models.generate_content(model=self.model, contents=prompt)
        except Exception:
            # Basic exception handling for rate limits
            time.sleep(60)
            response = self.client.models.generate_content(model=self.model, contents=prompt)
        return response.text
