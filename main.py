import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    filename="app.log",
    filemode="a",
    format="%(name)s - %(levelname)s - %(message)s",
)

import os
import traceback
import uuid
from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from database import get_db, init_db
from models import Agent, Config
from services.livekit_service import list_dispatch_rules, list_trunks


async def production_exception_handler(request: Request, exc: Exception):
    error_id = uuid.uuid4()

    # Log the detailed exception
    logging.error(f"Error ID: {error_id} - Unhandled exception: {exc}")
    logging.error(traceback.format_exc())

    return JSONResponse(
        status_code=500,
        content={
            "message": "An unexpected error occurred. Please contact support and provide this error ID.",
            "error_id": str(error_id),
        },
    )


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Initialize DB on startup
    init_db()
    yield


app = FastAPI(lifespan=lifespan)
app.add_exception_handler(Exception, production_exception_handler)

# Get the directory of the current file
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
templates = Jinja2Templates(directory=os.path.join(BASE_DIR, "templates"))


def load_config(db: Session):
    config_items = db.query(Config).all()
    return {item.key: item.value for item in config_items}


def save_config(db: Session, key: str, value: str):
    config_item = db.query(Config).filter(Config.key == key).first()
    if config_item:
        config_item.value = value
    else:
        config_item = Config(key=key, value=value)
        db.add(config_item)
    db.commit()


@app.get("/tab/dashboard", response_class=HTMLResponse)
async def tab_dashboard(request: Request):
    return templates.TemplateResponse("dashboard.html", {"request": request})


@app.get("/tab/agents", response_class=HTMLResponse)
async def tab_agents(request: Request, db: Session = Depends(get_db)):
    agents = db.query(Agent).all()
    return templates.TemplateResponse("agents.html", {"request": request, "agents": agents})


@app.get("/tab/settings", response_class=HTMLResponse)
async def tab_settings(request: Request, db: Session = Depends(get_db)):
    config = load_config(db)
    return templates.TemplateResponse("settings.html", {"request": request, "config": config})


@app.post("/agents")
async def create_agent(request: Request, db: Session = Depends(get_db)):
    form = await request.form()
    agent_id = str(uuid.uuid4())[:8]
    new_agent = Agent(
        id=agent_id,
        name=form["name"],
        type=form["type"],
        description=form.get("description", ""),
        config="{}",
    )
    db.add(new_agent)
    db.commit()

    return templates.TemplateResponse("agent_item.html", {"request": request, "agent": new_agent})


@app.delete("/agents/{agent_id}")
async def delete_agent(agent_id: str, db: Session = Depends(get_db)):
    agent = db.query(Agent).filter(Agent.id == agent_id).first()
    if agent:
        db.delete(agent)
        db.commit()
    return ""


@app.post("/settings/livekit")
async def update_livekit_settings(request: Request, db: Session = Depends(get_db)):
    form = await request.form()
    save_config(db, "livekit_url", form["url"])
    save_config(db, "livekit_api_key", form["key"])
    save_config(db, "livekit_api_secret", form["secret"])
    return "Configuration updated successfully ✔"


@app.get("/", response_class=HTMLResponse)
async def index(request: Request, db: Session = Depends(get_db)):
    config = load_config(db)
    return templates.TemplateResponse(
        "index.html",
        {"request": request, "config": config},
    )


@app.post("/prompt")
async def update_prompt(request: Request, db: Session = Depends(get_db)):
    form = await request.form()
    save_config(db, "system_prompt", form["prompt"])
    return "Saved ✔"


@app.get("/agents/{agent_id}/test", response_class=HTMLResponse)
async def test_agent(request: Request, agent_id: str, db: Session = Depends(get_db)):
    agent = db.query(Agent).filter(Agent.id == agent_id).first()
    if not agent:
        return "Agent not found"

    return templates.TemplateResponse("test_agent.html", {"request": request, "agent": agent})


@app.get("/trunks", response_class=HTMLResponse)
async def trunks(request: Request, db: Session = Depends(get_db)):
    try:
        trunks_data = await list_trunks(db)
        return templates.TemplateResponse("trunks_table.html", {"request": request, "trunks": trunks_data})
    except Exception as e:
        return f"<div class='p-4 bg-red-50 text-red-700 rounded-lg border border-red-200 flex items-center'><i class='fas fa-exclamation-circle mr-2'></i>Error fetching trunks: {str(e)}</div>"


@app.get("/dispatch-rules", response_class=HTMLResponse)
async def dispatch_rules(request: Request, db: Session = Depends(get_db)):
    try:
        rules_data = await list_dispatch_rules(db)
        return templates.TemplateResponse("rules_table.html", {"request": request, "rules": rules_data})
    except Exception as e:
        return f"<div class='p-4 bg-red-50 text-red-700 rounded-lg border border-red-200 flex items-center'><i class='fas fa-exclamation-circle mr-2'></i>Error fetching dispatch rules: {str(e)}</div>"


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=9001)
