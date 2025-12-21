from uuid import uuid4


def __get_config():
    return {
        'c1': {
            'model_name': 'llama3.1',
            'config': {
                'configurable': {
                    'thread_id': str(uuid4())
                }
            }
        },
        'c2': {
            'model_name': 'llama3.2',
            'config': {
                'configurable': {
                    'thread_id': str(uuid4())
                }
            }
        },
        'moderator': {
            'model_name': 'llama3',
            'config': {
                'configurable': {
                    'thread_id': str(uuid4())
                }
            }
        }
    }
