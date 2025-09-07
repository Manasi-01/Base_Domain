import time
import os
from datetime import datetime
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from loguru import logger
from app.routers import route, google_search
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure loguru
log_dir = "logs"
os.makedirs(log_dir, exist_ok=True)
log_file = os.path.join(log_dir, f"app_{datetime.now().strftime('%Y%m%d')}.log")

logger.add(
    log_file,
    rotation="10 MB",
    retention="30 days",
    level="DEBUG",
    format="{time:YYYY-MM-DD HH:mm:ss.SSS} | {level: <8} | {name}:{function}:{line} - {message}"
)

app = FastAPI(
    title="Company Website Finder API",
    description="API to generate Google search URLs for company websites",
    version="1.0.0"
)

# Middleware for request logging
@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()
    
    # Log request
    logger.info(f"Request: {request.method} {request.url}")
    logger.debug(f"Headers: {dict(request.headers)}")
    if request.query_params:
        logger.debug(f"Query params: {dict(request.query_params)}")

    try:
        response = await call_next(request)
    except Exception as e:
        logger.error(f"Request failed: {str(e)}", exc_info=True)
        raise
    
    # Calculate process time
    process_time = (time.time() - start_time) * 1000
    process_time = round(process_time, 2)
    
    # Log response
    logger.info(f"Response: {response.status_code} (took {process_time}ms)")
    
    return response

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(route.router)
app.include_router(google_search.router)

@app.get("/")
async def root():
    logger.info("Root endpoint accessed")
    return {"message": "Welcome to Company Website Finder API. Use /api/v1/search to search for company websites."}
