# marclou-first-said

A Python project created with Poetry.

## Installation

This project uses Poetry for dependency management. Make sure you have Poetry installed on your system.

```bash
# Install Poetry (if you haven't already)
curl -sSL https://install.python-poetry.org | python3 -

# Install dependencies
poetry install
```

## Development

This project includes several development tools:

- `pytest` for testing
- `black` for code formatting
- `isort` for import sorting
- `flake8` for linting
- `mypy` for static type checking

### Common Commands

```bash
# Run tests
poetry run pytest

# Format code
poetry run black .
poetry run isort .

# Run linting
poetry run flake8 .

# Run type checking
poetry run mypy .
```

## Documentation

### Architecture Decision Records (ADRs)

We maintain Architecture Decision Records (ADRs) in the `docs/adr` directory to document significant architectural decisions. Current ADRs include:

1. [Transcript Storage Strategy](docs/adr/001-transcript-storage.md) - Documents our approach to storing YouTube video transcripts in MongoDB

## License

This project is licensed under the MIT License.
