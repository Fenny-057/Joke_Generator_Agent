import os
import sys
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from agent import build_agent_graph

# Force UTF-8 encoding on Windows to prevent UnicodeEncodeError with emojis
try:
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')
except AttributeError:
    pass

app = FastAPI(title="Bollywood Comedy AI", version="1.0.0")

allowed_origins = [
    origin.strip()
    for origin in os.getenv("FRONTEND_URL", "http://127.0.0.1:5173").split(",")
    if origin.strip()
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ── Request / Response Models ──────────────────────────────────

class JokeRequest(BaseModel):
    topic: str


class JokeResponse(BaseModel):
    topic: str
    joke: str | None
    hidden_meaning: str | None
    is_valid: bool
    retry_count: int
    validation_errors: list[str]


# ── API Routes ─────────────────────────────────────────────────

@app.post("/api/joke", response_model=JokeResponse)
async def generate_joke(req: JokeRequest):
    topic = req.topic.strip()

    if not topic:
        raise HTTPException(status_code=400, detail="Topic is required.")

    initial_state = {
        "topic": topic,
        "joke": "",
        "hidden_meaning": "",
        "is_valid": False,
        "retry_count": 0,
        "validation_errors": [],
        "joke_history": [],
        "best_joke": None,
        "best_hidden_meaning": None,
        "force_fail_first": False
    }

    try:
        graph = build_agent_graph()
        final_state = graph.invoke(initial_state)
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))

    return JokeResponse(
        topic=topic,
        joke=final_state.get("joke"),
        hidden_meaning=final_state.get("hidden_meaning"),
        is_valid=final_state.get("is_valid", False),
        retry_count=final_state.get("retry_count", 0),
        validation_errors=final_state.get("validation_errors", []),
    )


@app.get("/api/health")
async def health():
    return {"status": "ok"}


# ── Serve built frontend (production) ─────────────────────────

frontend_dist = os.path.join(os.path.dirname(__file__), "Frontend", "dist")
if os.path.isdir(frontend_dist):
    app.mount("/", StaticFiles(directory=frontend_dist, html=True), name="frontend")


# ── Run with: uvicorn app:app --reload ─────────────────────────

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="0.0.0.0", port=int(os.getenv("PORT", 5000)), reload=True)
