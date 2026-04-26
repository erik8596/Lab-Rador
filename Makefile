# Lab-Rador Development Makefile

.PHONY: help install test lint format clean run dev setup

# Default target
help:
	@echo "Lab-Rador Development Commands:"
	@echo "  install    Install dependencies"
	@echo "  test       Run tests"
	@echo "  lint       Run linting"
	@echo "  format     Format code"
	@echo "  clean      Clean build artifacts"
	@echo "  run        Run the application"
	@echo "  dev        Run in development mode"
	@echo "  setup      Initial project setup"

# Install dependencies
install:
	@echo "Installing dependencies..."
	python -m pip install --upgrade pip
	pip install -r requirements.txt

# Run tests
test:
	@echo "Running tests..."
	pytest

# Run linting
lint:
	@echo "Running linting..."
	python -m py_compile core/models.py core/exceptions.py
	python -m py_compile agents/*.py api/*.py cli/*.py generators/*.py utils/*.py
	@echo "Syntax check passed!"

# Format code
format:
	@echo "Formatting code..."
	black .
	isort .

# Clean build artifacts
clean:
	@echo "Cleaning build artifacts..."
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	rm -rf .pytest_cache/
	rm -rf build/
	rm -rf dist/

# Run the application
run:
	@echo "Running Lab-Rador..."
	./venv/bin/python main.py --help

# Development mode
dev:
	@echo "Starting development environment..."
	@echo "Available commands:"
	@echo "  make run          - Run the application"
	@echo "  make test         - Run tests"
	@echo "  make lint         - Run linting"
	@echo "  make format       - Format code"
	@echo "  make clean        - Clean artifacts"

# Initial project setup
setup: install
	@echo "Setting up development environment..."
	@echo "1. Copy .env.example to .env and configure your API keys"
	@echo "2. Run 'make dev' to see available commands"
	@echo "3. Run 'make test' to run tests"
	@echo "4. Run 'make run' to start the application"
