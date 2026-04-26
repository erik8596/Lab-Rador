"""Tests for CLI functionality."""

import subprocess
import sys
from pathlib import Path


class TestCLI:
    """Test CLI commands via subprocess to avoid import issues."""

    def test_cli_help(self):
        """Test CLI help command."""
        result = subprocess.run(
            [sys.executable, "main.py", "--help"],
            capture_output=True,
            text=True,
            cwd=Path(__file__).parent.parent,
        )
        assert result.returncode == 0
        assert "Lab-Rador" in result.stdout
        assert "generate" in result.stdout
        assert "list-protocols" in result.stdout
        assert "export" in result.stdout

    def test_generate_help(self):
        """Test generate command help."""
        result = subprocess.run(
            [sys.executable, "main.py", "generate", "--help"],
            capture_output=True,
            text=True,
            cwd=Path(__file__).parent.parent,
        )
        assert result.returncode == 0
        assert "Generate a structured lab protocol" in result.stdout

    def test_list_protocols_help(self):
        """Test list-protocols command help."""
        result = subprocess.run(
            [sys.executable, "main.py", "list-protocols", "--help"],
            capture_output=True,
            text=True,
            cwd=Path(__file__).parent.parent,
        )
        assert result.returncode == 0
        assert "List all generated protocols" in result.stdout

    def test_export_help(self):
        """Test export command help."""
        result = subprocess.run(
            [sys.executable, "main.py", "export", "--help"],
            capture_output=True,
            text=True,
            cwd=Path(__file__).parent.parent,
        )
        assert result.returncode == 0
        assert "Export a protocol in different formats" in result.stdout
