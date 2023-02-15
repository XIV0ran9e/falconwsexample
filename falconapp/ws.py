import falcon
import asyncio
#
from datetime import datetime
from falcon.uri import parse_query_string
from falcon.asgi import WebSocket
from falcon.errors import WebSocketDisconnected
from falcon.request import Request
from falcon.response import Response


class WebSocketTest:
    async def on_websocket(self, req: Request, ws: WebSocket):
        try:
            await ws.accept()
        except WebSocketDisconnected:
            return

        async def sink():
            while True:
                try:
                    message = await ws.receive_text()
                except falcon.WebSocketDisconnected:
                    break
                if message == 'ping':
                    await ws.send_text('pong')
                else:
                    await ws.send_text('echo: ' + message)

        sink_task = falcon.create_task(sink())

        while not sink_task.done():
            while ws.ready and not sink_task.done():
                await ws.send_text(datetime.now().isoformat())
                await asyncio.sleep(10)
        sink_task.cancel()
        try:
            await sink_task
        except asyncio.CancelledError:
            return
