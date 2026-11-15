import os
from pathlib import Path
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from axomai.config import settings
from axomai.api.routes import router as api_router

BASE_DIR = Path(__file__).resolve().parent

app = FastAPI(
    title="AxomAI AGI - Z1 Alpha Panel",
    description="Custom Visual Intelligence Panel for Z1 Alpha File Agent",
    version="0.1.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Templates
templates_dir = BASE_DIR / "templates"
templates = Jinja2Templates(directory=str(templates_dir))

# Include API routes
app.include_router(api_router)

@app.get("/", response_class=HTMLResponse)
async def serve_dashboard(request: Request):
    """Serve the modern Z1 Alpha Custom Panel"""
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={"project_name": settings.PROJECT_NAME}
    )

def start_server(host: str = "127.0.0.1", port: int = 8000, reload: bool = True):
    """Launch uvicorn server"""
    import uvicorn
    uvicorn.run("axomai.api.app:app", host=host, port=port, reload=reload)

if __name__ == "__main__":
    start_server()
