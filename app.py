import subprocess
from debate_module import __get_config, start_debate
import gradio as gr
import warnings
import asyncio

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
    message = ""
    for char in response:
        message += char
        chat_history[-1] = (sender, message)
        yield gr.update(value=chat_history)
        await asyncio.sleep(0.05)  # Adjust the delay for typing speed


async def debate_response(user_input, chat_history):
    # Use the global round number, config, summary, topic, and phase
    global round_no, config, summary, topic, phase

    if round_no == 1 and phase == 1:
        config = __get_config()  # Call __get_config() only before round 1

    # Add the user input to the chat history
    topic = user_input
    chat_history.append(('Topic', user_input))
    yield gr.update(value=chat_history), gr.update(value="")

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

    phase = 1  # Reset phase for the next round
    round_no += 1  # Increment the round number for the next call


def clear_chat():
    global round_no, phase
    round_no = 1  # Reset the round number
    phase = 1  # Reset the phase
    return [], ""


with gr.Blocks(css=".chatbot { height: 70vh !important; }") as demo:
    chat_history = gr.Chatbot(label="Debate Responses", elem_classes="chatbot")
    user_input = gr.Textbox(label="Enter your question or statement:")
    clear_button = gr.Button("Reset Debate")
    next_round_button = gr.Button("Next Round")

    user_input.submit(
        debate_response,
        inputs=[user_input, chat_history],
        outputs=[chat_history, user_input]
    )

    clear_button.click(
        clear_chat,
        inputs=[],
        outputs=[chat_history, user_input]
    )

    next_round_button.click(
        debate_response,
        inputs=[user_input, chat_history],
        outputs=[chat_history, user_input]
    )

demo.launch()
