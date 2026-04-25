# Lab-Rador: AI-Powered Protocol Automator

**SCSP Hackathon 2026 — Autonomous Laboratories Track**

## Status: 🏗️ Foundation Template Created

This is the comprehensive project scaffold for Lab-Rador, an autonomous laboratory protocol automation system using AI to transform natural language descriptions into executable lab protocols.

## 📋 Project Structure

```
Lab-Rador/
├── agents/              # AI agents (generation, refinement, analysis)
├── api/                 # External API clients (Anthropic, protocols.io)
├── cli/                 # Command-line interface
├── config/              # Configuration and constants
├── core/                # Domain models, exceptions, enums
├── data/                # Example protocols and catalogs
├── docs/                # Documentation
├── generators/          # Output format generators (Opentrons, Markdown, JSON)
├── scripts/             # Utility scripts
├── tests/               # Test suite
├── utils/               # Logging, validation, formatting
├── main.py              # Entry point
├── requirements.txt     # Dependencies
├── pyproject.toml       # Modern Python config
├── pytest.ini           # Test configuration
├── Makefile             # Development commands
└── [docs files]         # INSTALL.md, CONTRIBUTING.md, etc.
```

## 🎯 Core Components (To Be Implemented)

### 1. **Core Module** (`core/`)
   - `models.py` — Protocol, Step, Equipment, Material, Safety models
   - `exceptions.py` — Custom error types
   - `enums.py` — Difficulty levels, equipment types, material categories

### 2. **Agents Module** (`agents/`)
   - `protocol_generator.py` — Convert natural language → structured protocols
   - `protocol_refiner.py` — Iterative refinement with feedback
   - `protocol_analyzer.py` — Safety checks and compatibility validation
   - `prompts/` — Claude prompt templates

### 3. **Generators Module** (`generators/`)
   - `opentrons_generator.py` — Generate Opentrons robot scripts
   - `markdown_generator.py` — Human-readable documentation
   - `json_generator.py` — Structured data export

### 4. **API Module** (`api/`)
   - `anthropic_client.py` — Wrapper for Claude API
   - `protocols_io_client.py` — Integration with protocols.io
   - `base_client.py` — Common HTTP utilities

### 5. **CLI Module** (`cli/`)
   - `main_cli.py` — CLI entry point
   - `commands/` — Individual commands (generate, refine, analyze, export, list)

### 6. **Utils Module** (`utils/`)
   - `logger.py` — Structured logging
   - `validators.py` — Data validation
   - `formatters.py` — Output formatting
   - `file_io.py` — File operations

## 🚀 Next Steps

1. **Implement Core Models** — Define data structures
2. **Build API Clients** — Anthropic integration
3. **Create Agents** — Protocol generation logic
4. **Add Generators** — Output format support
5. **Build CLI** — User interface
6. **Tests & Docs** — Full coverage

## 📦 Dependencies

- **anthropic** — Claude AI API
- **typer** — CLI framework
- **pydantic** — Data validation
- **requests** — HTTP client
- **rich** — Beautiful terminal output
- **python-dotenv** — Environment variables

## 🔧 Development

```bash
# Install dependencies
pip install -r requirements.txt

# Set up environment
cp .env.example .env
# Add ANTHROPIC_API_KEY

# Run tests
make test

# Format code
make format

# Run dev server
make dev
```

## 📝 Documentation

- [ARCHITECTURE.md](docs/ARCHITECTURE.md) — System design
- [API_REFERENCE.md](docs/API_REFERENCE.md) — API documentation
- [PROTOCOL_SCHEMA.md](docs/PROTOCOL_SCHEMA.md) — Protocol format
- [DEVELOPMENT.md](docs/DEVELOPMENT.md) — Developer guide
- [INSTALL.md](INSTALL.md) — Installation instructions

## 🏆 Hackathon Goal

Build a complete autonomous agent system that:
- Takes natural language lab procedure descriptions
- Generates structured, validated protocols
- Outputs executable automation scripts (Opentrons)
- Supports iterative refinement with AI feedback
- Validates safety and equipment compatibility

---

**Project Template Created:** April 2026  
**Status:** Ready for implementation
