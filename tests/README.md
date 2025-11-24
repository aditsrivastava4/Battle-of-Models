# Battle of Models Tests

This directory contains the test suite for the Battle of Models project.

## Test Structure

- `test_api.py` - End-to-end tests for the FastAPI backend
- `test_debate_module.py` - Unit tests for the debate module
- `test_integration.py` - Integration tests requiring API keys

## Running Tests

### Run all tests:
```bash
pytest
```

### Run with verbose output:
```bash
pytest -v
```

### Run specific test file:
```bash
pytest tests/test_api.py
```

### Run with coverage:
```bash
pytest --cov=. --cov-report=html
```

### Run only unit tests (skip integration):
```bash
pytest -m "not integration"
```

### Run only integration tests:
```bash
pytest -m integration
```

## Test Requirements

Install test dependencies:
```bash
pip install pytest pytest-asyncio httpx
```

## Integration Tests

Integration tests require API keys to be set in your `.env` file:
- `GROQ_API_KEY` - For Groq API access

Without these keys, integration tests will be automatically skipped.

## Continuous Integration

Tests are designed to run in CI/CD environments and will skip tests that require external API access when keys are not available.
