# app/main.py
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
import logging
import os
from .routers import review

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('code_review.log')
    ]
)

# Create logger for this module
logger = logging.getLogger(__name__)

# Create the FastAPI app instance
# This is the central object that all of your API's functionality will be registered against.
app = FastAPI(
    title="Code Review Assistant API",
    description="A comprehensive API that uses Google's Gemini AI to perform deep static analysis of source code, providing detailed quality metrics, issue detection, and improvement recommendations.",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify actual origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include the API router from the 'review.py' file.
# This makes all the endpoints defined in that router (e.g., /review/) available.
app.include_router(review.router)

# Mount the 'static' directory to serve frontend files (HTML, CSS, JS).
# The 'html=True' argument allows FastAPI to serve 'index.html' for the root path "/".
app.mount("/", StaticFiles(directory="app/static", html=True), name="static")

@app.on_event("startup")
async def startup_event():
    """Application startup event"""
    logger.info("Code Review Assistant API starting up...")
    
    # Check if required environment variables are set
    if not os.getenv("GEMINI_API_KEY"):
        logger.warning("GEMINI_API_KEY environment variable not set. API calls will fail.")
    else:
        logger.info("Gemini API key found. Service ready for code reviews.")

@app.on_event("shutdown")
async def shutdown_event():
    """Application shutdown event"""
    logger.info("Code Review Assistant API shutting down...")