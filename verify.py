#!/usr/bin/env python3
"""
Verification script to test Battle of Models v2.0 setup
"""

import sys
import os

def test_imports():
    """Test that all required imports work."""
    print("🔍 Testing imports...")
    try:
        from api import app, debate_state, ENTITIES
        from debate_module import __get_config, start_debate
        from debate_module.main import call_model, init_workflow
        from debate_module.resource import __get_config as get_config
        from debate_module.state import State
        print("  ✅ All imports successful")
        return True
    except Exception as e:
        print(f"  ❌ Import error: {e}")
        return False


def test_configuration():
    """Test configuration loading."""
    print("\n🔍 Testing configuration...")
    try:
        from debate_module import __get_config
        config = __get_config()
        
        # Check all entities are configured
        required_entities = ['c1', 'c2', 'moderator']
        for entity in required_entities:
            if entity not in config:
                print(f"  ❌ Missing entity: {entity}")
                return False
            if 'model_name' not in config[entity]:
                print(f"  ❌ Missing model_name for {entity}")
                return False
        
        print("  ✅ Configuration valid")
        return True
    except Exception as e:
        print(f"  ❌ Configuration error: {e}")
        return False


def test_api_structure():
    """Test FastAPI app structure."""
    print("\n🔍 Testing API structure...")
    try:
        from api import app
        
        # Check routes exist
        routes = [route.path for route in app.routes]
        required_routes = ['/', '/health', '/debate', '/debate/reset', '/debate/state']
        
        for route in required_routes:
            if route not in routes:
                print(f"  ❌ Missing route: {route}")
                return False
        
        print("  ✅ All API routes present")
        return True
    except Exception as e:
        print(f"  ❌ API structure error: {e}")
        return False


def test_environment():
    """Test environment setup."""
    print("\n🔍 Testing environment...")
    
    # Check for .env or environment variables
    has_groq_key = os.getenv('GROQ_API_KEY') is not None
    has_env_file = os.path.exists('.env')
    
    if not has_groq_key and not has_env_file:
        print("  ⚠️  No .env file found and GROQ_API_KEY not set")
        print("     Run: cp .env.template .env and add your API key")
    else:
        print("  ✅ Environment configured")
    
    return True


def test_tests():
    """Check if tests can be imported."""
    print("\n🔍 Testing test suite...")
    try:
        import pytest
        
        # Check test files exist
        test_files = [
            'tests/test_api.py',
            'tests/test_debate_module.py',
            'tests/test_integration.py'
        ]
        
        for test_file in test_files:
            if not os.path.exists(test_file):
                print(f"  ❌ Missing test file: {test_file}")
                return False
        
        print("  ✅ Test suite available")
        return True
    except ImportError:
        print("  ⚠️  pytest not installed - run: pip install pytest pytest-asyncio httpx")
        return True  # Not critical


def test_frontend():
    """Check if frontend exists."""
    print("\n🔍 Testing frontend...")
    
    if not os.path.exists('frontend'):
        print("  ❌ Frontend directory not found")
        return False
    
    required_files = [
        'frontend/package.json',
        'frontend/src/App.jsx',
        'frontend/src/App.css'
    ]
    
    for file in required_files:
        if not os.path.exists(file):
            print(f"  ❌ Missing file: {file}")
            return False
    
    print("  ✅ Frontend files present")
    return True


def main():
    """Run all verification tests."""
    print("=" * 60)
    print("Battle of Models v2.0 - Verification")
    print("=" * 60)
    
    tests = [
        test_imports,
        test_configuration,
        test_api_structure,
        test_environment,
        test_tests,
        test_frontend
    ]
    
    results = []
    for test in tests:
        try:
            results.append(test())
        except Exception as e:
            print(f"\n❌ Unexpected error in {test.__name__}: {e}")
            results.append(False)
    
    print("\n" + "=" * 60)
    passed = sum(results)
    total = len(results)
    print(f"Results: {passed}/{total} checks passed")
    
    if passed == total:
        print("✅ All checks passed! Ready to use.")
        print("\nQuick Start:")
        print("  Backend:  python api.py")
        print("  Frontend: cd frontend && npm run dev")
        print("  Docker:   docker-compose up")
        return 0
    else:
        print("⚠️  Some checks failed. Please review the output above.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
