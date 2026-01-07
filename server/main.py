import asyncio
import os
import sys
import logging
from loguru import logger
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from server.app.api.landing import router as landing_router
from server.app.api.playground import router as playground_router

# Creating Main App
app = FastAPI()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

FRONTEND_DIR = os.path.abspath(
    os.path.join(BASE_DIR, "..", "frontend")
)


# Setting static / templates files into FastAPI
app.mount("/static", StaticFiles(directory=os.path.join(FRONTEND_DIR,
          "static")), name="static")
app.mount("/assets", StaticFiles(directory=os.path.join(FRONTEND_DIR,
          "assets")), name="assets")


# app.include_router(auth_router)
app.include_router(landing_router)
app.include_router(playground_router)
