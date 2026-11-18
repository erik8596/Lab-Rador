# Lab-Rador

**AI-assisted laboratory protocol generation | SCSP Hackathon 2026 — Autonomous Laboratories Track**

Lab-Rador is a Python command-line prototype that converts a natural-language description of a laboratory procedure into a structured protocol. It uses an AI provider to draft protocol data, validates the resulting structure with Pydantic, and saves readable Markdown and machine-readable JSON files.

The project explores how language models, typed data models, and modular software components can work together in a scientific workflow. **It is a hackathon prototype, not a validated laboratory automation or safety system.**

## Features

- **Natural-language input:** Describe a procedure through a command-line interface built with Typer and Rich.
- **AI integration:** Generate structured responses using Google Gemini or Anthropic Claude, depending on the configured API key.
- **Typed protocol models:** Represent steps, materials, equipment, estimated duration, and safety notes with Pydantic models.
- **Two output formats:** Save generated protocols as Markdown and JSON files.
- **Saved protocol listing:** Display previously generated protocols from a local directory.
- **Demo fallback:** Generate a simplified example protocol when the selected AI provider returns an error. Demo output is illustrative, not scientifically verified.
- **Automated tests:** Includes tests for protocol models and CLI help commands.

## Tech Stack

Python 3.12+ · Pydantic · Typer · Rich · Google Gemini API · Anthropic API · python-dotenv · pytest

## Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/erik8596/Lab-Rador.git
cd Lab-Rador
```

### 2. Create a virtual environment

```bash
python3.12 -m venv .venv
source .venv/bin/activate
```

On Windows, activate it with `.venv\Scripts\activate` instead.

### 3. Install dependencies

```bash
python -m pip install -r requirements.txt
```

**Dependency note:** This project pins `google-genai==0.8.0` to remain compatible with its existing `pydantic==2.6.4` requirement. Upgrading the Google SDK may require updating Pydantic and checking for API changes.

### 4. Configure an API key

```bash
cp .env.example .env
```

Open `.env` and add **at least one** of the following settings:

```dotenv
GEMINI_API_KEY=your_gemini_api_key_here
# Or:
# ANTHROPIC_API_KEY=your_anthropic_api_key_here
```

The current configuration requires an API key to start, even though protocol generation can fall back to demo output after an API error. When both keys are configured, the generator selects Gemini. Never commit your `.env` file or real API keys.

### 5. Generate a sample protocol

```bash
python main.py generate "Mix 10 mL of water with 5 mL of blue dye."
```

Generated `.md` and `.json` files are saved in `data/protocols/` by default.

### 6. List generated protocols

```bash
python main.py list-protocols
```

To view all CLI commands and options:

```bash
python main.py --help
```

## How It Works

1. The **CLI** accepts a plain-language description.
2. `ProtocolGenerator` selects a configured AI client and requests structured JSON.
3. The returned data is parsed into a **Pydantic `Protocol` model**, which checks the data's structure and types.
4. The **Markdown and JSON generators** format the protocol.
5. File utilities save the outputs locally for inspection.

Pydantic validation checks schema conformity; it does **not** establish that scientific instructions are accurate, safe, or complete.

## Project Structure

```text
Lab-Rador/
├── agents/                # Protocol-generation orchestration and demo fallback
├── api/                   # Gemini and Anthropic clients
├── cli/                   # Typer command-line interface
├── config/                # Environment settings
├── core/                  # Pydantic models and exceptions
├── generators/            # Markdown and JSON output
├── utils/                 # Protocol file handling
├── data/protocols/        # Sample and generated protocol files
├── tests/                 # Model and CLI tests
├── main.py                # Application entry point
├── requirements.txt       # Dependency list
└── .env.example           # Environment configuration template
```

## Example Outputs

The repository includes sample generated files you can inspect without running an API request:

- [Example Markdown protocol](data/protocols/demo_protocol___test_protocol_generation_20260426_003523.md)
- [Example JSON protocol](data/protocols/demo_protocol___test_protocol_generation_20260426_003523.json)

## Testing

The repository contains `pytest` tests for the data models and CLI commands. After installing dependencies and configuring an API key, run:

```bash
python -m pytest
```

The project configuration currently specifies an 80% coverage threshold. Test passing status and coverage have **not been independently verified** for this README update.

## Current Limitations and Planned Work

- **Not implemented:** Opentrons script generation and protocols.io integration are placeholders in the current source tree.
- **Not implemented:** Physical laboratory equipment control and end-to-end scientific validation.
- **API fallback behavior:** The app selects one provider at startup; it does not automatically switch from Gemini to Claude after a request fails. The implemented error fallback generates a simplified demo protocol.
- **Dependency upgrades:** The Google Gen AI SDK is pinned to an older compatible version. Updating it and the Pydantic dependency together may require code or model-configuration changes.
- **Export command:** An `export` CLI command exists, but the file-loading utility contains duplicate function definitions. Verify and fix exporting before relying on it.
- **Model and quota settings:** Available provider models, prices, and rate limits may change. Confirm current settings with the provider before use.

## Safety and Intended Use

Lab-Rador is an experimental software project. AI-generated and demo protocols may be incomplete, incorrect, or unsafe. Do not use generated instructions to conduct laboratory procedures, operate equipment, or make safety decisions without review and approval by qualified laboratory personnel. Included safety-note fields are not a substitute for formal risk assessment.

## Project Context

Developed for the **SCSP Hackathon 2026, Autonomous Laboratories Track**. The project demonstrates modular Python architecture, API integration, structured data validation, automated tests, and command-line development.

## License

The repository's `LICENSE` file is currently a placeholder. A license has not yet been specified in the uploaded version.
