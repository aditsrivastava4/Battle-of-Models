# Battle of Models

This project is a debate simulation using language models. It allows users to input a topic and receive responses from two contestants and a moderator. The responses are streamed with a typewriter effect.

## Prerequisites

- Python 3.10 or higher
- pip (Python package installer)

## Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/aditsrivastava4/Battle-of-Models.git
    cd debate-llm
    ```

2. Create a virtual environment:

    ```bash
    python -m venv env
    ```

3. Activate the virtual environment:

    - On Windows:

        ```bash
        .\env\Scripts\activate
        ```

    - On macOS and Linux:

        ```bash
        source env/bin/activate
        ```

4. Install the required packages:

    ```bash
    pip install -r requirements.txt
    ```

5. Set up environment variables:

    - Copy the `.env.template` file to `.env`.
    - Open the `.env` file and add your API keys and other necessary configurations.

## Running the Project

1. Start the debate simulation:

    ```bash
    python app.py
    ```

2. Open your web browser and go to the URL provided by Gradio (usually `http://127.0.0.1:7860`).

3. Enter a topic in the text box and press Enter. The responses from Contestant 1, Contestant 2, and the Moderator will be streamed with a typewriter effect.

## Project Structure

- `app.py`: Main application file that sets up the Gradio interface and handles the debate logic.
- `debate_module`: Contains the core logic for the debate simulation.
  - `__init__.py`: Initializes the debate module.
  - `main.py`: Contains the main functions for invoking the workflow and starting the debate.
  - `resource.py`: Provides the configuration for the language models.
  - `state.py`: Defines the state schema for the workflow.
- `.env.template`: Template for environment variables.
- `requirements.txt`: List of required Python packages.

## License

This project is licensed under the MIT License. See the LICENSE file for details.