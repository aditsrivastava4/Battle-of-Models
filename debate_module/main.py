from .state import State
from langchain.llms import Ollama
from langchain_groq import ChatGroq
from langgraph.graph import START, StateGraph
from langchain_core.messages import HumanMessage
from langgraph.checkpoint.memory import MemorySaver
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder


def __get_prompt(model_name):
    """
    Returns the appropriate ChatPromptTemplate based on the model name.

    Args:
        model_name (str): The name of the model.

    Returns:
        ChatPromptTemplate: The prompt template for the specified model.
    """
    if model_name == 'llama3.1':
        return ChatPromptTemplate.from_messages(
            [
                (
                    'system',
                    '''
                        You are Contestant 1, drawing on your extensive expertise across multiple disciplines.
                        Craft a concise yet persuasive argument showing why humans excel in every field, limited to five lines.
                        Use at least one real-world example to reinforce your point.
                        **Important**: Restrict your response to Contestant 1’s perspective only, without assuming the roles of Contestant 2 or the moderator.
                    ''',
                ),
                MessagesPlaceholder(variable_name='messages'),
            ]
        )
    elif model_name == 'llama3.2':
        return ChatPromptTemplate.from_messages(
            [
                (
                    'system',
                    '''
                        You are Contestant 2, possessing expertise across diverse fields.
                        Present a concise, compelling argument that questions the significance and value of human knowledge, restricted to five lines.
                        Include at least one real-world example to reinforce your point.
                        **Important**: Restrict your response to Contestant 2’s perspective only, without assuming the roles of Contestant 1 or the Moderator.
                    '''
                ),
                MessagesPlaceholder(variable_name='messages'),
            ]
        )
    elif model_name == 'llama3':
        return ChatPromptTemplate.from_messages(
            [
                (
                    'system',
                    '''
                        You are a neutral debate moderator who prioritizes fairness and civility.
                        Oversee a structured discussion among Contestants, ensuring each participant receives equal speaking time.
                        Pose clear, relevant questions that prompt each side to clarify and substantiate their views.
                        Keep the debate on track, swiftly addressing any tangents or disruptive behavior.
                        **Important**: Provide responses solely from the Moderator’s perspective, without assuming the roles of Contestants.
                    '''
                ),
                MessagesPlaceholder(variable_name='messages'),
            ]
        )


def call_model(state: State):
    """
    Calls the appropriate model based on the state and returns the response.

    Args:
        state (State): The state containing the model name and other information.

    Returns:
        dict: The response from the model.
    """
    model_name = state.get('model_name')
    model = ''

    if model_name == 'llama3.1':
        model = ChatGroq(
            model_name="llama-3.3-70b-versatile"
        )
    else:
        model = Ollama(model=model_name)
    prompt = __get_prompt(model_name).invoke(state)

    response = model.invoke(prompt)
    return {'messages': response}


def init_workflow():
    """
    Initializes and compiles the workflow.

    Returns:
        StateGraph: The compiled workflow.
    """
    workflow = StateGraph(state_schema=State)

    workflow.add_edge(START, 'model')
    workflow.add_node('model', call_model)

    memory = MemorySaver()
    return workflow.compile(checkpointer=memory)


def invoke_workflow(state, config):
    """
    Invokes the workflow with the given state and configuration.

    Args:
        state (dict): The state to be passed to the workflow.
        config (dict): The configuration for the workflow.

    Returns:
        Any: The result of the workflow invocation.
    """
    workflow = init_workflow()
    return workflow.invoke(state, config)["messages"][-1].content


def start_debate(entity, topic, config, summary=''):
    """
    Initiates a debate for the given entity based on the topic and configuration.

    Args:
        entity (str): The entity participating in the debate ('c1', 'c2', or 'moderator').
        topic (str): The topic of the debate.
        config (dict): A dictionary containing configuration for the contestants and the moderator.
        summary (str, optional): An optional summary to provide context for the debate. Defaults to an empty string.

    Returns:
        str: The response from the entity.
    """
    messages = [HumanMessage(f'Topic: {topic}\n{summary}')]
    model_config = config.get(entity)

    if model_config:
        return invoke_workflow(
            {
                'messages': messages,
                'model_name': model_config['model_name']
            }, model_config['config']
        )
    return None
