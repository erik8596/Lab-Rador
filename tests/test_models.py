"""Tests for core models."""

import pytest

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


class TestProtocolModels:
    """Test protocol data models."""

    def test_equipment_creation(self):
        """Test equipment model creation."""
        equipment = Equipment(name="Pipette", type=EquipmentType.PIPETTE, quantity=1)
        assert equipment.name == "Pipette"
        assert equipment.type == EquipmentType.PIPETTE
        assert equipment.quantity == 1

    def test_material_creation(self):
        """Test material model creation."""
        material = Material(
            name="DNA Template", type=MaterialType.OTHER, amount="10-100 ng"
        )
        assert material.name == "DNA Template"
        assert material.type == MaterialType.OTHER
        assert material.amount == "10-100 ng"

    def test_safety_note_creation(self):
        """Test safety note model creation."""
        safety_note = SafetyNote(
            level=SafetyLevel.MEDIUM, description="Wear gloves", ppe_required=["Gloves"]
        )
        assert safety_note.level == SafetyLevel.MEDIUM
        assert safety_note.description == "Wear gloves"
        assert safety_note.ppe_required == ["Gloves"]

    def test_step_creation(self):
        """Test step model creation."""
        step = Step(
            step_number=1,
            description="Mix reagents",
            duration_minutes=5.0,
            equipment=["Pipette"],
            materials=["Buffer"],
            notes="Be careful",
        )
        assert step.step_number == 1
        assert step.description == "Mix reagents"
        assert step.duration_minutes == 5.0

    def test_protocol_creation(self):
        """Test protocol model creation."""
        protocol = Protocol(
            title="Test Protocol",
            objective="Test objective",
            duration_minutes=15.0,
            difficulty_level=DifficultyLevel.BEGINNER,
            equipment_required=[
                Equipment(name="Pipette", type=EquipmentType.PIPETTE, quantity=1)
            ],
            materials_required=[
                Material(name="Buffer", type=MaterialType.BUFFER, amount="1x")
            ],
            safety_notes=[
                SafetyNote(
                    level=SafetyLevel.LOW,
                    description="Standard precautions",
                    ppe_required=["Lab coat"],
                )
            ],
            steps=[
                Step(
                    step_number=1,
                    description="Mix reagents",
                    duration_minutes=10.0,
                    equipment=["Pipette"],
                    materials=["Buffer"],
                    notes="Standard procedure",
                )
            ],
            version="1.0",
            author="Test Author",
        )

        assert protocol.title == "Test Protocol"
        assert protocol.objective == "Test objective"
        assert protocol.duration_minutes == 15.0
        assert protocol.difficulty_level == DifficultyLevel.BEGINNER
        assert len(protocol.equipment_required) == 1
        assert len(protocol.materials_required) == 1
        assert len(protocol.safety_notes) == 1
        assert len(protocol.steps) == 1
        assert protocol.version == "1.0"
        assert protocol.author == "Test Author"


class TestEnums:
    """Test enum values."""

    def test_difficulty_levels(self):
        """Test difficulty level enum."""
        assert DifficultyLevel.BEGINNER.value == "beginner"
        assert DifficultyLevel.INTERMEDIATE.value == "intermediate"
        assert DifficultyLevel.ADVANCED.value == "advanced"

    def test_equipment_types(self):
        """Test equipment type enum."""
        assert EquipmentType.PIPETTE.value == "pipette"
        assert EquipmentType.CENTRIFUGE.value == "centrifuge"
        assert EquipmentType.THERMOCYCLER.value == "thermocycler"

    def test_material_types(self):
        """Test material type enum."""
        assert MaterialType.REAGENT.value == "reagent"
        assert MaterialType.BUFFER.value == "buffer"
        assert MaterialType.ENZYME.value == "enzyme"

    def test_safety_levels(self):
        """Test safety level enum."""
        assert SafetyLevel.LOW.value == "low"
        assert SafetyLevel.MEDIUM.value == "medium"
        assert SafetyLevel.HIGH.value == "high"
        assert SafetyLevel.CRITICAL.value == "critical"
