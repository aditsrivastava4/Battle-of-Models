"""
FastAPI backend for Battle of Models debate application.
Provides REST API endpoints with Server-Sent Events (SSE) for streaming responses.
"""

import asyncio
import json
import os
from typing import AsyncGenerator
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from dotenv import load_dotenv
import warnings

from debate_module import __get_config, start_debate

# Load environment variables
load_dotenv()

# Suppress warnings
warnings.filterwarnings('ignore')

# Configuration
ALLOWED_ORIGINS = os.getenv("ALLOWED_ORIGINS", "*").split(",")

# Initialize FastAPI app
app = FastAPI(title="Battle of Models API", version="2.0.0")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,  # Configure via ALLOWED_ORIGINS env var
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global state
debate_state = {
    'round_no': 1,
    'config': None,
    'topic': '',
    'summary': ''
}

ENTITIES = {
    'c1': 'Contestant 1',
    'c2': 'Contestant 2',
    'moderator': 'Moderator'
}


class DebateRequest(BaseModel):
    topic: str


class DebateResetRequest(BaseModel):
    pass


async def generate_debate_stream(topic: str) -> AsyncGenerator[str, None]:
    """
    Generate debate responses as Server-Sent Events stream.
    
    Args:
        topic (str): The debate topic
        
    Yields:
        str: SSE formatted messages with debate responses
    """
    global debate_state
    
    if debate_state['round_no'] == 1:
        # Initialize the configuration only before the first round
        debate_state['config'] = __get_config()
        debate_state['topic'] = topic
    
    # Send topic event
    yield f"data: {json.dumps({'type': 'topic', 'content': debate_state['topic'], 'sender': 'Topic'})}\n\n"
    
    for entity in ['moderator', 'c1', 'c2']:
        # Generate response for each entity
        try:
            response = start_debate(
                entity, 
                debate_state['topic'], 
                debate_state['config'], 
                debate_state['summary']
            )
            
            if entity == 'moderator':
                debate_state['summary'] = f'Moderator: {response}\n'
            else:
                debate_state['summary'] = f"{debate_state['summary']}\n{ENTITIES[entity]}: {response}\n"
            
            # Send start event for this entity
            yield f"data: {json.dumps({'type': 'start', 'sender': ENTITIES[entity]})}\n\n"
            
            # Stream response character by character for typewriter effect
            for char in response:
                yield f"data: {json.dumps({'type': 'char', 'content': char, 'sender': ENTITIES[entity]})}\n\n"
                await asyncio.sleep(0.003)  # Faster typing effect
            
            # Send complete event for this entity
            yield f"data: {json.dumps({'type': 'complete', 'sender': ENTITIES[entity], 'content': response})}\n\n"
            
            # Small delay between entities
            await asyncio.sleep(0.3)
            
        except Exception as e:
            yield f"data: {json.dumps({'type': 'error', 'message': str(e), 'sender': ENTITIES[entity]})}\n\n"
    
    # Increment round number
    debate_state['round_no'] += 1
    
    # Send done event
    yield f"data: {json.dumps({'type': 'done', 'round': debate_state['round_no']})}\n\n"


@app.get("/")
async def root():
    """Root endpoint with API information."""
    return {
        "name": "Battle of Models API",
        "version": "2.0.0",
        "endpoints": {
            "/health": "Health check",
            "/debate": "Start a debate (POST with topic)",
            "/debate/reset": "Reset debate state (POST)",
            "/debate/stream": "Stream debate responses (GET with topic query param)"
        }
    }


@app.get("/health")
async def health():
    """Health check endpoint."""
    return {"status": "healthy", "round": debate_state['round_no']}


@app.post("/debate")
async def start_debate_endpoint(request: DebateRequest):
    """
    Start a debate with Server-Sent Events streaming.
    
    Args:
        request: DebateRequest with topic
        
    Returns:
        StreamingResponse with SSE events
    """
    if not request.topic or len(request.topic.strip()) == 0:
        raise HTTPException(status_code=400, detail="Topic cannot be empty")
    
    return StreamingResponse(
        generate_debate_stream(request.topic),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
        }
    )


@app.post("/debate/reset")
async def reset_debate():
    """Reset the debate state."""
    global debate_state
    debate_state['round_no'] = 1
    debate_state['config'] = None
    debate_state['topic'] = ''
    debate_state['summary'] = ''
    return {"status": "reset", "message": "Debate state has been reset"}


@app.get("/debate/state")
async def get_debate_state():
    """Get current debate state."""
    return {
        "round": debate_state['round_no'],
        "topic": debate_state['topic'],
        "has_summary": len(debate_state['summary']) > 0
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
