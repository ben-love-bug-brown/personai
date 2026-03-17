"""NLP Service - Main API server for PersonAI"""

import asyncio
import json
import os
import sys
from aiohttp import web
from datetime import datetime

# Add parent to path
sys.path.insert(0, '/home/workspace/personai')

from src.llm import get_llm_client
from src.memory import get_memory
from src.planning.loop import MainLoop, get_main_loop
from src.planning.roadmap import get_roadmap


async def handle_chat(request):
    """Handle chat messages"""
    try:
        data = await request.json()
        message = data.get('message', '')
        
        loop = request.app['main_loop']
        result = await loop.send_message(message)
        
        return web.json_response({
            'response': result.get('response', 'No response'),
            'timestamp': datetime.now().isoformat()
        })
    except Exception as e:
        return web.json_response({'error': str(e)}, status=500)


async def handle_status(request):
    """Handle status requests"""
    loop = request.app['main_loop']
    status = loop.get_status()
    roadmap = get_roadmap()
    
    return web.json_response({
        'name': 'PersonAI',
        'version': '0.1.0',
        'status': status.get('running', False),
        'message_count': status.get('message_count', 0),
        'roadmap': roadmap.get_status_summary(),
        'personalization': 'active',
        'self_improvement': 'active'
    })


async def handle_history(request):
    """Handle history requests"""
    loop = request.app['main_loop']
    history = loop._conversation_history[-50:] if hasattr(loop, '_conversation_history') else []
    return web.json_response({'conversations': [{'messages': history}]})


async def handle_roadmap(request):
    """Handle roadmap requests"""
    roadmap = get_roadmap()
    return web.json_response(roadmap.get_status_summary())


async def handle_improve(request):
    """Handle self-improvement requests"""
    loop = request.app['main_loop']
    try:
        loop.trigger_self_improvement()
        return web.json_response({'status': 'improvement_triggered'})
    except Exception as e:
        return web.json_response({'error': str(e)}, status=500)


async def health_check(request):
    """Health check endpoint"""
    return web.json_response({'status': 'ok', 'service': 'personai-nlp'})


def create_app():
    """Create the aiohttp application"""
    app = web.Application()
    
    # Initialize components - memory needs storage path, not llm client
    memory = get_memory("/home/workspace/personai/data/memory.json")
    llm_client = get_llm_client()
    main_loop = MainLoop(llm_client, memory)
    
    # Store in app
    app['llm_client'] = llm_client
    app['memory'] = memory
    app['main_loop'] = main_loop
    
    # Start the main loop
    main_loop.start_async()
    
    # Add routes
    app.router.add_post('/chat', handle_chat)
    app.router.add_get('/status', handle_status)
    app.router.add_get('/history', handle_history)
    app.router.add_get('/roadmap', handle_roadmap)
    app.router.add_post('/improve', handle_improve)
    app.router.add_get('/health', health_check)
    
    return app


def main():
    """Main entry point"""
    print("Starting PersonAI NLP Service...")
    app = create_app()
    web.run_app(app, host='0.0.0.0', port=8765, print=None)


if __name__ == '__main__':
    main()
