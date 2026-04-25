"""Google Gemini API client wrapper."""

import json
from typing import Dict, Any, Optional
import google.genai as genai
from config.settings import GEMINI_API_KEY, GEMINI_MODEL, GEMINI_MAX_TOKENS, GEMINI_TEMPERATURE
from core.exceptions import GeminiAPIError


class GeminiClient:
    """Wrapper for Google Gemini API."""

    def __init__(self):
        if not GEMINI_API_KEY:
            raise ValueError("GEMINI_API_KEY not configured")

        self.client = genai.Client(api_key=GEMINI_API_KEY)
        self.model = GEMINI_MODEL
        self.max_tokens = GEMINI_MAX_TOKENS
        self.temperature = GEMINI_TEMPERATURE

    def generate_response(self, prompt: str, system_prompt: Optional[str] = None) -> str:
        """
        Generate a response from Gemini.

        Args:
            prompt: The user prompt
            system_prompt: Optional system instructions

        Returns:
            Generated response text

        Raises:
            GeminiAPIError: If API call fails
        """
        try:
            # Create full prompt with system instructions if provided
            full_prompt = prompt
            if system_prompt:
                full_prompt = f"{system_prompt}\n\n{prompt}"

            # Configure the model
            config = genai.types.GenerateContentConfig(
                temperature=self.temperature,
                max_output_tokens=self.max_tokens,
            )

            # Generate response
            response = self.client.models.generate_content(
                model=self.model,
                contents=full_prompt,
                config=config
            )

            return response.text

        except Exception as e:
            raise GeminiAPIError(f"Gemini API error: {e}")

    def generate_structured_response(self, prompt: str, system_prompt: Optional[str] = None) -> Dict[str, Any]:
        """
        Generate a structured JSON response from Gemini.

        Args:
            prompt: The user prompt with JSON formatting instructions
            system_prompt: Optional system instructions

        Returns:
            Parsed JSON response

        Raises:
            GeminiAPIError: If API call fails or JSON parsing fails
        """
        try:
            # Enhanced prompt for JSON output
            json_prompt = f"""{system_prompt or ""}

Please respond with a valid JSON object that matches the expected structure.

{prompt}

IMPORTANT: Your response must be valid JSON only, with no additional text or formatting."""

            # Configure for JSON output
            config = genai.types.GenerateContentConfig(
                temperature=self.temperature,
                max_output_tokens=self.max_tokens,
                response_mime_type="application/json",
            )

            # Generate response
            response = self.client.models.generate_content(
                model=self.model,
                contents=json_prompt,
                config=config
            )

            response_text = response.text.strip()

            # Parse JSON response
            try:
                return json.loads(response_text)
            except json.JSONDecodeError as e:
                raise GeminiAPIError(f"Invalid JSON response from Gemini: {response_text[:200]}... Error: {e}")

        except Exception as e:
            if isinstance(e, GeminiAPIError):
                raise
            raise GeminiAPIError(f"Gemini API error: {e}")