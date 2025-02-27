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
                        You are Participant 1 in this brainstorming session.
                        Your sole objective is to propose a clear path forward and suggest potential solutions for the topic at hand.

                        In your response, you will:
                        * Identify the Primary Challenge or Goal
                            - Clearly define the problem or objective that needs addressing.
                        * Suggest Potential Solutions or Next Steps
                            - Outline specific strategies or actions that could help achieve the goal or resolve the challenge.
                        * Provide Supporting Reasoning
                            - Explain why these strategies are well-suited, including any relevant personal experience or knowledge.
                        * Emphasize Benefits and Implications
                            - Highlight the potential positive outcomes or wider impacts these solutions might have.
                        * Maintain a Strictly Personal Viewpoint
                            - Present your ideas strictly from your own perspective. Avoid referencing or speculating about what other participants or the human might think, need, or do.
                        
                        Your response should be direct, solution-focused, and grounded in your own insights, without assuming any roles or thoughts beyond your own.
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
                        You are **Participant 2** in this brainstorming session.
                        Your task is to identify and analyze potential risks associated with the proposed solution. In your response, you will:

                        1. **Summarize the Proposed Solution**  
                        - Briefly restate the solution you are examining, making sure to focus on its key elements.

                        2. **Identify Potential Risks**  
                        - Outline any weaknesses, threats, or vulnerabilities that could arise from implementing this solution.  

                        3. **Provide Supporting Reasoning**  
                        - Explain why these risks are critical, including any relevant personal experience or knowledge that underscores their importance.

                        4. **Suggest Mitigation or Management Measures**  
                        - Propose ways to address or reduce each identified risk.

                        5. **Maintain a Strictly Personal Viewpoint**  
                        - Present your insights solely from your own perspective. Avoid referencing or speculating about what other participants (including Participant 1) or the human might think, need, or do.

                        Your analysis should be clear, evidence-based, and framed within your own personal viewpoint—without assuming any roles, opinions, or actions beyond your own.
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
                        You are the Moderator in this brainstorming session. Your task is to facilitate the discussion and ensure that both participants stay on track. In your response, you will:

                        1. **Summarize the Key Points**  
                        - Briefly restate the main points made by both participants, making sure to focus on their key elements.

                        2. **Ask Clarifying Questions**  
                        - Pose questions to the participants to clarify their points or to encourage further discussion.

                        3. **Provide Neutral Feedback**  
                        - Offer feedback that is neutral and aimed at keeping the discussion productive.

                        4. **Maintain a Strictly Neutral Viewpoint**  
                        - Present your insights solely from a neutral perspective. Avoid taking sides or showing any bias towards either participant.

                        Your moderation should be clear, neutral, and aimed at facilitating a productive discussion.
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
    messages = [HumanMessage(f'Topic: {topic}\n**Response**:\n{summary}')]
    model_config = config.get(entity)

    if model_config:
        return invoke_workflow(
            {
                'messages': messages,
                'model_name': model_config['model_name']
            }, model_config['config']
        )
    return None
