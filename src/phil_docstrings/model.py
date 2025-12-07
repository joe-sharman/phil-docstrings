import os
from typing import Optional, Protocol

import google.generativeai as genai


class Model(Protocol):
    """Protocol for defining interaction with model providers
    allows easy testing with new providers in future."""

    def generate(self, prompt: str) -> str:
        pass


class GeminiModel:

    def __init__(self, token: str):
        genai.configure(api_key=token)

    def generate(self, prompt: str) -> str:
        model = genai.GenerativeModel("gemini-2.0-flash-exp")
        response = model.generate_content(prompt)
        return response.text
