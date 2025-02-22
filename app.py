import asyncio
import warnings
import gradio as gr
from dotenv import load_dotenv
from debate_module import __get_config, start_debate

# Load environment variables from .env file
load_dotenv()

# Suppress warnings
warnings.filterwarnings('ignore')

# Initialize round number and config
round_no = 1
config = None
phase = 1  # 1: Contestant 1, 2: Contestant 2, 3: Moderator
ENTITIES = {
    'c1': 'Contestant 1',
    'c2': 'Contestant 2',
    'moderator': 'Moderator'
}
summary = ''
topic = ''


async def typewriter_effect(response, sender, chat_history):
    """
    Simulates a typewriter effect by incrementally updating the chat history with each character of the response.

    Args:
        response (str): The response to be displayed with the typewriter effect.
        sender (str): The sender of the response (e.g., 'Contestant 1', 'Contestant 2', 'Moderator').
        chat_history (list): The chat history to be updated.

    Yields:
        gr.update: Updates the chat history with the current state of the response.
    """
    message = ""
    for char in response:
        message += char
        chat_history[-1] = (sender, message)
        yield gr.update(value=chat_history)
        await asyncio.sleep(0.05)  # Adjust the delay for typing speed


async def debate_response(user_input, chat_history):
    """
    Handles the debate response by generating responses from Contestant 1, Contestant 2, and the Moderator.

    Args:
        user_input (str): The topic entered by the user.
        chat_history (list): The chat history to be updated.

    Yields:
        gr.update: Updates the chat history and user input field.
    """
    global round_no, config, summary, topic, phase  # Use the global round number, config, summary, topic, and phase

    if round_no == 1 and phase == 1:
        # Initialize the configuration only before the first round
        config = __get_config()
        # Set the topic to the user input
        topic = user_input

    # Add the user input to the chat history
    chat_history.append(('Topic', user_input))
    yield gr.update(value=chat_history), gr.update(value="", interactive=False)

    # Contestant 1's response
    response = start_debate('c1', topic, config, summary)
    summary = f'{summary}\nContestant 1: {response}\n'
    chat_history.append(('Contestant 1', ""))
    async for update in typewriter_effect(response, 'Contestant 1', chat_history):
        yield update, gr.update(value="")
    await asyncio.sleep(2)  # Delay to simulate processing time

    # Contestant 2's response
    response = start_debate('c2', topic, config, summary)
    summary = f'{summary}\nContestant 2: {response}\n'
    chat_history.append(('Contestant 2', ""))
    async for update in typewriter_effect(response, 'Contestant 2', chat_history):
        yield update, gr.update(value="")
    await asyncio.sleep(2)  # Delay to simulate processing time

    # Moderator's response
    response = start_debate('moderator', topic, config, summary)
    summary = f'Moderator: {response}\n'
    chat_history.append(('Moderator', ""))
    async for update in typewriter_effect(response, 'Moderator', chat_history):
        yield update, gr.update(value="")

    # Reset phase for the next round
    phase = 1
    # Increment the round number for the next call
    round_no += 1


def clear_chat():
    """
    Clears the chat history and resets the round number and phase.

    Returns:
        tuple: An empty chat history and an updated user input field.
    """
    global round_no, phase
    round_no = 1  # Reset the round number
    phase = 1  # Reset the phase
    return [], gr.update(value="", interactive=True)


with gr.Blocks(css=".chatbot { height: 70vh !important; }") as demo:
    # Create the chat history component
    chat_history = gr.Chatbot(label="Debate Responses", elem_classes="chatbot")
    # Create the user input component
    user_input = gr.Textbox(label="Enter your question or statement:")
    # Create the clear button component
    clear_button = gr.Button("Reset Debate")
    # Create the next round button component
    next_round_button = gr.Button("Next Round")

    # Set up the submit action for the user input
    user_input.submit(
        debate_response,
        inputs=[user_input, chat_history],
        outputs=[chat_history, user_input]
    )

    # Set up the click action for the clear button
    clear_button.click(
        clear_chat,
        inputs=[],
        outputs=[chat_history, user_input]
    )

    # Set up the click action for the next round button
    next_round_button.click(
        debate_response,
        inputs=[user_input, chat_history],
        outputs=[chat_history, user_input]
    )

# Launch the Gradio interface
demo.launch()
