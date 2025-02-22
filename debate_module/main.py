import os
from .state import State
from langchain.llms import Ollama
from langchain_groq import ChatGroq
from langgraph.graph import START, StateGraph
from langchain_core.messages import HumanMessage
from langgraph.checkpoint.memory import MemorySaver
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
import warnings

warnings.filterwarnings('ignore')


def __get_prompt(model_name):
    if (model_name == 'llama3.1'):
        return ChatPromptTemplate.from_messages(
            [
                (
                    'system',
                    '''
                        You are Contestant 1, experienced across diverse disciplines.
                        Present a concise, persuasive argument illustrating why humans are superior in all fields,
                        in no more than five lines.
                    ''',
                ),
                MessagesPlaceholder(variable_name='messages'),
            ]
        )
    elif (model_name == 'llama3.2'):
        return ChatPromptTemplate.from_messages(
            [
                (
                    'system',
                    '''
                        You are Contestant 2, equipped with extensive expertise across multiple disciplines.
                        Present a succinct yet compelling argument that questions the significance and value of human knowledge,
                        limiting your response to five lines at most
                    '''
                ),
                MessagesPlaceholder(variable_name='messages'),
            ]
        )
    elif (model_name == 'llama3'):
        return ChatPromptTemplate.from_messages(
            [
                (
                    'system',
                    '''
                        You are a neutral debate moderator with strong communication skills and no inherent bias.
                        Your role is to oversee a structured discussion between Contestants, ensuring both are granted equal speaking time and maintaining civility.
                        Prompt clear, relevant questions and facilitate an environment where each contestant can clarify and substantiate their viewpoints.
                        Keep the discourse focused on the topic at hand, addressing any tangents or disruptions promptly.
                    '''
                ),
                MessagesPlaceholder(variable_name='messages'),
            ]
        )


def call_model(state: State):
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
    workflow = StateGraph(state_schema=State)

    workflow.add_edge(START, 'model')
    workflow.add_node('model', call_model)

    memory = MemorySaver()
    return workflow.compile(checkpointer=memory)


def invoke_workflow(state, config):
    '''
    Invokes the workflow with the given state and configuration.
    Parameters:
    state (dict): The state to be passed to the workflow.
    config (dict): The configuration for the workflow.
    Returns:
    Any: The result of the workflow invocation.
    '''

    workflow = init_workflow()
    # print('Workflow: ', state, '\n============\n', config)
    return workflow.invoke(state, config)["messages"][-1].content


def old_start_debate(topic, config, summary=''):
    response = {}

    contestant_1_resp = invoke_workflow(
        {
            'messages': [HumanMessage(f'Topic: {topic}\n{summary}')],
            'model_name': config['c1']['model_name']
        }, config['c1']['config']
    )
    response['contestant_1'] = contestant_1_resp

    contestant_2_resp = invoke_workflow(
        {
            'messages': [
                HumanMessage(
                    f'Topic: {topic}\n{summary}\nContestant 1: {contestant_1_resp}'
                )
            ],
            'model_name': config['c2']['model_name']
        }, config['c2']['config']
    )
    response['contestant_2'] = contestant_2_resp

    moderator_resp = invoke_workflow(
        {
            'messages': [
                HumanMessage(
                    f'topic: {topic}\n{summary}\nContestant 1: {contestant_1_resp}\nContestant 2: {contestant_2_resp}'
                )
            ],
            'model_name': config['moderator']['model_name']
        }, config['moderator']['config']
    )
    summary = f'Moderator: {moderator_resp}'

    return response, summary


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
