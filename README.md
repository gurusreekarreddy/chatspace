# chatspace
to maks chatting easier 
# Chatspace (Slack-like app in Python)

A minimal Slack-like chat application scaffold built with FastAPI and WebSockets.

Features
- Room-based real-time messaging (in-memory)
- Minimal HTML client for quick testing

Quickstart
1) Create a virtual environment and install deps
   - python3 -m venv .venv
   - source .venv/bin/activate
   - pip install -r requirements.txt

2) Run the server
   - uvicorn app.main:app --reload

3) Open the UI
   - Visit http://127.0.0.1:8000 in your browser

Notes
- This scaffold uses in-memory storage for connections and rooms; it is not persistent. For production, add a proper datastore (e.g., PostgreSQL + SQLAlchemy) and authentication.
- The project is initialized as a Git repository with the main branch.
