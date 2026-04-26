"""Protocol generation agent."""

import json
from typing import Any, Dict, Optional

from api.anthropic_client import AnthropicClient
from api.gemini_client import GeminiClient
from config.settings import ANTHROPIC_API_KEY, GEMINI_API_KEY
from core.exceptions import ProtocolGenerationError
from core.models import Protocol


class ProtocolGenerator:
    """Agent that converts natural language descriptions into structured lab protocols."""

    def __init__(self):
        # Always try Gemini (free) first, then Claude (paid), otherwise demo mode
        if GEMINI_API_KEY:
            self.client = GeminiClient()
            self.client_type = "gemini"
        elif ANTHROPIC_API_KEY:
            self.client = AnthropicClient()
            self.client_type = "anthropic"
        else:
            self.client = None  # Demo mode fallback

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
        system_prompt = self._get_system_prompt()
        user_prompt = self._get_user_prompt(description)

        # Always try AI first, fallback to demo mode on any error
        if self.client:
            try:
                # Get structured response from AI
                protocol_data = self.client.generate_structured_response(
                    prompt=user_prompt, system_prompt=system_prompt
                )

                # Validate and create Protocol object
                protocol = Protocol(**protocol_data)
                return protocol

            except Exception as e:
                # Check if it's a quota exceeded error and fall back to demo mode
                error_str = str(e).lower()
                if (
                    "quota" in error_str
                    or "resource_exhausted" in error_str
                    or "429" in error_str
                ):
                    print("API quota exceeded, falling back to demo mode...")
                else:
                    print(f"API error ({e}), falling back to demo mode...")
                return self._generate_demo_protocol(description)
        else:
            # No API client available, use demo mode
            return self._generate_demo_protocol(description)

    def _generate_demo_protocol(self, description: str) -> Protocol:
        """Generate a demo protocol without requiring API access."""
        import re
        from datetime import datetime

        from core.models import (
            DifficultyLevel,
            Equipment,
            EquipmentType,
            Material,
            MaterialType,
            Protocol,
            SafetyLevel,
            SafetyNote,
            Step,
        )

        # Try to intelligently parse the description for better demo protocols
        description_lower = description.lower()

        # Extract potential equipment and materials from description
        equipment_list = []
        materials_list = []
        safety_notes = []

        # Common lab equipment patterns
        if any(word in description_lower for word in ["pipette", "pipet", "transfer"]):
            equipment_list.append(
                Equipment(
                    name="Pipette", type=EquipmentType.LIQUID_HANDLING, quantity=1
                )
            )
        if any(word in description_lower for word in ["centrifuge", "spin"]):
            equipment_list.append(
                Equipment(name="Centrifuge", type=EquipmentType.CENTRIFUGE, quantity=1)
            )
        if any(
            word in description_lower for word in ["incubator", "heat", "temperature"]
        ):
            equipment_list.append(
                Equipment(name="Incubator", type=EquipmentType.INCUBATOR, quantity=1)
            )
        if any(word in description_lower for word in ["pcr", "thermal cycler"]):
            equipment_list.append(
                Equipment(
                    name="Thermal Cycler", type=EquipmentType.THERMOCYCLER, quantity=1
                )
            )
        if any(word in description_lower for word in ["microscope", "view", "observe"]):
            equipment_list.append(
                Equipment(name="Microscope", type=EquipmentType.MICROSCOPE, quantity=1)
            )

        # Common materials patterns
        if any(word in description_lower for word in ["dna", "rna", "template"]):
            materials_list.append(
                Material(
                    name="DNA Template", type=MaterialType.OTHER, amount="10-100 ng"
                )
            )
        if any(word in description_lower for word in ["primer", "forward", "reverse"]):
            materials_list.append(
                Material(
                    name="PCR Primers", type=MaterialType.OTHER, amount="0.5 μM each"
                )
            )
        if any(word in description_lower for word in ["buffer", "solution"]):
            materials_list.append(
                Material(name="Reaction Buffer", type=MaterialType.BUFFER, amount="1x")
            )
        if any(word in description_lower for word in ["enzyme", "polymerase", "taq"]):
            materials_list.append(
                Material(
                    name="DNA Polymerase", type=MaterialType.ENZYME, amount="1 unit"
                )
            )

        # Default equipment if none detected
        if not equipment_list:
            equipment_list.append(
                Equipment(
                    name="Basic lab equipment", type=EquipmentType.OTHER, quantity=1
                )
            )

        # Default materials if none detected
        if not materials_list:
            materials_list.append(
                Material(
                    name="Required reagents",
                    type=MaterialType.OTHER,
                    amount="as needed",
                )
            )

        # Basic safety note
        safety_notes.append(
            SafetyNote(
                level=SafetyLevel.MEDIUM,
                description="Follow standard laboratory safety practices",
                ppe_required=["Lab coat", "Gloves", "Safety goggles"],
            )
        )

        # Estimate duration based on complexity
        duration = 15.0  # base duration
        if "pcr" in description_lower:
            duration = 120.0  # PCR typically takes longer
        elif any(word in description_lower for word in ["culture", "incubate"]):
            duration = 60.0

        # Determine difficulty
        difficulty = DifficultyLevel.BEGINNER
        if len(description.split()) > 20 or any(
            word in description_lower for word in ["pcr", "sequencing", "culture"]
        ):
            difficulty = DifficultyLevel.INTERMEDIATE

        # Create steps - break down the description into logical steps
        steps = []
        sentences = [s.strip() for s in description.split(".") if s.strip()]

        for i, sentence in enumerate(sentences, 1):
            step_duration = duration / len(sentences) if sentences else duration

            steps.append(
                Step(
                    step_number=i,
                    description=sentence,
                    duration_minutes=round(step_duration, 1),
                    equipment=[eq.name for eq in equipment_list],
                    materials=[mat.name for mat in materials_list],
                    notes="Follow standard laboratory safety practices",
                )
            )

        # If no sentences found, create a single step
        if not steps:
            steps = [
                Step(
                    step_number=1,
                    description=f"Perform the described procedure: {description}",
                    duration_minutes=duration,
                    equipment=[eq.name for eq in equipment_list],
                    materials=[mat.name for mat in materials_list],
                    notes="Follow standard laboratory safety practices",
                )
            ]

        return Protocol(
            title=f"Demo Protocol - {description[:50]}{'...' if len(description) > 50 else ''}",
            objective=f"Demo implementation of: {description}",
            duration_minutes=duration,
            difficulty_level=difficulty,
            equipment_required=equipment_list,
            materials_required=materials_list,
            safety_notes=safety_notes,
            steps=steps,
            version="1.0",
            author="Lab-Rador Demo Mode",
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
