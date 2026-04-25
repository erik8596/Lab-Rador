"""JSON export generator."""

import json
from typing import Dict, Any
from pathlib import Path
from core.models import Protocol


class JSONGenerator:
    """Generates JSON exports from protocols."""

    @staticmethod
    def generate_protocol_json(protocol: Protocol, pretty: bool = True) -> str:
        """
        Generate JSON representation of a protocol.

        Args:
            protocol: Protocol object
            pretty: Whether to pretty-print the JSON

        Returns:
            JSON string representation
        """
        protocol_dict = protocol.model_dump()

        # Convert datetime to ISO format string
        if 'created_at' in protocol_dict and protocol_dict['created_at']:
            protocol_dict['created_at'] = protocol_dict['created_at'].isoformat()

        if pretty:
            return json.dumps(protocol_dict, indent=2, ensure_ascii=False)
        else:
            return json.dumps(protocol_dict, ensure_ascii=False)

    @staticmethod
    def save_protocol_json(protocol: Protocol, file_path: Path, pretty: bool = True) -> None:
        """
        Save protocol as JSON file.

        Args:
            protocol: Protocol object
            file_path: Path to save the file
            pretty: Whether to pretty-print the JSON
        """
        json_content = JSONGenerator.generate_protocol_json(protocol, pretty)

        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(json_content)

    @staticmethod
    def load_protocol_json(file_path: Path) -> Protocol:
        """
        Load protocol from JSON file.

        Args:
            file_path: Path to the JSON file

        Returns:
            Protocol object

        Raises:
            FileNotFoundError: If file doesn't exist
            ValueError: If JSON is invalid or doesn't match schema
        """
        if not file_path.exists():
            raise FileNotFoundError(f"Protocol file not found: {file_path}")

        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        # Convert ISO datetime string back to datetime if present
        if 'created_at' in data and isinstance(data['created_at'], str):
            from datetime import datetime
            try:
                data['created_at'] = datetime.fromisoformat(data['created_at'])
            except ValueError:
                # If parsing fails, keep as string or set to None
                data['created_at'] = None

        return Protocol(**data)

    @staticmethod
    def generate_protocol_metadata(protocol: Protocol) -> Dict[str, Any]:
        """
        Generate metadata dictionary for a protocol.

        Args:
            protocol: Protocol object

        Returns:
            Metadata dictionary
        """
        return {
            "id": f"{protocol.title.lower().replace(' ', '_')}_{protocol.version}",
            "title": protocol.title,
            "created_at": protocol.created_at.isoformat() if protocol.created_at else None,
            "modified_at": protocol.created_at.isoformat() if protocol.created_at else None,
            "version": protocol.version,
            "author": protocol.author,
            "tags": [],  # Could be extended to extract from content
            "source": "generated",
            "stats": {
                "total_steps": len(protocol.steps),
                "total_duration_minutes": protocol.get_total_duration(),
                "equipment_count": len(protocol.equipment_required),
                "materials_count": len(protocol.materials_required),
                "safety_notes_count": len(protocol.safety_notes),
                "difficulty_level": protocol.difficulty_level.value
            }
        }
