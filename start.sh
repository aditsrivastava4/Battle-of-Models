#!/bin/bash
# Startup script for Battle of Models

set -e

echo "🚀 Battle of Models - Startup Script"
echo "===================================="

# Check if .env exists
if [ ! -f .env ]; then
    echo "⚠️  .env file not found. Copying from template..."
    cp .env.template .env
    echo "✅ Please edit .env and add your GROQ_API_KEY"
    exit 1
fi

# Check for required tools
command -v python3 >/dev/null 2>&1 || { echo "❌ Python 3 is required but not installed."; exit 1; }
command -v node >/dev/null 2>&1 || { echo "❌ Node.js is required but not installed."; exit 1; }

echo "📦 Installing Python dependencies..."
pip install -q -r requirements.txt

echo "📦 Installing frontend dependencies..."
cd frontend && npm install && cd ..

echo ""
echo "✅ Setup complete!"
echo ""
echo "To start the application:"
echo "  Backend:  python api.py (or uvicorn api:app --reload)"
echo "  Frontend: cd frontend && npm run dev"
echo ""
echo "Or use Docker:"
echo "  docker-compose up"
echo ""
