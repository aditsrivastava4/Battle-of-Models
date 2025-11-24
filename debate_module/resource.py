import os
from uuid import uuid4


def __get_config():
    """
    Get configuration for debate models.
    
    Models can be configured via environment variables:
    - CONTESTANT1_MODEL: Model for contestant 1 (default: llama3.1)
    - CONTESTANT2_MODEL: Model for contestant 2 (default: llama3.2)
    - MODERATOR_MODEL: Model for moderator (default: llama3)
    - GROQ_MODEL_NAME: Specific model name for Groq API (default: llama-3.3-70b-versatile)
    """
    return {
        'c1': {
            'model_name': os.getenv('CONTESTANT1_MODEL', 'llama3.1'),
            'config': {
                'configurable': {
                    'thread_id': str(uuid4())
                }
            }
        },
        'c2': {
            'model_name': os.getenv('CONTESTANT2_MODEL', 'llama3.2'),
            'config': {
                'configurable': {
                    'thread_id': str(uuid4())
                }
            }
        },
        'moderator': {
            'model_name': os.getenv('MODERATOR_MODEL', 'llama3'),
            'config': {
                'configurable': {
                    'thread_id': str(uuid4())
                }
            }
        }
    }
