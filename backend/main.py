from fastapi import FastAPI
from src.modules.auth.auth_controller import router as auth_router
from src.modules.patgpt_related.patgpt_related_controller import router as patgpt_related_router
from src.logger.log import logger
from fastapi.middleware.cors import CORSMiddleware
from src.config.env_config import settings
from contextlib import asynccontextmanager
from src.db.base_model import Base
from src.db.engine import get_db, engine
import json
import os
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info(f"Server started at http://localhost:{settings.PORT}")
    
    # Ensure database directory exists
    db_path = settings.DATABASE_URL.replace("sqlite:///", "")
    db_dir = os.path.dirname(db_path)
    if db_dir and not os.path.exists(db_dir):
        os.makedirs(db_dir)
        logger.info(f"Created database directory: {db_dir}")

    Base.metadata.create_all(engine)
    yield
    logger.info("Server stopped")

app=FastAPI(lifespan=lifespan)

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    error_details = jsonable_encoder(exc.errors())  
    logger.error(f"!!! Attention: Validation Error !!!")
    logger.error(f"Path: {request.url.path}")
    logger.error(f"Method: {request.method}")
    logger.error(f"Errors: {json.dumps(error_details, indent=2)}")
    try:
        body = await request.body()
        logger.error(f"Request Body: {body.decode()}")
    except:
        logger.error("Could not read request body")
    return JSONResponse(
        status_code=422,
        content={"detail": error_details},  
    )

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def health_check():
    logger.info("Health check request received")
    return {"status":"Server is running!"}
app.include_router(auth_router)
app.include_router(patgpt_related_router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="localhost", port=settings.PORT, reload=True)
