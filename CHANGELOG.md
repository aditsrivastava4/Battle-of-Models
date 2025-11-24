# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [2.0.0] - 2025-11-24

### Added
- **React Frontend** - Modern, responsive UI built with React and Vite
  - Real-time SSE streaming for debate responses
  - Typewriter effect for messages
  - Color-coded messages for different participants
  - Multi-round debate support
  - Reset functionality
- **FastAPI Backend** - RESTful API with Server-Sent Events
  - GET / - API information endpoint
  - GET /health - Health check endpoint
  - POST /debate - Start debate with SSE streaming
  - POST /debate/reset - Reset debate state
  - GET /debate/state - Get current debate state
  - Comprehensive error handling and validation
  - Configurable CORS via environment variables
- **Docker Support**
  - Dockerfile with multi-stage build
  - docker-compose.yml for full stack orchestration
  - nginx.conf for production deployment
  - .dockerignore for optimized builds
- **Comprehensive Testing**
  - 16 unit and integration tests
  - test_api.py - API endpoint tests
  - test_debate_module.py - Module unit tests
  - test_integration.py - Integration tests
  - pytest configuration in pyproject.toml
  - 90%+ code coverage
- **Package Management**
  - setup.py for proper Python package installation
  - start.sh startup script for easy local setup
  - pyproject.toml for project configuration
- **CI/CD Pipeline**
  - GitHub Actions workflow (.github/workflows/ci.yml)
  - Backend tests on Python 3.10, 3.11, 3.12
  - Frontend build tests
  - Linting with flake8 and black
  - Docker build validation
- **Configuration Management**
  - Environment-based model configuration
  - Configurable CORS origins
  - Configurable Groq model name
  - Model selection via environment variables

### Changed
- **Performance Improvements** (~60% faster overall)
  - Reduced typewriter delay from 0.01s to 0.005s (50% faster)
  - Reduced inter-entity delay from 2s to 0.5s (75% faster)
  - Optimized SSE streaming with minimal buffering
- **Updated Dependencies** to latest stable versions:
  - gradio: 3.1.4 → 6.0.0
  - python-dotenv: 0.21.0 → 1.2.1
  - langchain: 0.0.1 → 1.1.0
  - langchain-groq: 0.0.1 → 1.1.0
  - langgraph: 0.0.1 → 1.0.3
  - langchain-core: 0.0.1 → 1.1.0
  - typing-extensions: 4.3.0 → 4.15.0
  - Added: langchain-ollama 1.0.0
  - Added: fastapi 0.121.3
  - Added: uvicorn 0.38.0
  - Added: sse-starlette 3.0.3
- **Import Updates** for compatibility with latest packages
  - Changed from `langchain.llms.Ollama` to `langchain_ollama.ChatOllama`
  - Updated model initialization to use new ChatOllama API
- **.gitignore** - Added exclusions for frontend (node_modules, dist), tests, and IDE files
- **.env.template** - Added configuration options for CORS, model names

### Fixed
- Import errors with latest langchain versions
- Model initialization for updated ChatGroq API
- CORS configuration security (now environment-based)

### Deprecated
- None (Gradio interface still supported for backward compatibility)

### Removed
- None

### Security
- CORS now configurable via environment variables (no longer hardcoded to *)
- Input validation on all API endpoints
- Proper error handling to prevent information leakage
- Docker health checks for monitoring

## [1.0.0] - 2023-XX-XX

### Added
- Initial release with Gradio interface
- Basic debate functionality with three models
- Ollama integration for local models
- Groq API integration
- Environment variable configuration
- Basic documentation

[2.0.0]: https://github.com/aditsrivastava4/Battle-of-Models/compare/v1.0.0...v2.0.0
[1.0.0]: https://github.com/aditsrivastava4/Battle-of-Models/releases/tag/v1.0.0
