import asyncio
import warnings
import gradio as gr
from dotenv import load_dotenv
import subprocess
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
topic = ''


def restart_ollama_server():
    """
    Restarts the Ollama server by stopping any running instances and starting a new one.

    This function performs the following steps:
    1. Uses PowerShell to find and stop any running processes with names that include 'ollama'.
    2. Starts a new instance of the Ollama server using PowerShell.

    Note:
    - This function assumes that 'powershell.exe' is available in the system's PATH.
    - The 'ollama' command should be available and properly configured to start the server.

    Raises:
    - subprocess.CalledProcessError: If the subprocess.run or subprocess.Popen commands fail.
    """
    # Stop any running Ollama processes
    subprocess.run(
        [
            "powershell.exe", "-Command",
            "Get-Process | Where-Object {$_.ProcessName -like '*ollama*'} | Stop-Process"
        ]
    )
    # Start a new Ollama server instance
    subprocess.Popen(["powershell.exe", "-Command", "ollama.exe", "serve"])


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
        await asyncio.sleep(0.01)  # Adjust the delay for typing speed


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
    else:
        # restart_ollama_server()  # Restart the Ollama server for subsequent rounds
        # Above line is for restarting the Ollama server, if you have a GPU with low memory, you can uncomment it.
        # As it will free up the memory, as this app is loading multiple models in the background.
        pass

    # Add the user input to the chat history
    chat_history.append(('Topic', topic))
    yield gr.update(value=chat_history), gr.update(value="", interactive=False)

    for entity in ['c1', 'c2', 'moderator']:
        # Generate response for each entity
        response = start_debate(entity, topic, config, summary)
        if entity == 'moderator':
            # Add the moderator's response to the summary
            summary = f'Moderator: {response}\n'
        else:
            # Add the entity's response to the summary
            summary = f'{summary}\n{ENTITIES[entity]}: {response}\n'
        chat_history.append((ENTITIES[entity], ""))
        async for update in typewriter_effect(response, ENTITIES[entity], chat_history):
            yield update, gr.update(value="")
        await asyncio.sleep(2)  # Delay to simulate processing time

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
    global round_no, phase, summary  # Use the global round number and phase
    summary = ''  # Reset the summary
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
