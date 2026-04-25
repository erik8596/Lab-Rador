"""Protocol generation agent."""

import json
from typing import Dict, Any, Optional
from api.gemini_client import GeminiClient
from api.anthropic_client import AnthropicClient
from core.models import Protocol
from core.exceptions import ProtocolGenerationError
from config.settings import GEMINI_API_KEY, ANTHROPIC_API_KEY, DEMO_MODE


class ProtocolGenerator:
    """Agent that converts natural language descriptions into structured lab protocols."""

    def __init__(self):
        # Use Gemini (free) if available, otherwise Claude (paid), otherwise demo mode
        if DEMO_MODE:
            self.client = None  # Demo mode
        elif GEMINI_API_KEY:
            self.client = GeminiClient()
            self.client_type = "gemini"
        elif ANTHROPIC_API_KEY:
            self.client = AnthropicClient()
            self.client_type = "anthropic"
        else:
            raise ValueError("No API client available")

    def generate_protocol(self, description: str) -> Protocol:
        """
        Generate a structured lab protocol from a natural language description.

        Args:
            description: Natural language description of the lab procedure

        Returns:
            Protocol object with structured step-by-step instructions

        Raises:
            ProtocolGenerationError: If protocol generation fails
        """
        if DEMO_MODE:
            return self._generate_demo_protocol(description)

        system_prompt = self._get_system_prompt()
        user_prompt = self._get_user_prompt(description)

        try:
            # Get structured response from AI
            protocol_data = self.client.generate_structured_response(
                prompt=user_prompt,
                system_prompt=system_prompt
            )

            # Validate and create Protocol object
            protocol = Protocol(**protocol_data)
            return protocol

        except Exception as e:
            raise ProtocolGenerationError(f"Failed to generate protocol: {e}")

    def _generate_demo_protocol(self, description: str) -> Protocol:
        """Generate a demo protocol without requiring API access."""
        # This is a simplified demo - in real implementation we'd have more sophisticated logic
        from core.models import Protocol, Step, Equipment, Material, SafetyNote
        from core.models import SafetyLevel, EquipmentType, MaterialType, DifficultyLevel
        from datetime import datetime

        # Simple demo protocol
        steps = [
            Step(
                step_number=1,
                description=f"Perform the described procedure: {description}",
                duration_minutes=15.0,
                equipment=["Basic lab equipment"],
                materials=["Required materials"],
                notes="Follow standard laboratory safety practices"
            )
        ]

        return Protocol(
            title="Demo Protocol",
            objective=f"Demo implementation of: {description}",
            duration_minutes=15.0,
            difficulty_level=DifficultyLevel.BEGINNER,
            equipment_required=[
                Equipment(name="Basic lab equipment", type=EquipmentType.OTHER, quantity=1)
            ],
            materials_required=[
                Material(name="Required materials", type=MaterialType.OTHER, amount="as needed")
            ],
            safety_notes=[
                SafetyNote(
                    level=SafetyLevel.MEDIUM,
                    description="Follow standard laboratory safety practices",
                    ppe_required=["Lab coat", "Gloves", "Safety goggles"]
                )
            ],
            steps=steps,
            version="1.0",
            author="Lab-Rador Demo Mode"
        )

    def _get_system_prompt(self) -> str:
        """Get the system prompt for protocol generation."""
        return """You are an expert lab protocol designer and automation specialist.
Your task is to convert natural language descriptions of lab procedures into structured,
step-by-step protocols suitable for both human researchers and robotic automation systems.

You must respond with valid JSON that matches this exact schema:
{
  "title": "string",
  "objective": "string",
  "duration_minutes": number,
  "difficulty_level": "beginner|intermediate|advanced",
  "equipment_required": [{"name": "string", "type": "string", "quantity": number}],
  "materials_required": [{"name": "string", "type": "string", "amount": "string"}],
  "safety_notes": [{"level": "low|medium|high|critical", "description": "string", "ppe_required": ["string"]}],
  "steps": [{"step_number": number, "description": "string", "duration_minutes": number, "equipment": ["string"], "materials": ["string"], "notes": "string"}],
  "version": "string",
  "author": "string"
}

Be thorough, safe, and practical. Include all necessary safety precautions."""

    def _get_user_prompt(self, description: str) -> str:
        """Get the user prompt for protocol generation."""
        return f"""Convert this natural language description into a structured lab protocol:

"{description}"

Generate a complete, safe, and practical lab protocol with all required steps, equipment, materials, and safety considerations. Focus on being thorough and ensuring the protocol is executable by both humans and automation systems."""