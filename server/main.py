import asyncio
import os
import sys
import logging
from loguru import logger
from dotenv import load_dotenv

from server.app.middleware.refresh_tokens import AutoRefreshMiddleware
from server.core.config import settings
from server.core.jwt_config import auth
from server.core.jwt_service import JWTService

# Load environment variables from .env file
load_dotenv()

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import FileResponse
from server.app.api.landing import router as landing_router
from server.app.api.playground import router as playground_router
from server.app.api.auth import router as auth_router
from server.app.api.dashboard import router as dashboard_router
from server.app.api.v1.refresh_tokens import router as refresh_tokens_router
from server.app.api.v1.time_entries import router as time_entries_router
from server.app.api.v1.auth import router as api_auth_router

# === Intercept standard logging and redirect to Loguru ===
class InterceptHandler(logging.Handler):
    """Intercept standard logging messages and redirect them to Loguru."""
    def emit(self, record):
        # Get corresponding Loguru level if it exists
        try:
            level = logger.level(record.levelname).name
        except ValueError:
            level = record.levelno

        # Find caller from where the logged message originated
        frame, depth = sys._getframe(6), 6
        while frame and frame.f_code.co_filename == logging.__file__:
            frame = frame.f_back
            depth += 1

        logger.opt(depth=depth, exception=record.exc_info).log(level, record.getMessage())

# Remove default Loguru handler and add custom one
# logger.remove()

# Intercept all standard logging and redirect to Loguru
logging.basicConfig(handlers=[InterceptHandler()], level=0, force=True)

# Redirect uvicorn loggers to Loguru
for logger_name in ["uvicorn", "uvicorn.error", "uvicorn.access"]:
    logging_logger = logging.getLogger(logger_name)
    logging_logger.handlers = [InterceptHandler()]
    logging_logger.propagate = False

def handle_exception(exc_type, exc_value, exc_traceback):
    logger.error("Uncaught exception", exc_info=(exc_type, exc_value, exc_traceback))

sys.excepthook = handle_exception


# Creating Main App
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:8080", "https://reflectly.myroslavrepin.com"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Paths settings
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

FRONTEND_DIR = os.path.abspath(
    os.path.join(BASE_DIR, "..", "frontend", "dist")
)


# Setting static / templates files into FastAPI
app.mount("/assets", StaticFiles(directory=os.path.join(FRONTEND_DIR, "assets")), name="assets")


# app.include_router(auth_router)
app.include_router(landing_router)
app.include_router(playground_router)
app.include_router(auth_router)
app.include_router(dashboard_router)
app.include_router(refresh_tokens_router)
app.include_router(time_entries_router)
app.include_router(api_auth_router)

if "__main__" == __name__:
    import uvicorn
    uvicorn.run(app, host=settings.server_host, port=settings.server_port, reload=settings.server_reload)