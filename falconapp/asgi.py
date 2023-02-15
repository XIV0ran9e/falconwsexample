from falcon.asgi import App
#
from .ws import WebSocketTest

app = App()
app.add_route("/ws", WebSocketTest())
