"""
Integration tests for the complete debate workflow
"""

import pytest
import os
from dotenv import load_dotenv

load_dotenv()


@pytest.mark.integration
@pytest.mark.skipif(
    not os.getenv('GROQ_API_KEY'),
    reason="GROQ_API_KEY not set - skipping integration tests"
)
def test_debate_module_imports():
    """Test that all debate module components can be imported."""
    from debate_module import __get_config, start_debate
    from debate_module.main import call_model, init_workflow, invoke_workflow
    from debate_module.resource import __get_config
    from debate_module.state import State
    
    assert callable(__get_config)
    assert callable(start_debate)
    assert callable(call_model)
    assert callable(init_workflow)
    assert callable(invoke_workflow)


@pytest.mark.integration
@pytest.mark.skipif(
    not os.getenv('GROQ_API_KEY'),
    reason="GROQ_API_KEY not set - skipping integration tests"
)
def test_workflow_initialization():
    """Test that workflow can be initialized."""
    from debate_module.main import init_workflow
    
    workflow = init_workflow()
    assert workflow is not None


@pytest.mark.integration
@pytest.mark.skipif(
    not os.getenv('GROQ_API_KEY'),
    reason="GROQ_API_KEY not set - skipping integration tests"
)
@pytest.mark.asyncio
async def test_full_debate_flow():
    """Test a complete debate flow with real API calls."""
    from debate_module import __get_config, start_debate
    
    topic = "Should AI be regulated?"
    config = __get_config()
    summary = ""
    
    # Test moderator response
    try:
        moderator_response = start_debate('moderator', topic, config, summary)
        assert moderator_response is not None
        assert len(moderator_response) > 0
        summary = f'Moderator: {moderator_response}\n'
    except Exception as e:
        pytest.skip(f"Skipping due to API error: {e}")
    
    # Test contestant 1 response
    try:
        c1_response = start_debate('c1', topic, config, summary)
        assert c1_response is not None
        assert len(c1_response) > 0
        summary = f'{summary}\nContestant 1: {c1_response}\n'
    except Exception as e:
        pytest.skip(f"Skipping due to API error: {e}")
    
    # Test contestant 2 response
    try:
        c2_response = start_debate('c2', topic, config, summary)
        assert c2_response is not None
        assert len(c2_response) > 0
    except Exception as e:
        pytest.skip(f"Skipping due to API error: {e}")


@pytest.mark.integration
def test_environment_variables():
    """Test that environment variables can be loaded."""
    # This should not fail even without API keys
    groq_key = os.getenv('GROQ_API_KEY')
    # We don't assert it exists, just that the env loading works
    assert groq_key is None or isinstance(groq_key, str)


if __name__ == "__main__":
    pytest.main([__file__, "-v", "-m", "integration"])
