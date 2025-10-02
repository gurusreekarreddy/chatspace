from typing import Dict, Set

from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

app = FastAPI(title="Chatspace")
templates = Jinja2Templates(directory="templates")

class ConnectionManager:
    def __init__(self) -> None:
        self.rooms: Dict[str, Set[WebSocket]] = {}
        self.usernames: Dict[WebSocket, str] = {}

    async def connect(self, room: str, websocket: WebSocket, username: str) -> None:
        await websocket.accept()
        self.rooms.setdefault(room, set()).add(websocket)
        self.usernames[websocket] = username
        await self.broadcast(room, f"{username} joined {room}")

    def disconnect(self, room: str, websocket: WebSocket) -> None:
        if room in self.rooms:
            self.rooms[room].discard(websocket)
        self.usernames.pop(websocket, None)

    async def broadcast(self, room: str, message: str) -> None:
        for ws in list(self.rooms.get(room, set())):
            try:
                await ws.send_text(message)
            except Exception:
                # Ignore failed sends (e.g., disconnected clients)
                pass

manager = ConnectionManager()

@app.get("/", response_class=HTMLResponse)
async def index(request: Request) -> HTMLResponse:
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/health")
async def health() -> dict:
    return {"status": "ok"}

@app.websocket("/ws/{room}")
async def websocket_endpoint(websocket: WebSocket, room: str, username: str | None = None) -> None:
    if not username:
        username = "anonymous"

    await manager.connect(room, websocket, username)
    try:
        while True:
            data = await websocket.receive_text()
            await manager.broadcast(room, f"{username}: {data}")
    except WebSocketDisconnect:
        manager.disconnect(room, websocket)
        await manager.broadcast(room, f"{username} left {room}")
