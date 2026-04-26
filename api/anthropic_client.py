"""Anthropic API client wrapper."""

import json
from typing import Any, Dict, Optional

import anthropic

from config.settings import (
    ANTHROPIC_API_KEY,
    CLAUDE_MAX_TOKENS,
    CLAUDE_MODEL,
    CLAUDE_TEMPERATURE,
)
from core.exceptions import AnthropicAPIError


class AnthropicClient:
    """Wrapper for Anthropic Claude API."""

    def __init__(self):
        if not ANTHROPIC_API_KEY:
            raise ValueError("ANTHROPIC_API_KEY not configured")

        self.client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)
        self.model = CLAUDE_MODEL
        self.max_tokens = CLAUDE_MAX_TOKENS
        self.temperature = CLAUDE_TEMPERATURE

    def generate_response(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
    ) -> str:
        """
        Generate a response from Claude.

        Args:
            prompt: The user prompt
            system_prompt: Optional system prompt
            temperature: Override default temperature
            max_tokens: Override default max tokens

        Returns:
            Claude's response text

        Raises:
            AnthropicAPIError: If API call fails
        """
        try:
            # Prepare messages
            messages = [{"role": "user", "content": prompt}]

            # Make API call
            response = self.client.messages.create(
                model=self.model,
                max_tokens=max_tokens or self.max_tokens,
                temperature=temperature or self.temperature,
                system=system_prompt,
                messages=messages,
            )

            return response.content[0].text

        except anthropic.APIError as e:
            raise AnthropicAPIError(f"Claude API error: {e}", status_code=e.status_code)
        except Exception as e:
            raise AnthropicAPIError(f"Unexpected error calling Claude API: {e}")

    def generate_structured_response(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        response_format: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """
        Generate a structured JSON response from Claude.

        Args:
            prompt: The user prompt
            system_prompt: Optional system prompt
            response_format: Expected response structure

        Returns:
            Parsed JSON response

        Raises:
            AnthropicAPIError: If API call fails or JSON parsing fails
        """
        # Add JSON formatting instructions to system prompt
        json_instructions = """
        You must respond with valid JSON only. Do not include any text before or after the JSON.
        Ensure the JSON is properly formatted and matches the expected schema.
        """

        if system_prompt:
            system_prompt = system_prompt + "\n\n" + json_instructions
        else:
            system_prompt = json_instructions

        response_text = self.generate_response(prompt, system_prompt)

        try:
            # Try to extract JSON from response
            json_start = response_text.find("{")
            json_end = response_text.rfind("}") + 1

            if json_start >= 0 and json_end > json_start:
                json_str = response_text[json_start:json_end]
                return json.loads(json_str)
            else:
                raise ValueError("No JSON object found in response")

        except json.JSONDecodeError as e:
            raise AnthropicAPIError(f"Failed to parse Claude response as JSON: {e}")

    def estimate_tokens(self, text: str) -> int:
        """
        Estimate the number of tokens in a text string.
        This is a rough approximation.

        Args:
            text: Input text

        Returns:
            Estimated token count
        """
        # Rough approximation: 1 token ≈ 4 characters for English text
        return len(text) // 4
