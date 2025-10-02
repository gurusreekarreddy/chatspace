# WARP.md

This file provides guidance to WARP (warp.dev) when working with code in this repository.

Project overview
- Chatspace: a minimal Slack-like chat scaffold built with FastAPI and WebSockets.
- Real-time rooms are implemented in-memory (no persistence). A minimal HTML client is provided for manual testing.

Common commands
- Setup dependencies and virtualenv
  - make setup
- Start the development server (auto-reload enabled)
  - make run
- Clean local artifacts (venv and caches)
  - make clean
- Health check (server must be running)
  - curl -s http://127.0.0.1:8000/health
- Open the UI
  - Visit http://127.0.0.1:8000 in a browser

Notes on tooling present
- Packaging/build: not configured (this is a runnable app, not a published package).
- Linting: not configured.
- Tests: not present.

Big-picture architecture
- Entry point: app/main.py
  - FastAPI app with three routes:
    - GET / → serves templates/index.html via Jinja2Templates
    - GET /health → returns {"status": "ok"}
    - WS /ws/{room}?username=... → WebSocket endpoint for room-based chat
  - ConnectionManager coordinates real-time messaging:
    - rooms: Dict[str, Set[WebSocket]] maps room name → connected websockets
    - usernames: Dict[WebSocket, str] tracks display names per connection
    - connect(room, ws, username): accept, register, and broadcast “joined”
    - broadcast(room, message): best-effort send to each connected client
    - disconnect(room, ws): unregister and cleanup; broadcast “left”
  - Message flow (high level):
    - Client connects to /ws/{room}?username=NAME
    - Server registers client and broadcasts a join notice
    - Client sends text frames → server broadcasts “NAME: message” to room
    - On disconnect, server removes client and broadcasts a leave notice
- Client: templates/index.html
  - Minimal HTML/JS that:
    - Builds ws(s):// URL using current location and selected room/username
    - Appends incoming messages to a scrollable log
    - Sends the contents of the input field on click/Enter
- Dependencies: see requirements.txt (fastapi, uvicorn[standard], jinja2)
- Developer entry points:
  - Server behavior: app/main.py (edit routing, broadcasting, connection lifecycle)
  - Client behavior: templates/index.html (WebSocket URL construction, UI)

Repo specifics and implications
- State is in-memory; restarting the server clears rooms and connections.
- The client constructs the WebSocket URL from window.location. If serving behind a proxy with a path prefix, you may need to update the client-side URL generation.

Docs and rules discovered
- README.md: Quickstart aligns with the commands above.
- No CLAUDE, Cursor, or Copilot rule files were found.
