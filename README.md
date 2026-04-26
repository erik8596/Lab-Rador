# Lab-Rador: AI-Powered Protocol Automator

**SCSP Hackathon 2026 — Autonomous Laboratories Track**

## Status: Working with FREE AI (Quota Limited)

Lab-Rador is a complete autonomous laboratory protocol automation system that uses FREE Google Gemini AI to transform natural language descriptions into structured, executable lab protocols.

Current Status: API integration working, but free tier quota may be exceeded. Use demo mode as fallback.

## Quick Start

### 1. Get FREE Gemini API Key
1. Visit: https://makersuite.google.com/app/apikey
2. Sign in with Google account
3. Create API key and copy it

### 2. Configure Environment
```bash
# Edit .env file
GEMINI_API_KEY=your_api_key_here
LABRADOR_DEMO_MODE=false
```

### 3. Generate Your First Protocol
```bash
python main.py generate "Prepare a PCR reaction for amplifying a 500bp DNA fragment"
```

### API Quota Note
- Free Tier: 60 requests/minute, 1000/day
- If you see quota exceeded errors, use demo mode:
  ```bash
  LABRADOR_DEMO_MODE=true python main.py generate "your protocol"
  ```
- Quota resets daily

### 4. View Generated Protocols
```bash
python main.py list-protocols
```

## Features

### Implemented
- FREE AI Integration: Google Gemini API (60 requests/min, 1000/day)
- Multi-format Output: Markdown documentation + JSON data
- Rich CLI: Progress bars, tables, colored output
- Protocol Models: Pydantic-based data validation
- File Management: Automatic saving and listing
- Demo Mode: Works without API keys for testing

### Architecture
- Agent-based Design: ProtocolGenerator with AI analysis
- Modular Generators: Separate Markdown/JSON output
- Type Safety: Full Pydantic validation
- Error Handling: Comprehensive exception hierarchy
- Configuration: Environment-based settings

## Core Components

### Core Models (core/models.py)
- Protocol — Complete lab procedure with metadata
- Step — Individual protocol steps with timing
- Equipment — Lab equipment with types and quantities
- Material — Reagents with amounts and safety info
- SafetyNote — PPE requirements and warnings

### AI Agents (agents/)
- ProtocolGenerator — Converts natural language to structured protocols
- Multi-API support: Gemini (FREE) → Claude (paid) → Demo fallback

### Generators (generators/)
- MarkdownGenerator — Human-readable protocol documentation
- JSONGenerator — Structured data export/import

### CLI Interface (cli/)
- generate — Create protocols from descriptions
- list-protocols — View saved protocols
- export — Export in different formats

## Technical Stack

- Python 3.12+ with type hints
- Pydantic 2.x — Data validation and serialization
- Google Gemini API — FREE AI for protocol generation
- Typer — Modern CLI framework
- Rich — Beautiful terminal output
- Pathlib — Modern file system operations

## Project Structure

```
Lab-Rador/
├── main.py              # CLI entry point
├── cli/main_cli.py      # Command definitions
├── agents/
│   └── protocol_generator.py
├── api/
│   └── gemini_client.py # FREE Gemini API client
├── core/
│   ├── models.py        # Pydantic models
│   └── exceptions.py    # Error handling
├── generators/
│   ├── markdown_generator.py
│   └── json_generator.py
├── config/
│   └── settings.py      # Configuration
├── utils/
│   └── file_io.py       # File operations
├── data/protocols/      # Generated protocols
├── requirements.txt     # Dependencies
└── .env                 # API keys (not in git)
```

## 🎮 Usage Examples

### Generate Protocol
```bash
python main.py generate "Extract DNA from blood samples using phenol-chloroform method"
```

### List Protocols
```bash
python main.py list-protocols
```

### Export Protocol
```bash
python main.py export "protocol_name" --format markdown
```

## 🔒 Security & Safety

- **Input Validation**: All protocols validated against schemas
- **Safety Checks**: Automatic PPE and hazard identification
- **Error Handling**: Graceful failure with helpful messages
- **API Security**: Keys stored in environment variables

## 🤝 Contributing

1. Fork the repository
2. Create feature branch
3. Add tests for new functionality
4. Ensure all tests pass
5. Submit pull request

## 📄 License

MIT License - Free for academic and research use.

## Acknowledgments

- SCSP Hackathon organizers
- Google for providing FREE Gemini API
- Open source community for amazing Python libraries
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

## Next Steps

1. Implement Core Models — Define data structures
2. Build API Clients — Anthropic integration
3. Create Agents — Protocol generation logic
4. Add Generators — Output format support
5. Build CLI — User interface
6. Tests & Docs — Full coverage

## Dependencies

- anthropic — Claude AI API
- typer — CLI framework
- pydantic — Data validation
- requests — HTTP client
- rich — Beautiful terminal output
- python-dotenv — Environment variables

## Development

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
