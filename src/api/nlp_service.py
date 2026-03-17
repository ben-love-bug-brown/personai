"""NLP Service - Main API server for PersonAI"""

import sys
from aiohttp import web
from datetime import datetime

sys.path.insert(0, '/home/workspace/personai')

from src.llm import get_llm_client, LLMClient
from src.memory import get_memory, MemoryService
from src.planning.loop import MainLoop
from src.planning.roadmap import get_roadmap

LLM_CLIENT_KEY = web.AppKey("llm_client", LLMClient)
MEMORY_KEY = web.AppKey("memory", MemoryService)
MAIN_LOOP_KEY = web.AppKey("main_loop", MainLoop)


async def handle_chat(request):
    """Handle chat messages"""
    try:
        data = await request.json()
        message = data.get('message', '')

        loop = request.app[MAIN_LOOP_KEY]
        result = await loop.send_message(message)

        return web.json_response({
            'response': result.get('response', 'No response'),
            'timestamp': datetime.now().isoformat()
        })
    except Exception as e:
        return web.json_response({'error': str(e)}, status=500)


async def handle_status(request):
    """Handle status requests"""
    loop = request.app[MAIN_LOOP_KEY]
    status = loop.get_status()
    roadmap = get_roadmap()
    running = bool(status.get('running', False))

    return web.json_response({
        'name': 'PersonAI',
        'version': '0.1.0',
        'status': 'active' if running else 'stopped',
        'running': running,
        'message_count': status.get('message_count', 0),
        'roadmap': roadmap.get_status_summary(),
        'personalization': 'active',
        'self_improvement': 'active'
    })


async def handle_history(request):
    """Handle history requests"""
    loop = request.app[MAIN_LOOP_KEY]
    history = loop.get_history(50)
    return web.json_response({'conversations': [{'messages': history}]})


async def handle_roadmap(request):
    """Handle roadmap requests"""
    roadmap = get_roadmap()
    return web.json_response(roadmap.get_status_summary())


async def handle_improve(request):
    """Handle self-improvement requests"""
    loop = request.app[MAIN_LOOP_KEY]
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

    memory = get_memory("/home/workspace/personai/data/memory.json")
    llm_client = get_llm_client()
    main_loop = MainLoop(llm_client, memory)

    app[LLM_CLIENT_KEY] = llm_client
    app[MEMORY_KEY] = memory
    app[MAIN_LOOP_KEY] = main_loop

    main_loop.start_async()

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
