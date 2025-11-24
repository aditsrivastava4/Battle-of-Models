"""
Unit tests for debate module
"""

import pytest
from debate_module.resource import __get_config
from debate_module.state import State
from langchain_core.messages import HumanMessage


def test_get_config():
    """Test configuration generation."""
    config = __get_config()
    
    # Check that all entities are configured
    assert 'c1' in config
    assert 'c2' in config
    assert 'moderator' in config
    
    # Check structure
    for entity in ['c1', 'c2', 'moderator']:
        assert 'model_name' in config[entity]
        assert 'config' in config[entity]
        assert 'configurable' in config[entity]['config']
        assert 'thread_id' in config[entity]['config']['configurable']


def test_config_model_names():
    """Test that model names are correctly assigned."""
    config = __get_config()
    
    assert config['c1']['model_name'] == 'llama3.1'
    assert config['c2']['model_name'] == 'llama3.2'
    assert config['moderator']['model_name'] == 'llama3'


def test_config_unique_thread_ids():
    """Test that each entity gets a unique thread ID."""
    config = __get_config()
    
    thread_ids = [
        config['c1']['config']['configurable']['thread_id'],
        config['c2']['config']['configurable']['thread_id'],
        config['moderator']['config']['configurable']['thread_id']
    ]
    
    # Check all thread IDs are unique
    assert len(thread_ids) == len(set(thread_ids))


def test_state_structure():
    """Test State TypedDict structure."""
    # Create a valid state
    state = {
        'messages': [HumanMessage(content="Test message")],
        'model_name': 'llama3.1'
    }
    
    # Check that required fields are present
    assert 'messages' in state
    assert 'model_name' in state
    assert len(state['messages']) > 0
    assert isinstance(state['model_name'], str)


def test_multiple_config_calls():
    """Test that calling __get_config multiple times generates different thread IDs."""
    config1 = __get_config()
    config2 = __get_config()
    
    # Thread IDs should be different between calls
    assert config1['c1']['config']['configurable']['thread_id'] != \
           config2['c1']['config']['configurable']['thread_id']


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
