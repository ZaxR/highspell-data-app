from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from nicegui import app as nicegui_app, ui
from app.api import router as api_router
from app.views import register_ui_pages

app = FastAPI()

# API setup
app.include_router(api_router, prefix="/api")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Replace with specific domains in prod
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Build UI elements
register_ui_pages()

ui.run_with(
    app,
)