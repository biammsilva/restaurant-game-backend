import asyncio
import json
import logging
import websockets

logging.basicConfig()


async def counter(websocket, path):
    while True:
        message = await websocket.recv()
        data = json.loads(message)
        await websocket.send(json.dumps(data))


start_server = websockets.serve(counter, "localhost", 6789)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
