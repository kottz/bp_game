from typing import List
from fastapi import FastAPI
from starlette.responses import HTMLResponse, PlainTextResponse
from starlette.requests import Request
from starlette.staticfiles import StaticFiles
from starlette.templating import Jinja2Templates
from starlette.websockets import WebSocket, WebSocketDisconnect
from game_async import Game, TextView, MusicView
import asyncio
import mpv

class OnlineTextView:

    initialized = False
    prevStage = ""

    def _update(self, subject):
        
        if(subject.currentStage != self.prevStage):
            self.prevStage = subject.currentStage
            if(subject.currentStage == "intro"):
                return ("Winner is: " + subject.winner)
            return ("--- CURRENT STAGE: " + subject.currentStage + " ---")
        else:
            return (" Active light: "+str(subject.activeLight))

    def update(self, subject):
        asyncio.create_task(notifier.push(self._update(subject)))

class OnlineTextView2:
    def update(self, subject):
        asyncio.create_task(notifier.push(subject.to_dict()))

player = mpv.MPV()
game = Game('edward', 'viktor', 'anton', 'erik')
tv = TextView()
music = MusicView(player)
game.attach(tv)
game.attach(music)
otv = OnlineTextView2()
game.attach(otv)

app = FastAPI()
app.mount('/static', StaticFiles(directory='static'), name="static")

class Notifier:
    def __init__(self):
        self.connections: List[WebSocket] = []
        self.generator = self.get_notification_generator()

    async def get_notification_generator(self):
        while True:
            message = yield
            await self._notify(message)

    async def push(self, msg: str):
        await self.generator.asend(msg)

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.connections.append(websocket)

    def remove(self, websocket: WebSocket):
        self.connections.remove(websocket)

    async def _notify(self, message: str):
        living_connections = []
        while len(self.connections) > 0:
            # Looping like this is necessary in case a disconnection is handled
            # during await websocket.send_text(message)
            websocket = self.connections.pop()
            await websocket.send_json(message)
            living_connections.append(websocket)
        self.connections = living_connections


notifier = Notifier()


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await notifier.connect(websocket)
    try:
        while True:
            data = await websocket.receive_json()
            if data['action'] == "drink_event":
                await send_game_event()
            if data['action'] == "start_game" and not game.running:
                game.playerArray = data['players']
                print(game.playerArray)
                await run_game()
            #await websocket.send_text(f"Message text was: {data}")
    except WebSocketDisconnect:
        notifier.remove(websocket)


@app.get("/push/{message}")
async def push_to_connected_websockets(message: str):
    await notifier.push(f"! Push notification: {message} !")


@app.on_event("startup")
async def startup():
    # Prime the push notification generator
    await notifier.generator.asend(None)


@app.get("/game")
async def run_game():
    if not game.running:
        asyncio.create_task(game.runGame())
        return {"started game"}
    return {"game already running"}


@app.get("/send_game_event")
async def send_game_event():
    game.drinkEvent.set()
    return {"sent event"}

templates = Jinja2Templates(directory="templates")
@app.get("/")
async def home(request: Request):
    return templates.TemplateResponse('index.html', {'request': request})
