```mermaid
graph TD
    A[app.py] -->|Load environment variables| B[Load .env file]
    A -->|Suppress warnings| C[Filter warnings]
    A -->|Initialize variables| D[Initialize round_no, config, ENTITIES, topic, summary]
    A -->|Define functions| E[restart_ollama_server, typewriter_effect, debate_response, clear_chat]
    A -->|Create Gradio interface| F[Gradio Blocks]
    
    F -->|Create components| G[chat_history, user_input, clear_button, next_round_button]
    G -->|Set up actions| H[Submit, Click actions]
    H -->|Launch interface| I[demo.launch()]

    E -->|restart_ollama_server| J[Stop and start Ollama server]
    E -->|typewriter_effect| K[Simulate typewriter effect]
    E -->|debate_response| L[Handle debate response]
    E -->|clear_chat| M[Clear chat history]

    L -->|Initialize config| N[__get_config()]
    L -->|Generate responses| O[start_debate]
    O -->|Invoke workflow| P[invoke_workflow]
    P -->|Initialize workflow| Q[init_workflow]
    Q -->|Compile workflow| R[StateGraph, MemorySaver]
    P -->|Call model| S[call_model]
    S -->|Get prompt| T[__get_prompt]
    S -->|Invoke model| U[ChatGroq, Ollama]

    N -->|Return config| V[Configuration dictionary]
    O -->|Return response| W[Response string]
    P -->|Return messages| X[Messages content]
    L -->|Update chat history| Y[Update chat history]
    M -->|Reset variables| Z[Reset round_no, summary]
```