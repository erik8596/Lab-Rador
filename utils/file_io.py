"""File I/O operations."""

import json
from pathlib import Path
from typing import List, Dict, Any
from datetime import datetime
from core.models import Protocol
from generators.markdown_generator import MarkdownGenerator
from generators.json_generator import JSONGenerator


def save_protocol_files(
    protocol: Protocol,
    output_dir: str,
    custom_name: str = None
) -> List[str]:
    """
    Save protocol in multiple formats.

    Args:
        protocol: Protocol to save
        output_dir: Directory to save files
        custom_name: Custom base filename (auto-generated if None)

    Returns:
        List of saved file paths
    """
    output_path = Path(output_dir)
    output_path.mkdir(exist_ok=True, parents=True)

    # Generate base name
    if custom_name:
        base_name = custom_name
    else:
        # Create a safe filename from protocol title
        base_name = protocol.title.lower().replace(' ', '_').replace('-', '_')
        base_name = ''.join(c for c in base_name if c.isalnum() or c == '_')
        # Add timestamp to avoid conflicts
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        base_name = f"{base_name}_{timestamp}"

    saved_files = []

    # Generate and save Markdown
    markdown_gen = MarkdownGenerator()
    markdown_content = markdown_gen.generate_protocol_markdown(protocol)
    markdown_path = output_path / f"{base_name}.md"
    with open(markdown_path, 'w', encoding='utf-8') as f:
        f.write(markdown_content)
    saved_files.append(str(markdown_path))

    # Generate and save JSON
    json_gen = JSONGenerator()
    json_content = json_gen.generate_protocol_json(protocol)
    json_path = output_path / f"{base_name}.json"
    with open(json_path, 'w', encoding='utf-8') as f:
        f.write(json_content)
    saved_files.append(str(json_path))

    return saved_files


def load_protocol_from_file(file_path: str) -> Protocol:
    """
    Load a protocol from a JSON file.

    Args:
        file_path: Path to the JSON file

    Returns:
        Protocol object

    Raises:
        FileNotFoundError: If file doesn't exist
        ValueError: If JSON is invalid or doesn't contain a valid protocol
    """
    path = Path(file_path)

    # If just a name is provided, look in the protocols directory
    if not path.exists():
        from config.settings import PROTOCOLS_DIR
        protocols_dir = Path(PROTOCOLS_DIR)
        # Try different extensions
        for ext in ['.json', '.md']:
            candidate = protocols_dir / f"{file_path}{ext}"
            if candidate.exists():
                path = candidate
                break

    if not path.exists():
        raise FileNotFoundError(f"Protocol file not found: {file_path}")

    # Load JSON file
    with open(path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # Convert back to Protocol object
    return Protocol(**data)


def list_protocol_files(directory: str) -> List[Dict[str, Any]]:
    """
    List all protocol files in a directory.

    Args:
        directory: Directory to scan

    Returns:
        List of protocol information dictionaries
    """
    protocols_dir = Path(directory)
    if not protocols_dir.exists():
        return []

    protocols = []

    # Find all JSON files (assuming they contain protocol data)
    for json_file in protocols_dir.glob("*.json"):
        try:
            with open(json_file, 'r', encoding='utf-8') as f:
                data = json.load(f)

            # Extract basic info
            protocol_info = {
                'filename': json_file.name,
                'title': data.get('title', 'Unknown'),
                'created_at': datetime.fromisoformat(data.get('created_at', datetime.now().isoformat())),
                'version': data.get('version', '1.0'),
                'steps_count': len(data.get('steps', [])),
                'file_path': str(json_file)
            }
            protocols.append(protocol_info)

        except (json.JSONDecodeError, KeyError, ValueError):
            # Skip invalid files
            continue

    # Sort by creation date (newest first)
    protocols.sort(key=lambda x: x['created_at'], reverse=True)

    return protocols

    # Save JSON
    json_path = output_dir / f"{base_name}_protocol.json"
    json_gen.save_protocol_json(protocol, json_path)
    saved_files["JSON"] = json_path

    # Save Markdown
    markdown_content = markdown_gen.generate_protocol_markdown(protocol)
    markdown_path = output_dir / f"{base_name}_protocol.md"
    with open(markdown_path, "w", encoding="utf-8") as f:
        f.write(markdown_content)
    saved_files["Markdown"] = markdown_path

    return saved_files


def load_protocol_from_file(file_path: Path) -> Protocol:
    """
    Load protocol from JSON file.

    Args:
        file_path: Path to JSON file

    Returns:
        Protocol object

    Raises:
        FileNotFoundError: If file doesn't exist
        ValueError: If file is not valid JSON or doesn't match schema
    """
    return JSONGenerator.load_protocol_json(file_path)


def create_output_directory(base_dir: Path, protocol_name: str) -> Path:
    """
    Create and return output directory for a protocol.

    Args:
        base_dir: Base output directory
        protocol_name: Protocol name for subdirectory

    Returns:
        Path to output directory
    """
    output_dir = base_dir / protocol_name.lower().replace(" ", "_")
    output_dir.mkdir(parents=True, exist_ok=True)
    return output_dir
