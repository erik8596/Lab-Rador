"""Domain models for protocols, steps, and lab entities."""

from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field, field_validator


class DifficultyLevel(str, Enum):
    """Protocol difficulty levels."""

    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"


class EquipmentType(str, Enum):
    """Types of lab equipment."""

    PIPETTE = "pipette"
    CENTRIFUGE = "centrifuge"
    INCUBATOR = "incubator"
    MICROPIPETTE = "micropipette"
    TUBE_RACK = "tube_rack"
    PLATE_READER = "plate_reader"
    THERMOCYCLER = "thermocycler"
    OTHER = "other"


class MaterialType(str, Enum):
    """Types of lab materials."""

    REAGENT = "reagent"
    BUFFER = "buffer"
    ENZYME = "enzyme"
    ANTIBODY = "antibody"
    CELL_LINE = "cell_line"
    PLASMID = "plasmid"
    OTHER = "other"


class SafetyLevel(str, Enum):
    """Safety concern levels."""

    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class Equipment(BaseModel):
    """Lab equipment item."""

    name: str = Field(..., description="Equipment name")
    type: EquipmentType = Field(..., description="Equipment category")
    quantity: int = Field(default=1, description="Number of units needed")
    notes: Optional[str] = Field(
        default=None, description="Special notes or requirements"
    )


class Material(BaseModel):
    """Lab material or reagent."""

    name: str = Field(..., description="Material name")
    type: MaterialType = Field(..., description="Material category")
    amount: str = Field(..., description="Amount/quantity needed")
    concentration: Optional[str] = Field(
        default=None, description="Concentration if applicable"
    )
    storage_conditions: Optional[str] = Field(
        default=None, description="Storage requirements"
    )
    notes: Optional[str] = Field(default=None, description="Special handling notes")


class SafetyNote(BaseModel):
    """Safety consideration or warning."""

    level: SafetyLevel = Field(..., description="Safety concern level")
    description: str = Field(..., description="Safety note text")
    ppe_required: Optional[List[str]] = Field(default=None, description="Required PPE")
    hazards: Optional[List[str]] = Field(default=None, description="Associated hazards")


class Step(BaseModel):
    """Individual step in a lab protocol."""

    step_number: int = Field(..., description="Sequential step number")
    description: str = Field(..., description="Detailed step instructions")
    duration_minutes: float = Field(
        default=0.0, description="Estimated duration in minutes"
    )
    notes: Optional[str] = Field(default=None, description="Additional notes or tips")
    equipment: Optional[List[str]] = Field(
        default_factory=list, description="Equipment used in this step"
    )
    materials: Optional[List[str]] = Field(
        default_factory=list, description="Materials used in this step"
    )
    critical_parameters: Optional[Dict[str, Any]] = Field(
        default=None, description="Critical parameters to monitor"
    )

    @field_validator("step_number")
    @classmethod
    def step_number_must_be_positive(cls, v):
        if v < 1:
            raise ValueError("Step number must be positive")
        return v


class Protocol(BaseModel):
    """Complete lab protocol."""

    title: str = Field(..., description="Protocol title")
    objective: str = Field(..., description="What the protocol achieves")
    duration_minutes: float = Field(..., description="Total estimated duration")
    difficulty_level: DifficultyLevel = Field(
        default=DifficultyLevel.INTERMEDIATE, description="Difficulty level"
    )
    equipment_required: List[Equipment] = Field(
        default_factory=list, description="Required equipment"
    )
    materials_required: List[Material] = Field(
        default_factory=list, description="Required materials"
    )
    safety_notes: List[SafetyNote] = Field(
        default_factory=list, description="Safety considerations"
    )
    steps: List[Step] = Field(default_factory=list, description="Protocol steps")
    created_at: datetime = Field(
        default_factory=datetime.now, description="Creation timestamp"
    )
    version: str = Field(default="1.0", description="Protocol version")
    author: Optional[str] = Field(default=None, description="Protocol author")
    references: Optional[List[str]] = Field(
        default=None, description="Literature references"
    )

    @field_validator("duration_minutes")
    @classmethod
    def duration_must_be_positive(cls, v):
        if v < 0:
            raise ValueError("Duration must be non-negative")
        return v

    @field_validator("steps")
    @classmethod
    def steps_must_be_ordered(cls, v):
        if not v:
            return v
        step_numbers = [step.step_number for step in v]
        if step_numbers != list(range(1, len(step_numbers) + 1)):
            raise ValueError("Steps must be numbered sequentially starting from 1")
        return v

    def get_total_duration(self) -> float:
        """Calculate total duration from steps if not explicitly set."""
        if self.duration_minutes > 0:
            return self.duration_minutes
        return sum(step.duration_minutes for step in self.steps)

    def get_equipment_names(self) -> List[str]:
        """Get list of equipment names."""
        return [eq.name for eq in self.equipment_required]

    def get_material_names(self) -> List[str]:
        """Get list of material names."""
        return [mat.name for mat in self.materials_required]


class ProtocolMetadata(BaseModel):
    """Metadata for protocol storage and retrieval."""

    id: str = Field(..., description="Unique protocol identifier")
    title: str = Field(..., description="Protocol title")
    created_at: datetime = Field(..., description="Creation timestamp")
    modified_at: datetime = Field(..., description="Last modification timestamp")
    version: str = Field(..., description="Protocol version")
    author: Optional[str] = Field(default=None, description="Protocol author")
    tags: List[str] = Field(default_factory=list, description="Protocol tags")
    source: str = Field(
        default="generated", description="Protocol source (generated, imported, etc.)"
    )


class ValidationResult(BaseModel):
    """Result of protocol validation."""

    is_valid: bool = Field(..., description="Whether validation passed")
    errors: List[str] = Field(
        default_factory=list, description="Validation error messages"
    )
    warnings: List[str] = Field(default_factory=list, description="Validation warnings")
    suggestions: List[str] = Field(
        default_factory=list, description="Improvement suggestions"
    )
